import itertools
import time

from Codigo.Server.Partida import CriarPartida


QUANTIDADE_JOGADORES_PARTIDA = 5
MINIMO_UNIVERSOS_COMUNS = 2
TEMPO_BUSCA_ENCAIXE_MELHOR = 10


class FilaRanqueada:
    def __init__(self):
        self.Jogadores = {}
        self.PartidasPorJogador = {}
        self.CandidatoAtual = None

    def EntrarNaFila(self, jogador_id, nome, universos):
        universos_filtrados = [universo for universo in universos if universo]
        agora = time.time()
        self.Jogadores[jogador_id] = {
            "id": jogador_id,
            "nome": nome,
            "universos": universos_filtrados,
            "entrada": agora,
        }
        return self.AtualizarJogador(jogador_id)

    def SairDaFila(self, jogador_id):
        self.Jogadores.pop(jogador_id, None)
        self.PartidasPorJogador.pop(jogador_id, None)
        self._limpar_candidato_se_precisar()
        return {"status": "fora_da_fila"}

    def AtualizarJogador(self, jogador_id):
        self._atualizar_fila()

        if jogador_id in self.PartidasPorJogador:
            return {
                "status": "partida_encontrada",
                "partida": self.PartidasPorJogador[jogador_id],
            }

        if jogador_id not in self.Jogadores:
            return {"status": "fora_da_fila"}

        return {
            "status": "na_fila",
            "jogadores_na_fila": len(self.Jogadores),
            "aguardando_melhor_encaixe": self.CandidatoAtual is not None,
            "segundos_restantes": self._segundos_restantes(),
        }

    def _atualizar_fila(self):
        melhor = self._melhor_candidato()
        agora = time.time()

        if not melhor:
            self.CandidatoAtual = None
            return

        if not self.CandidatoAtual:
            self.CandidatoAtual = {
                "inicio": agora,
                "jogadores": melhor["jogadores"],
                "universos": melhor["universos"],
                "score": melhor["score"],
            }
            return

        if melhor["score"] > self.CandidatoAtual["score"]:
            self.CandidatoAtual["jogadores"] = melhor["jogadores"]
            self.CandidatoAtual["universos"] = melhor["universos"]
            self.CandidatoAtual["score"] = melhor["score"]

        if agora - self.CandidatoAtual["inicio"] >= TEMPO_BUSCA_ENCAIXE_MELHOR:
            self._iniciar_partida(self.CandidatoAtual["jogadores"], self.CandidatoAtual["universos"])
            self.CandidatoAtual = None

    def _melhor_candidato(self):
        if len(self.Jogadores) < QUANTIDADE_JOGADORES_PARTIDA:
            return None

        melhor = None
        for jogadores in itertools.combinations(self.Jogadores.values(), QUANTIDADE_JOGADORES_PARTIDA):
            universos_comuns = set(jogadores[0]["universos"])
            for jogador in jogadores[1:]:
                universos_comuns &= set(jogador["universos"])

            if len(universos_comuns) < MINIMO_UNIVERSOS_COMUNS:
                continue

            score = (
                len(universos_comuns),
                sum(len(jogador["universos"]) for jogador in jogadores),
                -sum(jogador["entrada"] for jogador in jogadores),
            )
            candidato = {
                "jogadores": list(jogadores),
                "universos": sorted(universos_comuns),
                "score": score,
            }

            if not melhor or candidato["score"] > melhor["score"]:
                melhor = candidato

        return melhor

    def _iniciar_partida(self, jogadores, universos):
        partida = CriarPartida(jogadores, universos)
        for jogador in jogadores:
            self.Jogadores.pop(jogador["id"], None)
            self.PartidasPorJogador[jogador["id"]] = partida

    def _segundos_restantes(self):
        if not self.CandidatoAtual:
            return 0

        restante = TEMPO_BUSCA_ENCAIXE_MELHOR - (time.time() - self.CandidatoAtual["inicio"])
        return max(0, int(restante))

    def _limpar_candidato_se_precisar(self):
        if not self.CandidatoAtual:
            return

        ids_ativos = set(self.Jogadores)
        ids_candidato = {jogador["id"] for jogador in self.CandidatoAtual["jogadores"]}
        if not ids_candidato <= ids_ativos:
            self.CandidatoAtual = None


FilaServidor = FilaRanqueada()
