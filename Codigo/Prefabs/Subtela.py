import pygame
from Codigo.Visual.TransicaoTela import DesenharEscurecimento


class Subtela:
    def __init__(self, controlador, rect_base=(560, 260, 800, 560)):
        self.Controlador = controlador
        self.RectBase = pygame.Rect(rect_base)
        self.Rect = pygame.Rect(rect_base)
        self.Botoes = []
        self.Textos = []
        self.EscurecerFundo = True
        self.AlphaFundo = 145
        self.Raio = 24

    def Entrar(self):
        pass

    def Sair(self):
        pass

    def AtualizarRect(self):
        layout = self.Controlador.Layout
        self.Rect = pygame.Rect(layout.Rect(self.RectBase.x, self.RectBase.y, self.RectBase.w, self.RectBase.h))

    def ProcessarEventos(self, eventos):
        pass

    def Atualizar(self, dt):
        self.AtualizarRect()
        mouse_pos = self.Controlador.MousePos

        for botao in self.Botoes:
            botao.AtualizarRect(self.Controlador.Layout)
            botao.Atualizar(self.Controlador.Eventos, mouse_pos)

    def DesenharBase(self, tela):
        if self.EscurecerFundo:
            DesenharEscurecimento(tela, self.AlphaFundo)

        pygame.draw.rect(tela, (15, 18, 34), self.Rect, border_radius=self.Raio)
        pygame.draw.rect(tela, (95, 122, 230), self.Rect, 2, border_radius=self.Raio)

    def Desenhar(self, tela):
        self.DesenharBase(tela)
