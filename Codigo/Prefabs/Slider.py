import pygame
from Codigo.Prefabs.Texto import Texto


class Slider:
    def __init__(self, rect, texto="", valor=0, minimo=0, maximo=1, passo=0.01, acao=None, style=None, formatador=None):
        self.RectBase = pygame.Rect(rect)
        self.Rect = pygame.Rect(rect)
        self.TrackRect = pygame.Rect(rect)
        self.KnobPos = 0
        self.TextoLabel = Texto(texto, tamanho=28, cor=(238, 242, 255), negrito=True, centralizado=False)
        self.TextoValor = Texto("", tamanho=24, cor=(175, 188, 230), negrito=True)
        self.Minimo = minimo
        self.Maximo = maximo
        self.Passo = passo
        self.Acao = acao
        self.Arrastando = False
        self.MouseEmCima = False
        self.Formatador = formatador or self.FormatarValorPadrao
        self.Style = {
            "fundo": (19, 24, 48),
            "borda": (91, 112, 204),
            "trilho": (46, 52, 82),
            "preenchido": (97, 137, 255),
            "preenchido_hover": (132, 166, 255),
            "knob": (247, 249, 255),
            "knob_borda": (154, 177, 255),
            "sombra": (0, 0, 0, 80),
            "raio": 22,
        }
        if style:
            self.Style.update(style)

        self.Valor = self.TratarValor(valor)
        self.AtualizarTextoValor()

    def FormatarValorPadrao(self, valor):
        if self.Maximo <= 1:
            return f"{int(round(valor * 100))}%"
        return str(int(round(valor)))

    def TratarValor(self, valor):
        valor = max(self.Minimo, min(self.Maximo, valor))
        if self.Passo:
            passos = round((valor - self.Minimo) / self.Passo)
            valor = self.Minimo + passos * self.Passo
        if isinstance(self.Passo, int) or self.Passo >= 1:
            valor = int(round(valor))
        return valor

    def AtualizarTextoValor(self):
        self.TextoValor.DefinirTexto(self.Formatador(self.Valor))

    def DefinirValor(self, valor, executar_acao=False):
        novo = self.TratarValor(valor)
        if novo == self.Valor:
            return False

        self.Valor = novo
        self.AtualizarTextoValor()
        if executar_acao and self.Acao:
            self.Acao(self.Valor)
        return True

    def Percentual(self):
        if self.Maximo == self.Minimo:
            return 0
        return (self.Valor - self.Minimo) / (self.Maximo - self.Minimo)

    def AtualizarRect(self, layout):
        self.Rect = pygame.Rect(layout.Rect(self.RectBase.x, self.RectBase.y, self.RectBase.w, self.RectBase.h))
        margem_x = max(26, self.Rect.w // 26)
        self.TrackRect = pygame.Rect(
            self.Rect.x + margem_x,
            self.Rect.y + int(self.Rect.h * 0.58),
            self.Rect.w - margem_x * 2,
            max(10, self.Rect.h // 9),
        )
        self.KnobPos = self.TrackRect.x + int(self.TrackRect.w * self.Percentual())

    def DefinirValorPeloMouse(self, mouse_x):
        percentual = (mouse_x - self.TrackRect.x) / max(1, self.TrackRect.w)
        percentual = max(0, min(1, percentual))
        valor = self.Minimo + percentual * (self.Maximo - self.Minimo)
        return self.DefinirValor(valor, executar_acao=True)

    def Atualizar(self, eventos, mouse_pos):
        area_interacao = self.Rect.inflate(0, 12)
        self.MouseEmCima = area_interacao.collidepoint(mouse_pos)
        alterou = False

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.MouseEmCima:
                self.Arrastando = True
                alterou = self.DefinirValorPeloMouse(mouse_pos[0]) or alterou

            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                self.Arrastando = False

            if evento.type == pygame.MOUSEMOTION and self.Arrastando:
                alterou = self.DefinirValorPeloMouse(mouse_pos[0]) or alterou

        if self.Arrastando:
            alterou = self.DefinirValorPeloMouse(mouse_pos[0]) or alterou

        return alterou

    def Desenhar(self, tela):
        sombra = self.Rect.move(0, 8)
        pygame.draw.rect(tela, self.Style["sombra"], sombra, border_radius=self.Style["raio"])
        pygame.draw.rect(tela, self.Style["fundo"], self.Rect, border_radius=self.Style["raio"])
        pygame.draw.rect(tela, self.Style["borda"], self.Rect, 2, border_radius=self.Style["raio"])

        self.TextoLabel.Desenhar(tela, (self.Rect.x + 28, self.Rect.y + 18))
        self.TextoValor.Desenhar(tela, (self.Rect.right - 68, self.Rect.y + 34))

        pygame.draw.rect(tela, self.Style["trilho"], self.TrackRect, border_radius=self.TrackRect.h // 2)
        preenchido = pygame.Rect(self.TrackRect.x, self.TrackRect.y, max(0, self.KnobPos - self.TrackRect.x), self.TrackRect.h)
        cor_preenchido = self.Style["preenchido_hover"] if self.MouseEmCima or self.Arrastando else self.Style["preenchido"]
        pygame.draw.rect(tela, cor_preenchido, preenchido, border_radius=self.TrackRect.h // 2)

        raio_knob = max(15, int(self.Rect.h * 0.18))
        pygame.draw.circle(tela, (0, 0, 0, 90), (self.KnobPos, self.TrackRect.centery + 5), raio_knob)
        pygame.draw.circle(tela, self.Style["knob"], (self.KnobPos, self.TrackRect.centery), raio_knob)
        pygame.draw.circle(tela, self.Style["knob_borda"], (self.KnobPos, self.TrackRect.centery), raio_knob, 3)
