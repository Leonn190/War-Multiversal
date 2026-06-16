import pygame
from Codigo.Prefabs.Tela import Tela
from Codigo.Prefabs.Botao import Botao
from Codigo.Prefabs.Texto import Texto
from Codigo.Prefabs.CampoUniversos import CampoUniversos
from Codigo.Prefabs.Painel import Painel


class TelaCustomizada(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)
        self.Tempo = 0
        self.Titulo = Texto("CUSTOMIZADA", tamanho=72, cor=(248, 250, 255), negrito=True)
        self.Subtitulo = Texto("Essa tela vai virar a criação de sala customizada depois", tamanho=28, cor=(172, 186, 235))
        self.CampoUniversos = CampoUniversos(quantidade=12, seed=512)
        self.PainelCustomizada = Painel((510, 335, 900, 390), {
            "fundo": (13, 18, 42, 220),
            "borda": (160, 128, 255, 150),
            "sombra": (0, 0, 0, 115),
            "offset_sombra": 18,
            "raio": 42,
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
        self.BotaoVoltar = Botao((70, 64, 250, 68), "Voltar", self.Voltar, estilo_voltar)
        self.Botoes = [self.BotaoVoltar]

    def Entrar(self):
        self.Controlador.Sonoridades.TocarTema()

    def Voltar(self):
        self.Controlador.DefinirTela("TelaInicial")

    def Atualizar(self, dt):
        self.Tempo += dt
        largura, altura = self.Controlador.Tela.get_size()
        self.CampoUniversos.Atualizar(dt, largura, altura)
        self.PainelCustomizada.AtualizarRect(self.Controlador.Layout)
        super().Atualizar(dt)

    def DesenharFundo(self, tela):
        largura, altura = tela.get_size()
        tela.fill((5, 7, 18))
        for y in range(0, altura, 54):
            pygame.draw.line(tela, (13, 17, 42), (0, y), (largura, y), 1)
        self.CampoUniversos.Desenhar(tela)
        camada = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.circle(camada, (91, 44, 132, 88), (int(largura * 0.76), int(altura * 0.76)), int(min(largura, altura) * 0.32))
        pygame.draw.rect(camada, (0, 0, 0, 105), (0, 0, largura, altura))
        tela.blit(camada, (0, 0))

    def Desenhar(self, tela):
        layout = self.Controlador.Layout
        self.DesenharFundo(tela)
        self.PainelCustomizada.Desenhar(tela)
        self.Titulo.Desenhar(tela, (layout.X(960), layout.Y(230)))
        self.Subtitulo.Desenhar(tela, (layout.X(960), layout.Y(500)))

        for botao in self.Botoes:
            botao.Desenhar(tela)
