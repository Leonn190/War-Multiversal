import pygame
from Codigo.Prefabs.Texto import Texto


class Mensagem:
    def __init__(self, texto, duracao=2.7, largura=760, altura=58):
        self.Texto = Texto(texto, tamanho=24, cor=(214, 224, 255), negrito=True)
        self.Duracao = duracao
        self.Tempo = 0
        self.Largura = largura
        self.Altura = altura
        self.YInicial = 94
        self.VelocidadeSubida = 62

    def Atualizar(self, dt):
        self.Tempo += dt

    def Acabou(self):
        return self.Tempo >= self.Duracao

    def Alpha(self):
        if self.Tempo < 0.18:
            return int(255 * (self.Tempo / 0.18))

        tempo_restante = self.Duracao - self.Tempo
        if tempo_restante < 0.85:
            return int(255 * max(0, tempo_restante / 0.85))

        return 255

    def PosicaoY(self):
        return int(self.YInicial - self.Tempo * self.VelocidadeSubida)

    def Desenhar(self, tela, layout, deslocamento=0):
        alpha = max(0, min(255, self.Alpha()))
        largura = layout.X(self.Largura)
        altura = layout.Y(self.Altura)
        x = int((layout.Largura - largura) / 2)
        y = layout.Y(self.PosicaoY() - deslocamento)

        camada = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.rect(camada, (18, 25, 58, min(210, alpha)), (0, 0, largura, altura), border_radius=18)
        pygame.draw.rect(camada, (130, 158, 255, min(180, alpha)), (0, 0, largura, altura), 2, border_radius=18)
        pygame.draw.rect(camada, (255, 255, 255, min(28, alpha)), (8, 8, largura - 16, altura - 16), 1, border_radius=13)
        self.Texto.Desenhar(camada, (largura // 2, altura // 2))
        camada.set_alpha(alpha)
        tela.blit(camada, (x, y))


class CampoMensagens:
    def __init__(self):
        self.Mensagens = []

    def Adicionar(self, texto, duracao=2.7):
        self.Mensagens.append(Mensagem(texto, duracao=duracao))
        if len(self.Mensagens) > 4:
            self.Mensagens = self.Mensagens[-4:]

    def Atualizar(self, dt):
        for mensagem in self.Mensagens:
            mensagem.Atualizar(dt)
        self.Mensagens = [mensagem for mensagem in self.Mensagens if not mensagem.Acabou()]

    def Desenhar(self, tela, layout):
        for indice, mensagem in enumerate(self.Mensagens):
            mensagem.Desenhar(tela, layout, deslocamento=indice * 66)
