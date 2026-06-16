from Codigo.Server.Fila import FilaServidor
from Codigo.Server.Partida import ContarPersonagens


class Comunicacao:
    def __init__(self):
        self.JogadorId = "jogador_local"
        self.NomeJogador = "Jogador Local"

    def EntrarFilaRanqueada(self, universos):
        return FilaServidor.EntrarNaFila(self.JogadorId, self.NomeJogador, universos)

    def AtualizarFilaRanqueada(self):
        return FilaServidor.AtualizarJogador(self.JogadorId)

    def SairFilaRanqueada(self):
        return FilaServidor.SairDaFila(self.JogadorId)

    def ContarPersonagensUniversos(self, universos):
        return ContarPersonagens(universos)
