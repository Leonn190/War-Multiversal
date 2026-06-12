import pygame
from Codigo.Prefabs.Texto import Texto


class Botao:
    def __init__(self, rect, texto="", acao=None, style=None):
        self.RectBase = pygame.Rect(rect)
        self.Rect = pygame.Rect(rect)
        self.Acao = acao
        self.MouseEmCima = False
        self.Pressionado = False
        self.Ativo = True
        self.Style = {
            "fundo": (32, 39, 72),
            "fundo_hover": (49, 61, 112),
            "fundo_press": (22, 27, 52),
            "borda": (118, 149, 255),
            "borda_hover": (169, 192, 255),
            "texto": (246, 248, 255),
            "raio": 18,
            "largura_borda": 2,
            "sombra": (0, 0, 0, 85),
            "offset_sombra": 7,
        }

        if style:
            self.Style.update(style)

        self.Texto = Texto(texto, tamanho=self.Style.get("tamanho_texto", 34), cor=self.Style["texto"], negrito=True)

    def AtualizarRect(self, layout):
        self.Rect = pygame.Rect(layout.Rect(self.RectBase.x, self.RectBase.y, self.RectBase.w, self.RectBase.h))

    def Atualizar(self, eventos, mouse_pos):
        self.MouseEmCima = self.Ativo and self.Rect.collidepoint(mouse_pos)
        clicou = False

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.MouseEmCima:
                self.Pressionado = True

            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self.Pressionado and self.MouseEmCima:
                    clicou = True
                self.Pressionado = False

        if clicou and self.Acao:
            self.Acao()

        return clicou

    def Desenhar(self, tela):
        if not self.Ativo:
            fundo = (24, 25, 36)
            borda = (65, 67, 82)
        elif self.Pressionado:
            fundo = self.Style["fundo_press"]
            borda = self.Style["borda_hover"]
        elif self.MouseEmCima:
            fundo = self.Style["fundo_hover"]
            borda = self.Style["borda_hover"]
        else:
            fundo = self.Style["fundo"]
            borda = self.Style["borda"]

        sombra = self.Rect.move(0, self.Style["offset_sombra"])
        pygame.draw.rect(tela, self.Style["sombra"], sombra, border_radius=self.Style["raio"])
        pygame.draw.rect(tela, fundo, self.Rect, border_radius=self.Style["raio"])
        pygame.draw.rect(tela, borda, self.Rect, self.Style["largura_borda"], border_radius=self.Style["raio"])

        self.Texto.Desenhar(tela, self.Rect.center)
