import ast
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


RAIZ = Path(__file__).resolve().parents[1]
PASTA_RELATORIOS = RAIZ / "Documentação" / "Relatorios"
IGNORAR = {".git", "__pycache__", ".venv", "venv", "env", ".idea", ".vscode"}
DONO = "Leon Soto"


def CaminhosArquivos():
    arquivos = []

    for pasta, subpastas, nomes in os.walk(RAIZ):
        partes = set(Path(pasta).relative_to(RAIZ).parts)
        if partes & IGNORAR:
            continue

        subpastas[:] = [subpasta for subpasta in subpastas if subpasta not in IGNORAR]

        for nome in nomes:
            if nome == ".gitkeep":
                continue
            arquivos.append(Path(pasta) / nome)

    return arquivos


def RodarGit(comando):
    try:
        saida = subprocess.check_output(comando, cwd=RAIZ, stderr=subprocess.DEVNULL, text=True).strip()
        return saida
    except Exception:
        return ""


def InformacoesGit():
    total_commits = RodarGit(["git", "rev-list", "--count", "HEAD"])
    primeiro_commit = RodarGit(["git", "log", "--reverse", "--format=%ci", "--max-count=1"])

    if total_commits.isdigit():
        total_commits = int(total_commits)
    else:
        total_commits = 0

    dias = 0
    data_criacao = None

    if primeiro_commit:
        try:
            data_criacao = datetime.strptime(primeiro_commit[:19], "%Y-%m-%d %H:%M:%S")
            dias = (datetime.now() - data_criacao).days
        except Exception:
            data_criacao = None

    return total_commits, dias, data_criacao.isoformat() if data_criacao else None


def AnalisarPython(arquivos_py):
    linhas = 0
    classes = 0
    funcoes = 0
    metodos = 0
    maiores = []

    for arquivo in arquivos_py:
        try:
            texto = arquivo.read_text(encoding="utf-8")
        except Exception:
            texto = arquivo.read_text(encoding="latin-1", errors="ignore")

        qtd_linhas = len(texto.splitlines())
        linhas += qtd_linhas
        maiores.append((str(arquivo.relative_to(RAIZ)), qtd_linhas))

        try:
            arvore = ast.parse(texto)
        except SyntaxError:
            continue

        for node in ast.walk(arvore):
            if isinstance(node, ast.ClassDef):
                classes += 1
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        metodos += 1

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                funcoes += 1

    maiores.sort(key=lambda item: item[1], reverse=True)

    return {
        "linhas_py": linhas,
        "arquivos_py": len(arquivos_py),
        "classes_py": classes,
        "funcoes_metodos_py": funcoes,
        "metodos_py": metodos,
        "funcoes_soltas_py": max(0, funcoes - metodos),
        "top_10_maiores_py": maiores[:10],
    }


def TamanhoFormatado(bytes_total):
    unidades = ["B", "KB", "MB", "GB"]
    valor = float(bytes_total)

    for unidade in unidades:
        if valor < 1024:
            return f"{valor:.2f} {unidade}"
        valor /= 1024

    return f"{valor:.2f} TB"


def PastasPrincipaisCodigo(arquivos):
    ranking = {}
    base = RAIZ / "Codigo"

    for arquivo in arquivos:
        try:
            relativo = arquivo.relative_to(base)
        except ValueError:
            continue

        if len(relativo.parts) == 1:
            pasta = "Codigo"
        else:
            pasta = relativo.parts[0]

        ranking.setdefault(pasta, {"arquivos": 0, "linhas_py": 0, "bytes": 0})
        ranking[pasta]["arquivos"] += 1
        ranking[pasta]["bytes"] += arquivo.stat().st_size

        if arquivo.suffix == ".py":
            try:
                ranking[pasta]["linhas_py"] += len(arquivo.read_text(encoding="utf-8").splitlines())
            except Exception:
                pass

    return dict(sorted(ranking.items(), key=lambda item: item[1]["linhas_py"], reverse=True))


def RelatoriosAntigos():
    historico = []

    if not PASTA_RELATORIOS.exists():
        return historico

    for arquivo in PASTA_RELATORIOS.glob("*/dados.json"):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
            historico.append(dados)
        except Exception:
            pass

    historico.sort(key=lambda item: item.get("data", ""))
    return historico


def CriarGraficoBarras(caminho, ranking):
    if plt is None or not ranking:
        return False

    nomes = list(ranking.keys())
    valores = [ranking[nome]["linhas_py"] for nome in nomes]

    plt.figure(figsize=(10, 5))
    plt.bar(nomes, valores)
    plt.title("Linhas Python por pasta principal de Codigo")
    plt.ylabel("Linhas .py")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()
    return True


def CriarGraficoPizza(caminho, ranking):
    if plt is None or not ranking:
        return False

    filtrado = {nome: dados for nome, dados in ranking.items() if dados["linhas_py"] > 0}
    if not filtrado:
        return False

    plt.figure(figsize=(7, 7))
    plt.pie([dados["linhas_py"] for dados in filtrado.values()], labels=list(filtrado.keys()), autopct="%1.1f%%")
    plt.title("Distribuição de linhas Python por pasta")
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()
    return True


def CriarGraficoCrescimento(caminho, historico, chave, titulo, ylabel):
    if plt is None or len(historico) < 1:
        return False

    xs = list(range(1, len(historico) + 1))
    ys = [item.get(chave, 0) for item in historico]

    plt.figure(figsize=(10, 5))
    plt.plot(xs, ys, marker="o")
    plt.title(titulo)
    plt.xlabel("Relatórios")
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()
    return True


def CriarMarkdown(dados, imagens, prefixo_imagens=""):
    linhas = []
    linhas.append("# Registro do War Multiversal")
    linhas.append("")
    linhas.append(f"**Data:** {dados['data']}")
    linhas.append(f"**Autor:** {dados['autor']}")
    linhas.append("")
    linhas.append("## Resumo geral")
    linhas.append("")
    linhas.append(f"- Tamanho: {dados['tamanho_formatado']}")
    linhas.append(f"- Arquivos no geral: {dados['arquivos_total']}")
    linhas.append(f"- Número de commits: {dados['commits']}")
    linhas.append(f"- Dias desde a criação do repo: {dados['dias_desde_criacao_repo']}")
    linhas.append("")
    linhas.append("## Python")
    linhas.append("")
    linhas.append(f"- Linhas .py: {dados['linhas_py']}")
    linhas.append(f"- Arquivos .py: {dados['arquivos_py']}")
    linhas.append(f"- Classes .py: {dados['classes_py']}")
    linhas.append(f"- Métodos e funções .py: {dados['funcoes_metodos_py']}")
    linhas.append(f"- Métodos .py: {dados['metodos_py']}")
    linhas.append(f"- Funções soltas .py: {dados['funcoes_soltas_py']}")
    linhas.append("")
    linhas.append("## Top 10 maiores arquivos .py")
    linhas.append("")

    for indice, item in enumerate(dados["top_10_maiores_py"], 1):
        linhas.append(f"{indice}. `{item[0]}` — {item[1]} linhas")

    linhas.append("")
    linhas.append("## Rank das pastas principais de Codigo")
    linhas.append("")

    for indice, (nome, info) in enumerate(dados["pastas_codigo"].items(), 1):
        linhas.append(f"{indice}. `{nome}` — {info['linhas_py']} linhas .py, {info['arquivos']} arquivos")

    linhas.append("")
    linhas.append("## Gráficos")
    linhas.append("")

    for titulo, caminho in imagens.items():
        linhas.append(f"### {titulo}")
        linhas.append("")
        linhas.append(f"![{titulo}]({prefixo_imagens}{caminho})")
        linhas.append("")

    return "\n".join(linhas)


def GerarRelatorio():
    agora = datetime.now()
    nome = agora.strftime("%Y-%m-%d_%H-%M-%S")
    pasta = PASTA_RELATORIOS / nome
    pasta_imagens = pasta / "imagens"
    pasta_imagens.mkdir(parents=True, exist_ok=True)

    arquivos = CaminhosArquivos()
    arquivos_py = [arquivo for arquivo in arquivos if arquivo.suffix == ".py"]
    total_bytes = sum(arquivo.stat().st_size for arquivo in arquivos if arquivo.exists())
    commits, dias, data_criacao = InformacoesGit()
    py = AnalisarPython(arquivos_py)
    pastas_codigo = PastasPrincipaisCodigo(arquivos)

    dados = {
        "data": agora.isoformat(timespec="seconds"),
        "autor": DONO,
        "tamanho_bytes": total_bytes,
        "tamanho_formatado": TamanhoFormatado(total_bytes),
        "arquivos_total": len(arquivos),
        "commits": commits,
        "dias_desde_criacao_repo": dias,
        "data_criacao_repo": data_criacao,
        "pastas_codigo": pastas_codigo,
        **py,
    }

    historico = RelatoriosAntigos() + [dados]
    imagens = {}

    if CriarGraficoBarras(pasta_imagens / "pastas_codigo_barras.png", pastas_codigo):
        imagens["Barras das pastas principais"] = "imagens/pastas_codigo_barras.png"

    if CriarGraficoPizza(pasta_imagens / "pastas_codigo_pizza.png", pastas_codigo):
        imagens["Pizza das pastas principais"] = "imagens/pastas_codigo_pizza.png"

    if CriarGraficoCrescimento(pasta_imagens / "crescimento_arquivos_py.png", historico, "arquivos_py", "Crescimento de arquivos .py", "Arquivos .py"):
        imagens["Crescimento de arquivos Python"] = "imagens/crescimento_arquivos_py.png"

    if CriarGraficoCrescimento(pasta_imagens / "crescimento_linhas_py.png", historico, "linhas_py", "Crescimento de linhas .py", "Linhas .py"):
        imagens["Crescimento de linhas Python"] = "imagens/crescimento_linhas_py.png"

    if CriarGraficoCrescimento(pasta_imagens / "crescimento_commits.png", historico, "commits", "Crescimento de commits", "Commits"):
        imagens["Crescimento de commits"] = "imagens/crescimento_commits.png"

    dados["imagens"] = imagens

    (pasta / "dados.json").write_text(json.dumps(dados, indent=4, ensure_ascii=False), encoding="utf-8")
    markdown = CriarMarkdown(dados, imagens)
    (pasta / "relatorio.md").write_text(markdown, encoding="utf-8")

    prefixo_registro = f"Documentação/Relatorios/{nome}/"
    markdown_raiz = CriarMarkdown(dados, imagens, prefixo_registro)
    (RAIZ / "Registro.md").write_text(markdown_raiz, encoding="utf-8")

    return pasta


GerarRelatorio()
