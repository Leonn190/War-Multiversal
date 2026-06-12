import pygame


def CriarCamadaEscura(tamanho, alpha=150):
    camada = pygame.Surface(tamanho, pygame.SRCALPHA)
    camada.fill((0, 0, 0, alpha))
    return camada


def DesenharEscurecimento(tela, alpha=150):
    tela.blit(CriarCamadaEscura(tela.get_size(), alpha), (0, 0))


def CalcularAlphaFade(tempo, duracao, invertido=False):
    if duracao <= 0:
        return 0 if invertido else 255

    progresso = max(0, min(1, tempo / duracao))
    alpha = int(255 * progresso)

    if invertido:
        alpha = 255 - alpha

    return alpha


class TransicaoTela:
    def __init__(self):
        self.Ativa = False
        self.Tempo = 0
        self.Duracao = 0
        self.Invertida = False
        self.Cor = (0, 0, 0)

    def Iniciar(self, duracao=0.35, invertida=False, cor=(0, 0, 0)):
        self.Ativa = True
        self.Tempo = 0
        self.Duracao = duracao
        self.Invertida = invertida
        self.Cor = cor

    def Atualizar(self, dt):
        if not self.Ativa:
            return

        self.Tempo += dt

        if self.Tempo >= self.Duracao:
            self.Ativa = False

    def Desenhar(self, tela):
        if not self.Ativa:
            return

        alpha = CalcularAlphaFade(self.Tempo, self.Duracao, self.Invertida)
        camada = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        camada.fill((*self.Cor, alpha))
        tela.blit(camada, (0, 0))
