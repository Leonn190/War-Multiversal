import pygame
from Codigo.Prefabs.Texto import Texto


class Botao:
    def __init__(self, rect, texto="", acao=None, style=None):
        self.RectBase = pygame.Rect(rect)
        self.RectLayout = pygame.Rect(rect)
        self.Rect = pygame.Rect(rect)
        self.Acao = acao
        self.MouseEmCima = False
        self.Pressionado = False
        self.Ativo = True
        self.HoverAnim = 0
        self.PressAnim = 0
        self.Style = {
            "fundo": (34, 43, 84),
            "fundo_hover": (55, 72, 138),
            "fundo_press": (22, 28, 58),
            "fundo_desativado": (26, 27, 40),
            "borda": (106, 136, 255),
            "borda_hover": (176, 196, 255),
            "borda_press": (92, 116, 220),
            "borda_desativado": (64, 66, 82),
            "texto": (248, 250, 255),
            "texto_hover": (255, 255, 255),
            "texto_desativado": (128, 132, 150),
            "raio": 20,
            "largura_borda": 2,
            "sombra": (0, 0, 0, 105),
            "sombra_hover": (21, 35, 104, 120),
            "offset_sombra": 8,
            "offset_sombra_hover": 12,
            "crescimento_hover": 1.055,
            "crescimento_press": 0.982,
            "velocidade_hover": 0.18,
            "velocidade_press": 0.28,
            "tamanho_texto": 34,
            "negrito_texto": True,
            "fonte": "segoeui",
            "offset_texto_x": 0,
            "offset_texto_y": 0,
            "brilho": True,
            "brilho_alpha": 34,
            "linha_lateral": True,
        }

        if style:
            self.Style.update(style)

        self.Texto = Texto(
            texto,
            tamanho=self.Style.get("tamanho_texto", 34),
            cor=self.Style["texto"],
            fonte=self.Style.get("fonte"),
            negrito=self.Style.get("negrito_texto", True),
        )

    def DefinirTexto(self, texto):
        self.Texto.DefinirTexto(texto)

    def AtualizarRect(self, layout):
        self.RectLayout = pygame.Rect(layout.Rect(self.RectBase.x, self.RectBase.y, self.RectBase.w, self.RectBase.h))
        self.Rect = self.CriarRectAnimado()

    def Aproximar(self, valor, alvo, velocidade):
        if valor < alvo:
            return min(alvo, valor + velocidade)
        return max(alvo, valor - velocidade)

    def CriarRectAnimado(self):
        escala = 1 + ((self.Style["crescimento_hover"] - 1) * self.HoverAnim)
        escala += ((self.Style["crescimento_press"] - 1) * self.PressAnim)

        largura = max(1, int(self.RectLayout.w * escala))
        altura = max(1, int(self.RectLayout.h * escala))
        rect = pygame.Rect(0, 0, largura, altura)
        rect.center = self.RectLayout.center
        return rect

    def Atualizar(self, eventos, mouse_pos):
        self.MouseEmCima = self.Ativo and self.RectLayout.collidepoint(mouse_pos)
        clicou = False

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.MouseEmCima:
                self.Pressionado = True

            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self.Pressionado and self.MouseEmCima:
                    clicou = True
                self.Pressionado = False

        alvo_hover = 1 if self.MouseEmCima and self.Ativo else 0
        alvo_press = 1 if self.Pressionado and self.Ativo else 0
        self.HoverAnim = self.Aproximar(self.HoverAnim, alvo_hover, self.Style["velocidade_hover"])
        self.PressAnim = self.Aproximar(self.PressAnim, alvo_press, self.Style["velocidade_press"])
        self.Rect = self.CriarRectAnimado()

        if clicou and self.Acao:
            self.Acao()

        return clicou

    def PegarCoresAtuais(self):
        if not self.Ativo:
            return self.Style["fundo_desativado"], self.Style["borda_desativado"], self.Style["texto_desativado"]

        if self.Pressionado:
            return self.Style["fundo_press"], self.Style["borda_press"], self.Style["texto_hover"]

        if self.MouseEmCima:
            return self.Style["fundo_hover"], self.Style["borda_hover"], self.Style["texto_hover"]

        return self.Style["fundo"], self.Style["borda"], self.Style["texto"]

    def DesenharBrilho(self, tela):
        if not self.Style.get("brilho", True):
            return

        altura = max(1, self.Rect.h // 2)
        brilho = pygame.Surface((self.Rect.w, altura), pygame.SRCALPHA)
        alpha = int(self.Style.get("brilho_alpha", 34) * (0.6 + 0.4 * self.HoverAnim))
        pygame.draw.rect(
            brilho,
            (255, 255, 255, alpha),
            (0, 0, self.Rect.w, altura),
            border_radius=self.Style["raio"],
        )
        tela.blit(brilho, self.Rect.topleft)

    def DesenharLinhaLateral(self, tela, borda):
        if not self.Style.get("linha_lateral", True):
            return

        x = self.Rect.x + max(12, self.Rect.h // 5)
        y1 = self.Rect.y + max(14, self.Rect.h // 4)
        y2 = self.Rect.bottom - max(14, self.Rect.h // 4)
        pygame.draw.line(tela, borda, (x, y1), (x, y2), max(2, self.Rect.h // 22))

    def Desenhar(self, tela):
        fundo, borda, cor_texto = self.PegarCoresAtuais()
        sombra_cor = self.Style["sombra_hover"] if self.MouseEmCima else self.Style["sombra"]
        offset_sombra = self.Style["offset_sombra_hover"] if self.MouseEmCima else self.Style["offset_sombra"]
        sombra = self.Rect.move(0, offset_sombra)

        pygame.draw.rect(tela, sombra_cor, sombra, border_radius=self.Style["raio"])
        pygame.draw.rect(tela, fundo, self.Rect, border_radius=self.Style["raio"])
        self.DesenharBrilho(tela)
        pygame.draw.rect(tela, borda, self.Rect, self.Style["largura_borda"], border_radius=self.Style["raio"])
        pygame.draw.rect(tela, (255, 255, 255, 18), self.Rect.inflate(-8, -8), 1, border_radius=max(1, self.Style["raio"] - 5))
        self.DesenharLinhaLateral(tela, borda)

        self.Texto.DefinirCor(cor_texto)
        centro = (
            self.Rect.centerx + self.Style.get("offset_texto_x", 0),
            self.Rect.centery + self.Style.get("offset_texto_y", 0),
        )
        self.Texto.Desenhar(tela, centro)


class BotaoAlavanca(Botao):
    def __init__(self, rect, texto="", valor=False, acao=None, style=None):
        self.Valor = bool(valor)
        self.AcaoMudanca = acao
        estilo = {
            "offset_texto_x": -52,
            "tamanho_texto": 28,
            "crescimento_hover": 1.035,
            "raio": 26,
            "linha_lateral": False,
        }
        if style:
            estilo.update(style)

        super().__init__(rect, texto, self.TrocarValor, estilo)

    def DefinirValor(self, valor, executar_acao=False):
        novo = bool(valor)
        if self.Valor == novo:
            return

        self.Valor = novo
        if executar_acao and self.AcaoMudanca:
            self.AcaoMudanca(self.Valor)

    def TrocarValor(self):
        self.Valor = not self.Valor
        if self.AcaoMudanca:
            self.AcaoMudanca(self.Valor)

    def DesenharAlavanca(self, tela):
        margem = max(10, self.Rect.h // 6)
        largura = max(74, int(self.Rect.w * 0.22))
        altura = max(34, self.Rect.h - margem * 2)
        trilho = pygame.Rect(0, 0, largura, altura)
        trilho.centery = self.Rect.centery
        trilho.right = self.Rect.right - margem - 4

        cor_trilho = (46, 178, 125) if self.Valor else (69, 73, 96)
        cor_borda = (162, 255, 220) if self.Valor else (135, 142, 174)
        pygame.draw.rect(tela, cor_trilho, trilho, border_radius=altura // 2)
        pygame.draw.rect(tela, cor_borda, trilho, 2, border_radius=altura // 2)

        raio = max(12, altura // 2 - 5)
        x_off = trilho.right - altura // 2 if self.Valor else trilho.left + altura // 2
        pygame.draw.circle(tela, (245, 248, 255), (x_off, trilho.centery), raio)
        pygame.draw.circle(tela, (0, 0, 0, 45), (x_off, trilho.centery + 2), raio, 1)

        texto_estado = "ON" if self.Valor else "OFF"
        fonte = Texto(texto_estado, tamanho=max(13, self.Rect.h // 5), cor=(236, 241, 255), negrito=True)
        centro_estado = (trilho.centerx - (altura // 6 if self.Valor else -altura // 6), trilho.centery)
        fonte.Desenhar(tela, centro_estado)

    def Desenhar(self, tela):
        super().Desenhar(tela)
        self.DesenharAlavanca(tela)
