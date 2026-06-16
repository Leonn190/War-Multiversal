import pygame
from Codigo.Prefabs.Tela import Tela
from Codigo.Prefabs.Botao import Botao
from Codigo.Prefabs.Texto import Texto
from Codigo.Prefabs.Universos import CampoUniversos


class TelaInicial(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)
        self.Tempo = 0
        self.Titulo = Texto("WAR MULTIVERSAL", tamanho=84, cor=(248, 250, 255), negrito=True)
        self.Subtitulo = Texto("Domine territórios. Planeje turnos. Quebre universos.", tamanho=30, cor=(171, 184, 230))
        self.Aviso = Texto("", tamanho=24, cor=(200, 212, 255), negrito=True)
        self.TempoAviso = 0
        self.CampoUniversos = CampoUniversos(quantidade=15, seed=777)
        self.CriarBotoes()

    def CriarBotoes(self):
        estilo_principal = {
            "fundo": (31, 43, 89),
            "fundo_hover": (59, 82, 168),
            "fundo_press": (20, 28, 64),
            "borda": (102, 141, 255),
            "borda_hover": (196, 211, 255),
            "tamanho_texto": 32,
            "raio": 24,
            "crescimento_hover": 1.06,
            "offset_sombra": 9,
            "offset_sombra_hover": 14,
        }
        estilo_secundario = {
            **estilo_principal,
            "fundo": (37, 34, 77),
            "fundo_hover": (87, 65, 156),
            "borda": (160, 128, 255),
            "borda_hover": (218, 198, 255),
        }
        estilo_config = {
            **estilo_principal,
            "fundo": (29, 60, 75),
            "fundo_hover": (42, 104, 126),
            "borda": (104, 215, 255),
            "borda_hover": (185, 238, 255),
        }
        estilo_sair = {
            **estilo_principal,
            "fundo": (73, 32, 47),
            "fundo_hover": (128, 43, 65),
            "fundo_press": (54, 22, 34),
            "borda": (245, 106, 136),
            "borda_hover": (255, 180, 194),
        }

        self.BotaoRanqueado = Botao((710, 535, 500, 86), "Ranqueado", self.AbrirRanqueado, estilo_principal)
        self.BotaoCustomizado = Botao((710, 645, 500, 86), "Customizado", self.AbrirCustomizado, estilo_secundario)
        self.BotaoConfiguracoes = Botao((710, 755, 500, 86), "Configurações", self.AbrirConfiguracoes, estilo_config)
        self.BotaoSair = Botao((710, 865, 500, 86), "Sair", self.Controlador.Encerrar, estilo_sair)
        self.Botoes = [self.BotaoRanqueado, self.BotaoCustomizado, self.BotaoConfiguracoes, self.BotaoSair]

    def AbrirRanqueado(self):
        self.DefinirAviso("Ranqueado ainda não foi ligado ao servidor de partidas.")

    def AbrirCustomizado(self):
        self.DefinirAviso("Customizado ainda não foi ligado à criação de sala.")

    def AbrirConfiguracoes(self):
        self.Controlador.DefinirTela("TelaConfiguracoes")

    def DefinirAviso(self, texto):
        self.Aviso.DefinirTexto(texto)
        self.TempoAviso = 3.0

    def Atualizar(self, dt):
        self.Tempo += dt
        self.CampoUniversos.Atualizar(dt)
        if self.TempoAviso > 0:
            self.TempoAviso = max(0, self.TempoAviso - dt)
        super().Atualizar(dt)

    def DesenharFundo(self, tela):
        largura, altura = tela.get_size()
        tela.fill((5, 7, 18))

        for y in range(0, altura, 54):
            intensidade = 12 + int(20 * (y / max(1, altura)))
            pygame.draw.line(tela, (intensidade, intensidade + 5, intensidade + 20), (0, y), (largura, y), 1)

        deslocamento = int((self.Tempo * 18) % 96)
        for x in range(-96, largura + 96, 96):
            pygame.draw.line(tela, (13, 19, 44), (x + deslocamento, 0), (x + deslocamento - 230, altura), 1)

        self.CampoUniversos.Desenhar(tela)

        camada = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.circle(camada, (30, 44, 116, 128), (int(largura * 0.14), int(altura * 0.2)), int(min(largura, altura) * 0.28))
        pygame.draw.circle(camada, (91, 44, 132, 92), (int(largura * 0.86), int(altura * 0.78)), int(min(largura, altura) * 0.32))
        pygame.draw.rect(camada, (0, 0, 0, 70), (0, 0, largura, altura))
        tela.blit(camada, (0, 0))

    def DesenharPainelCentral(self, tela):
        painel = pygame.Rect(610, 480, 700, 520)
        pygame.draw.rect(tela, (10, 13, 31, 190), painel.move(0, 14), border_radius=36)
        pygame.draw.rect(tela, (14, 18, 42, 185), painel, border_radius=36)
        pygame.draw.rect(tela, (94, 120, 240, 125), painel, 2, border_radius=36)
        pygame.draw.rect(tela, (255, 255, 255, 18), painel.inflate(-12, -12), 1, border_radius=30)

    def Desenhar(self, tela):
        layout = self.Controlador.Layout
        self.DesenharFundo(tela)
        self.DesenharPainelCentral(tela)

        self.Titulo.Desenhar(tela, (layout.X(960), layout.Y(275)))
        self.Subtitulo.Desenhar(tela, (layout.X(960), layout.Y(372)))

        for botao in self.Botoes:
            botao.Desenhar(tela)

        if self.TempoAviso > 0:
            alpha = int(255 * min(1, self.TempoAviso / 0.35)) if self.TempoAviso < 0.35 else 255
            caixa = pygame.Surface((740, 54), pygame.SRCALPHA)
            pygame.draw.rect(caixa, (18, 25, 58, min(210, alpha)), (0, 0, 740, 54), border_radius=18)
            pygame.draw.rect(caixa, (130, 158, 255, min(180, alpha)), (0, 0, 740, 54), 2, border_radius=18)
            tela.blit(caixa, (layout.X(590), layout.Y(982)))
            self.Aviso.DefinirCor((200, 212, 255))
            self.Aviso.Desenhar(tela, (layout.X(960), layout.Y(1009)))
