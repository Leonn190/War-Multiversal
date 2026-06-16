import json
from pathlib import Path


RAIZ = Path(__file__).resolve().parent
CAMINHO_CONFIG = RAIZ / "configfixa.json"

CONFIG_PADRAO = {
    "FPS": 200,
    "Volume": 0.5,
    "Claridade": 75,
    "Mudo": False,
    "FPS Visivel": True,
    "Shader": True,
    "LarguraBase": 1920,
    "AlturaBase": 1080,
    "Universos Ranqueados": [],
}


def NormalizarConfig(config):
    config_final = CONFIG_PADRAO.copy()

    if isinstance(config, dict):
        config_final.update(config)

    config_final["FPS"] = int(max(30, min(240, config_final.get("FPS", CONFIG_PADRAO["FPS"]))))
    config_final["Volume"] = float(max(0, min(1, config_final.get("Volume", CONFIG_PADRAO["Volume"]))))
    config_final["Claridade"] = int(max(0, min(100, config_final.get("Claridade", CONFIG_PADRAO["Claridade"]))))
    config_final["Mudo"] = bool(config_final.get("Mudo", False))
    config_final["FPS Visivel"] = bool(config_final.get("FPS Visivel", True))
    config_final["Shader"] = bool(config_final.get("Shader", True))
    config_final["LarguraBase"] = int(config_final.get("LarguraBase", 1920))
    config_final["AlturaBase"] = int(config_final.get("AlturaBase", 1080))

    universos_validos = {
        "Marvel",
        "DC",
        "The Boys",
        "Invencível",
        "League Of Legends",
        "Overwatch",
        "One Piece",
        "My Hero Academia",
        "Pokemon",
        "Gerais",
    }
    universos = config_final.get("Universos Ranqueados", [])
    if not isinstance(universos, list):
        universos = []
    config_final["Universos Ranqueados"] = [nome for nome in universos if nome in universos_validos]

    return config_final


def CarregarConfig():
    if not CAMINHO_CONFIG.exists():
        SalvarConfig(CONFIG_PADRAO)
        return CONFIG_PADRAO.copy()

    try:
        dados = json.loads(CAMINHO_CONFIG.read_text(encoding="utf-8"))
    except Exception:
        dados = {}

    config = NormalizarConfig(dados)
    SalvarConfig(config)
    return config


def SalvarConfig(config):
    config = NormalizarConfig(config)
    CAMINHO_CONFIG.write_text(json.dumps(config, indent=4, ensure_ascii=False), encoding="utf-8")
    return config
