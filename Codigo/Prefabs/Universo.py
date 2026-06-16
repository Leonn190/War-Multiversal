import math
import random
import pygame


class Universo:
    def __init__(self, x, y, raio, velocidade, cor, cor_borda=None, brilho=70):
        self.X = float(x)
        self.Y = float(y)
        self.Raio = int(raio)
        self.Velocidade = float(velocidade)
        self.Cor = cor
        self.CorBorda = cor_borda or tuple(min(255, c + 50) for c in cor)
        self.Brilho = brilho
        self.Pulso = random.uniform(0, 6.28)

    def Atualizar(self, dt, largura, altura=1080):
        self.X -= self.Velocidade * dt
        self.Pulso += dt * 1.35

        if self.X < -self.Raio * 3:
            self.X = largura + self.Raio * 3 + random.randint(0, 360)
            self.Y += random.randint(-120, 120)
            self.Y = max(90, min(altura - 90, self.Y))

    def Desenhar(self, tela):
        raio_pulso = self.Raio + int(math.sin(self.Pulso) * max(2, self.Raio * 0.06))
        tamanho = raio_pulso * 4
        camada = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        centro = (tamanho // 2, tamanho // 2)

        pygame.draw.circle(camada, (*self.Cor, 18), centro, raio_pulso * 2)
        pygame.draw.circle(camada, (*self.Cor, self.Brilho), centro, int(raio_pulso * 1.38))
        pygame.draw.circle(camada, (*self.Cor, 210), centro, raio_pulso)
        pygame.draw.circle(camada, (*self.CorBorda, 245), centro, raio_pulso, max(2, raio_pulso // 13))
        pygame.draw.circle(camada, (255, 255, 255, 65), (centro[0] - raio_pulso // 3, centro[1] - raio_pulso // 3), max(3, raio_pulso // 5))

        tela.blit(camada, (int(self.X) - tamanho // 2, int(self.Y) - tamanho // 2))
