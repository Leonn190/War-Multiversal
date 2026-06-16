import pygame


class Painel:
    def __init__(self, rect, style=None):
        self.RectBase = pygame.Rect(rect)
        self.Rect = pygame.Rect(rect)
        self.Style = {
            "fundo": (13, 18, 42, 210),
            "borda": (93, 132, 250, 150),
            "borda_interna": (255, 255, 255, 18),
            "sombra": (0, 0, 0, 105),
            "offset_sombra": 16,
            "raio": 40,
            "largura_borda": 2,
            "padding_borda_interna": 14,
        }
        if style:
            self.Style.update(style)

    def AtualizarRect(self, layout):
        self.Rect = pygame.Rect(layout.Rect(self.RectBase.x, self.RectBase.y, self.RectBase.w, self.RectBase.h))

    def Desenhar(self, tela):
        raio = self.Style["raio"]
        sombra = self.Rect.move(0, self.Style["offset_sombra"])
        pygame.draw.rect(tela, self.Style["sombra"], sombra, border_radius=raio)
        pygame.draw.rect(tela, self.Style["fundo"], self.Rect, border_radius=raio)
        pygame.draw.rect(tela, self.Style["borda"], self.Rect, self.Style["largura_borda"], border_radius=raio)

        padding = self.Style.get("padding_borda_interna", 14)
        if padding > 0:
            pygame.draw.rect(
                tela,
                self.Style["borda_interna"],
                self.Rect.inflate(-padding, -padding),
                1,
                border_radius=max(1, raio - padding // 2),
            )
