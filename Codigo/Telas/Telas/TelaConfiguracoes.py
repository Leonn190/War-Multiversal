import pygame
from Codigo.Prefabs.Tela import Tela
from Codigo.Prefabs.Botao import Botao, BotaoAlavanca
from Codigo.Prefabs.Slider import Slider
from Codigo.Prefabs.Texto import Texto
from Codigo.Prefabs.CampoUniversos import CampoUniversos
from Codigo.Prefabs.Painel import Painel


class TelaConfiguracoes(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)
        self.Tempo = 0
        self.Titulo = Texto("CONFIGURAÇÕES", tamanho=70, cor=(248, 250, 255), negrito=True)
        self.Subtitulo = Texto("Ajustes do cliente visual", tamanho=28, cor=(169, 183, 230))
        self.CampoUniversos = CampoUniversos(quantidade=10, seed=331)
        self.PainelConfiguracoes = Painel((520, 300, 880, 600), {
            "fundo": (13, 18, 42, 220),
            "borda": (93, 132, 250, 155),
            "sombra": (0, 0, 0, 105),
            "offset_sombra": 18,
            "raio": 40,
            "padding_borda_interna": 14,
        })
        self.CriarControles()

    def CriarControles(self):
        estilo_voltar = {
            "fundo": (31, 38, 75),
            "fundo_hover": (55, 69, 132),
            "borda": (126, 150, 255),
            "borda_hover": (202, 213, 255),
            "tamanho_texto": 26,
            "raio": 22,
            "crescimento_hover": 1.035,
        }
        estilo_toggle = {
            "fundo": (29, 51, 76),
            "fundo_hover": (40, 78, 111),
            "borda": (103, 205, 255),
            "borda_hover": (182, 235, 255),
            "raio": 30,
        }

        self.BotaoVoltar = Botao((70, 64, 250, 68), "Voltar", self.Voltar, estilo_voltar)
        self.BotaoFPSVisivel = BotaoAlavanca(
            (730, 728, 460, 78),
            "Mostrar FPS",
            self.Controlador.Config.get("FPS Visivel", True),
            self.AlterarFPSVisivel,
            estilo_toggle,
        )
        self.SliderVolume = Slider(
            (610, 398, 700, 112),
            "Volume",
            self.Controlador.Config.get("Volume", 0.5),
            0,
            1,
            0.01,
            self.AlterarVolume,
            formatador=lambda valor: f"{int(round(valor * 100))}%",
        )
        self.SliderFPS = Slider(
            (610, 558, 700, 112),
            "FPS máximo",
            self.Controlador.Config.get("FPS", 200),
            30,
            240,
            10,
            self.AlterarFPSMaximo,
            formatador=lambda valor: f"{int(valor)} FPS",
        )

        self.Botoes = [self.BotaoVoltar, self.BotaoFPSVisivel]
        self.Sliders = [self.SliderVolume, self.SliderFPS]

    def Entrar(self):
        self.Controlador.Sonoridades.TocarTema()

    def Voltar(self):
        self.Controlador.DefinirTela("TelaInicial")

    def AlterarVolume(self, valor):
        valor = max(0, min(1, float(valor)))
        self.Controlador.Config["Volume"] = valor
        self.Controlador.Config["Mudo"] = valor <= 0
        self.Controlador.SalvarConfiguracoes()

    def AlterarFPSMaximo(self, valor):
        self.Controlador.Config["FPS"] = int(valor)
        self.Controlador.SalvarConfiguracoes()

    def AlterarFPSVisivel(self, valor):
        self.Controlador.Config["FPS Visivel"] = bool(valor)
        self.Controlador.SalvarConfiguracoes()

    def Atualizar(self, dt):
        self.Tempo += dt
        largura, altura = self.Controlador.Tela.get_size()
        self.CampoUniversos.Atualizar(dt, largura, altura)
        self.PainelConfiguracoes.AtualizarRect(self.Controlador.Layout)
        super().Atualizar(dt)

        mouse_pos = self.Controlador.MousePos
        for slider in self.Sliders:
            slider.AtualizarRect(self.Controlador.Layout)
            slider.Atualizar(self.Controlador.Eventos, mouse_pos)

    def DesenharFundo(self, tela):
        largura, altura = tela.get_size()
        tela.fill((5, 8, 19))

        for y in range(0, altura, 48):
            pygame.draw.line(tela, (12, 18, 41), (0, y), (largura, y), 1)

        self.CampoUniversos.Desenhar(tela)

        camada = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.rect(camada, (0, 0, 0, 118), (0, 0, largura, altura))
        pygame.draw.circle(camada, (44, 100, 142, 95), (int(largura * 0.76), int(altura * 0.2)), int(min(largura, altura) * 0.27))
        tela.blit(camada, (0, 0))

    def Desenhar(self, tela):
        layout = self.Controlador.Layout
        self.DesenharFundo(tela)
        self.PainelConfiguracoes.Desenhar(tela)

        self.Titulo.Desenhar(tela, (layout.X(960), layout.Y(205)))
        self.Subtitulo.Desenhar(tela, (layout.X(960), layout.Y(275)))

        for slider in self.Sliders:
            slider.Desenhar(tela)

        for botao in self.Botoes:
            botao.Desenhar(tela)
