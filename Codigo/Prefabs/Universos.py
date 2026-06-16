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

    def Atualizar(self, dt, largura):
        self.X -= self.Velocidade * dt
        self.Pulso += dt * 1.35

        if self.X < -self.Raio * 3:
            self.X = largura + self.Raio * 3 + random.randint(0, 360)
            self.Y += random.randint(-120, 120)
            if self.Y < 90:
                self.Y = 90
            if self.Y > 990:
                self.Y = 990

    def Desenhar(self, tela):
        import math

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


class CampoUniversos:
    def __init__(self, quantidade=12, largura_base=1920, altura_base=1080, seed=190):
        self.Quantidade = quantidade
        self.LarguraBase = largura_base
        self.AlturaBase = altura_base
        self.Seed = seed
        self.Universos = []
        self.CriarUniversos()

    def CriarUniversos(self):
        random.seed(self.Seed)
        cores = [
            (90, 131, 255),
            (186, 97, 255),
            (84, 221, 172),
            (255, 154, 91),
            (255, 92, 130),
            (92, 213, 255),
            (232, 220, 105),
        ]

        self.Universos.clear()
        for i in range(self.Quantidade):
            x = random.randint(0, self.LarguraBase + 900)
            y = random.randint(120, self.AlturaBase - 120)
            raio = random.randint(26, 82)
            velocidade = random.randint(28, 105)
            cor = cores[i % len(cores)]
            borda = tuple(min(255, c + random.randint(18, 54)) for c in cor)
            self.Universos.append(Universo(x, y, raio, velocidade, cor, borda))

    def Atualizar(self, dt, largura=None):
        largura = largura or self.LarguraBase
        for universo in self.Universos:
            universo.Atualizar(dt, largura)

    def Desenhar(self, tela):
        for universo in self.Universos:
            universo.Desenhar(tela)
