import pygame


class Texto:
    Fontes = {}

    def __init__(self, texto, tamanho=32, cor=(245, 246, 255), fonte=None, negrito=False, centralizado=True):
        self.Texto = texto
        self.Tamanho = tamanho
        self.Cor = cor
        self.FonteNome = fonte
        self.Negrito = negrito
        self.Centralizado = centralizado
        self.Superficie = None
        self.Rect = None
        self.AtualizarSuperficie()

    def PegarFonte(self):
        chave = (self.FonteNome, self.Tamanho, self.Negrito)

        if chave not in Texto.Fontes:
            fonte = pygame.font.SysFont(self.FonteNome or "segoeui", self.Tamanho, bold=self.Negrito)
            Texto.Fontes[chave] = fonte

        return Texto.Fontes[chave]

    def AtualizarSuperficie(self):
        self.Superficie = self.PegarFonte().render(str(self.Texto), True, self.Cor)
        self.Rect = self.Superficie.get_rect()

    def DefinirTexto(self, texto):
        if self.Texto == texto:
            return

        self.Texto = texto
        self.AtualizarSuperficie()

    def DefinirCor(self, cor):
        if self.Cor == cor:
            return

        self.Cor = cor
        self.AtualizarSuperficie()

    def Desenhar(self, tela, posicao):
        if self.Centralizado:
            self.Rect.center = posicao
        else:
            self.Rect.topleft = posicao

        tela.blit(self.Superficie, self.Rect)
