import random
from Codigo.Prefabs.Universo import Universo


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

    def Atualizar(self, dt, largura=None, altura=None):
        largura = largura or self.LarguraBase
        altura = altura or self.AlturaBase
        for universo in self.Universos:
            universo.Atualizar(dt, largura, altura)

    def Desenhar(self, tela):
        for universo in self.Universos:
            universo.Desenhar(tela)
