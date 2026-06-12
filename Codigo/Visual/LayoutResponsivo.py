class LayoutResponsivo:
    def __init__(self, largura_base=1920, altura_base=1080):
        self.LarguraBase = largura_base
        self.AlturaBase = altura_base
        self.Largura = largura_base
        self.Altura = altura_base
        self.EscalaX = 1
        self.EscalaY = 1
        self.Escala = 1

    def Atualizar(self, tamanho):
        self.Largura, self.Altura = tamanho
        self.EscalaX = self.Largura / self.LarguraBase
        self.EscalaY = self.Altura / self.AlturaBase
        self.Escala = min(self.EscalaX, self.EscalaY)

    def X(self, valor):
        return int(valor * self.EscalaX)

    def Y(self, valor):
        return int(valor * self.EscalaY)

    def V(self, valor):
        return int(valor * self.Escala)

    def Rect(self, x, y, largura, altura):
        return (self.X(x), self.Y(y), self.X(largura), self.Y(altura))

    def CentroX(self, largura=0):
        return int((self.Largura - self.X(largura)) / 2)

    def CentroY(self, altura=0):
        return int((self.Altura - self.Y(altura)) / 2)
