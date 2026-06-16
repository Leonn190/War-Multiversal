import math
import pygame
from Codigo.Prefabs.Tela import Tela
from Codigo.Prefabs.Botao import Botao
from Codigo.Prefabs.Texto import Texto
from Codigo.Prefabs.CampoUniversos import CampoUniversos
from Codigo.Prefabs.Painel import Painel


class TelaFila(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)
        self.Tempo = 0
        self.Titulo = Texto("BUSCANDO JOGADORES", tamanho=70, cor=(248, 250, 255), negrito=True)
        self.Status = Texto("Entrando na fila ranqueada", tamanho=31, cor=(182, 198, 245), negrito=True)
        self.Descricao = Texto("A fila ainda é visual. O matchmaking será ligado depois.", tamanho=25, cor=(154, 168, 218))
        self.UniversosTexto = Texto("", tamanho=22, cor=(137, 152, 204))
        self.EstadoFila = {}
        self.PartidaEncontrada = False
        self.CampoUniversos = CampoUniversos(quantidade=13, seed=714)
        self.PainelFila = Painel((510, 310, 900, 465), {
            "fundo": (13, 18, 42, 220),
            "borda": (93, 132, 250, 155),
            "sombra": (0, 0, 0, 115),
            "offset_sombra": 18,
            "raio": 42,
            "padding_borda_interna": 14,
        })
        self.CriarControles()

    def CriarControles(self):
        estilo_cancelar = {
            "fundo": (73, 32, 47),
            "fundo_hover": (128, 43, 65),
            "fundo_press": (54, 22, 34),
            "borda": (245, 106, 136),
            "borda_hover": (255, 180, 194),
            "tamanho_texto": 30,
            "raio": 24,
            "crescimento_hover": 1.04,
            "linha_lateral": False,
        }
        self.BotaoCancelar = Botao((735, 665, 450, 82), "Cancelar", self.Cancelar, estilo_cancelar)
        self.Botoes = [self.BotaoCancelar]

    def Entrar(self):
        self.Controlador.Sonoridades.TocarTema()
        universos = getattr(self.Controlador, "UniversosRanqueadosSelecionados", [])
        if universos:
            texto = "Universos: " + ", ".join(universos)
        else:
            texto = "Nenhum universo selecionado"
        self.UniversosTexto.DefinirTexto(texto)
        self.EstadoFila = self.Controlador.Comunicacao.EntrarFilaRanqueada(universos)

    def Sair(self):
        if not self.PartidaEncontrada:
            self.Controlador.Comunicacao.SairFilaRanqueada()

    def Cancelar(self):
        self.Controlador.Comunicacao.SairFilaRanqueada()
        self.Controlador.MostrarMensagem("Busca cancelada.")
        self.Controlador.DefinirTela("TelaRanqueada")

    def Atualizar(self, dt):
        self.Tempo += dt
        self.EstadoFila = self.Controlador.Comunicacao.AtualizarFilaRanqueada()
        if self.EstadoFila.get("status") == "partida_encontrada" and not self.PartidaEncontrada:
            self.PartidaEncontrada = True
            self.Controlador.PartidaAtual = self.EstadoFila.get("partida")
            self.Controlador.MostrarMensagem("Partida encontrada.")

        largura, altura = self.Controlador.Tela.get_size()
        self.CampoUniversos.Atualizar(dt, largura, altura)
        self.PainelFila.AtualizarRect(self.Controlador.Layout)
        super().Atualizar(dt)

    def DesenharFundo(self, tela):
        largura, altura = tela.get_size()
        tela.fill((5, 8, 19))
        for y in range(0, altura, 50):
            pygame.draw.line(tela, (12, 18, 41), (0, y), (largura, y), 1)
        self.CampoUniversos.Desenhar(tela)
        camada = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.rect(camada, (0, 0, 0, 112), (0, 0, largura, altura))
        pygame.draw.circle(camada, (44, 100, 142, 86), (int(largura * 0.73), int(altura * 0.22)), int(min(largura, altura) * 0.27))
        tela.blit(camada, (0, 0))

    def DesenharIndicador(self, tela):
        layout = self.Controlador.Layout
        centro_x = layout.X(960)
        centro_y = layout.Y(520)
        raio_caminho = layout.X(84)
        for indice in range(8):
            angulo = self.Tempo * 3.2 + indice * (math.tau / 8)
            x = int(centro_x + math.cos(angulo) * raio_caminho)
            y = int(centro_y + math.sin(angulo) * raio_caminho)
            alpha = 80 + int(150 * (indice + 1) / 8)
            tamanho = max(5, layout.X(8 + indice * 1.3))
            pygame.draw.circle(tela, (122, 162, 255, alpha), (x, y), tamanho)

    def Desenhar(self, tela):
        layout = self.Controlador.Layout
        self.DesenharFundo(tela)
        self.PainelFila.Desenhar(tela)
        self.Titulo.Desenhar(tela, (layout.X(960), layout.Y(230)))
        if self.PartidaEncontrada:
            self.Status.DefinirTexto("Partida iniciada")
            self.Descricao.DefinirTexto("Dados da partida recebidos do servidor")
        elif self.EstadoFila.get("aguardando_melhor_encaixe"):
            restante = self.EstadoFila.get("segundos_restantes", 0)
            self.Status.DefinirTexto(f"Fechando encaixe em {restante}s")
            self.Descricao.DefinirTexto("Procurando uma combinacao melhor de universos")
        else:
            jogadores = self.EstadoFila.get("jogadores_na_fila", 1)
            self.Status.DefinirTexto(f"Na fila: {jogadores}/5" + "." * (int(self.Tempo * 2) % 4))
            self.Descricao.DefinirTexto("Aguardando jogadores compativeis")
        self.Status.Desenhar(tela, (layout.X(960), layout.Y(405)))
        self.DesenharIndicador(tela)
        self.Descricao.Desenhar(tela, (layout.X(960), layout.Y(600)))
        self.UniversosTexto.Desenhar(tela, (layout.X(960), layout.Y(632)))

        for botao in self.Botoes:
            botao.Desenhar(tela)
