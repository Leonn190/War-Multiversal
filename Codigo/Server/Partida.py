import json
import unicodedata
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[2]
PASTA_UNIVERSOS = RAIZ / "Dados" / "Universos"
LIMITE_PERSONAGENS_PARTIDA = 40


def _normalizar_nome(nome):
    texto = str(nome).strip().lower().replace("_", " ")
    texto = texto.replace("\u00c3\u00ad", "i").replace("\u00ed", "i")
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(letra for letra in texto if not unicodedata.combining(letra))
    return texto


def CarregarUniversos():
    universos = {}

    if not PASTA_UNIVERSOS.exists():
        return universos

    for caminho in PASTA_UNIVERSOS.glob("*.json"):
        try:
            dados = json.loads(caminho.read_text(encoding="utf-8"))
        except Exception:
            continue

        nome = dados.get("nome", caminho.stem.replace("_", " "))
        personagens = dados.get("personagens", [])
        if not isinstance(personagens, list):
            personagens = []

        item = {
            "nome": nome,
            "arquivo": caminho.name,
            "personagens": list(personagens),
            "quantidade_personagens": len(personagens),
        }
        universos[nome] = item
        universos[caminho.stem.replace("_", " ")] = item

    return universos


def ResolverUniversos(nomes):
    dados = CarregarUniversos()
    por_nome = {_normalizar_nome(nome): universo for nome, universo in dados.items()}
    resolvidos = []
    vistos = set()

    for nome in nomes:
        chave = _normalizar_nome(nome)
        universo = por_nome.get(chave)
        if not universo:
            continue

        nome_real = universo["nome"]
        if nome_real in vistos:
            continue

        vistos.add(nome_real)
        resolvidos.append(universo)

    return resolvidos


def ContarPersonagens(nomes):
    return sum(universo["quantidade_personagens"] for universo in ResolverUniversos(nomes))


def CriarPartida(jogadores, universos):
    universos_resolvidos = ResolverUniversos(universos)
    personagens = []

    for universo in universos_resolvidos:
        for personagem in universo["personagens"]:
            personagens.append({
                "nome": personagem,
                "universo": universo["nome"],
            })

    personagens = personagens[:LIMITE_PERSONAGENS_PARTIDA]

    return {
        "tipo": "ranqueada",
        "jogadores": [
            {
                "id": jogador["id"],
                "nome": jogador.get("nome", jogador["id"]),
                "universos": list(jogador["universos"]),
            }
            for jogador in jogadores
        ],
        "universos": [universo["nome"] for universo in universos_resolvidos],
        "personagens": personagens,
        "quantidade_personagens": len(personagens),
        "quantidade_jogadores": len(jogadores),
    }
