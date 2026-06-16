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
            "sombra": (0, 0, 0, 112),
            "offset_sombra": 9,
            "offset_sombra_hover": 12,
            "crescimento_hover": 1.045,
            "crescimento_press": 0.985,
            "velocidade_hover": 0.16,
            "velocidade_press": 0.25,
            "tamanho_texto": 34,
            "negrito_texto": True,
            "fonte": "segoeui",
            "offset_texto_x": 0,
            "offset_texto_y": 0,
            "brilho": True,
            "brilho_alpha": 32,
            "linha_lateral": True,
            "anel_hover": True,
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

    def MisturarCor(self, a, b, t):
        t = max(0, min(1, t))
        return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

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

        fundo = self.MisturarCor(self.Style["fundo"], self.Style["fundo_hover"], self.HoverAnim)
        borda = self.MisturarCor(self.Style["borda"], self.Style["borda_hover"], self.HoverAnim)
        texto = self.MisturarCor(self.Style["texto"], self.Style["texto_hover"], self.HoverAnim)

        if self.Pressionado:
            fundo = self.MisturarCor(fundo, self.Style["fundo_press"], self.PressAnim)
            borda = self.MisturarCor(borda, self.Style["borda_press"], self.PressAnim)

        return fundo, borda, texto

    def DesenharBrilho(self, tela):
        if not self.Style.get("brilho", True):
            return

        altura = max(1, self.Rect.h // 2)
        brilho = pygame.Surface((self.Rect.w, altura), pygame.SRCALPHA)
        alpha = int(self.Style.get("brilho_alpha", 32) * (0.55 + 0.45 * self.HoverAnim))
        pygame.draw.rect(
            brilho,
            (255, 255, 255, alpha),
            (0, 0, self.Rect.w, altura),
            border_radius=self.Style["raio"],
        )
        tela.blit(brilho, self.Rect.topleft)

    def DesenharAnelHover(self, tela, borda):
        if not self.Style.get("anel_hover", True) or self.HoverAnim <= 0:
            return

        alpha = int(60 * self.HoverAnim)
        anel = pygame.Surface((self.Rect.w + 18, self.Rect.h + 18), pygame.SRCALPHA)
        rect = pygame.Rect(9, 9, self.Rect.w, self.Rect.h)
        pygame.draw.rect(anel, (*borda, alpha), rect.inflate(10, 10), 2, border_radius=self.Style["raio"] + 6)
        tela.blit(anel, (self.Rect.x - 9, self.Rect.y - 9))

    def DesenharLinhaLateral(self, tela, borda):
        if not self.Style.get("linha_lateral", True):
            return

        x = self.Rect.x + max(12, self.Rect.h // 5)
        y1 = self.Rect.y + max(14, self.Rect.h // 4)
        y2 = self.Rect.bottom - max(14, self.Rect.h // 4)
        pygame.draw.line(tela, borda, (x, y1), (x, y2), max(2, self.Rect.h // 22))

    def DesenharCorpo(self, tela):
        fundo, borda, cor_texto = self.PegarCoresAtuais()
        offset_sombra = int(self.Style["offset_sombra"] + (self.Style["offset_sombra_hover"] - self.Style["offset_sombra"]) * self.HoverAnim)
        sombra = self.Rect.move(0, offset_sombra)

        pygame.draw.rect(tela, self.Style["sombra"], sombra, border_radius=self.Style["raio"])
        self.DesenharAnelHover(tela, borda)
        pygame.draw.rect(tela, fundo, self.Rect, border_radius=self.Style["raio"])
        self.DesenharBrilho(tela)
        pygame.draw.rect(tela, borda, self.Rect, self.Style["largura_borda"], border_radius=self.Style["raio"])
        pygame.draw.rect(tela, (255, 255, 255, 18), self.Rect.inflate(-8, -8), 1, border_radius=max(1, self.Style["raio"] - 5))
        self.DesenharLinhaLateral(tela, borda)
        return cor_texto

    def DesenharTexto(self, tela, cor_texto):
        self.Texto.DefinirCor(cor_texto)
        centro = (
            self.Rect.centerx + self.Style.get("offset_texto_x", 0),
            self.Rect.centery + self.Style.get("offset_texto_y", 0),
        )
        self.Texto.Desenhar(tela, centro)

    def Desenhar(self, tela):
        cor_texto = self.DesenharCorpo(tela)
        self.DesenharTexto(tela, cor_texto)


class BotaoAlavanca(Botao):
    def __init__(self, rect, texto="", valor=False, acao=None, style=None):
        self.Valor = bool(valor)
        self.AnimValor = 1 if self.Valor else 0
        self.AcaoMudanca = acao
        estilo = {
            "offset_texto_x": -70,
            "tamanho_texto": 27,
            "crescimento_hover": 1.025,
            "raio": 28,
            "linha_lateral": False,
            "brilho_alpha": 24,
            "mostrar_estado": True,
        }
        if style:
            estilo.update(style)

        super().__init__(rect, texto, self.TrocarValor, estilo)
        self.TextoEstado = Texto("ON" if self.Valor else "OFF", tamanho=17, cor=(245, 248, 255), negrito=True)

    def DefinirValor(self, valor, executar_acao=False):
        novo = bool(valor)
        if self.Valor == novo:
            return

        self.Valor = novo
        if self.Style.get("mostrar_estado", True):
            self.TextoEstado.DefinirTexto("ON" if self.Valor else "OFF")
        if executar_acao and self.AcaoMudanca:
            self.AcaoMudanca(self.Valor)

    def TrocarValor(self):
        self.DefinirValor(not self.Valor, executar_acao=True)

    def Atualizar(self, eventos, mouse_pos):
        clicou = super().Atualizar(eventos, mouse_pos)
        alvo = 1 if self.Valor else 0
        self.AnimValor = self.Aproximar(self.AnimValor, alvo, 0.12)
        return clicou

    def DesenharTexto(self, tela, cor_texto):
        self.Texto.DefinirCor(cor_texto)
        centro = (
            self.Rect.x + int(self.Rect.w * 0.38),
            self.Rect.centery + self.Style.get("offset_texto_y", 0),
        )
        self.Texto.Desenhar(tela, centro)

    def DesenharAlavanca(self, tela):
        margem = max(10, self.Rect.h // 6)
        largura = max(92, int(self.Rect.w * 0.24))
        altura = max(38, self.Rect.h - margem * 2)
        trilho = pygame.Rect(0, 0, largura, altura)
        trilho.centery = self.Rect.centery
        trilho.right = self.Rect.right - margem - 6

        cor_off = (61, 66, 94)
        cor_on = (49, 196, 137)
        cor_borda_off = (128, 138, 176)
        cor_borda_on = (166, 255, 223)
        cor_trilho = self.MisturarCor(cor_off, cor_on, self.AnimValor)
        cor_borda = self.MisturarCor(cor_borda_off, cor_borda_on, self.AnimValor)

        pygame.draw.rect(tela, (0, 0, 0, 62), trilho.move(0, 4), border_radius=altura // 2)
        pygame.draw.rect(tela, cor_trilho, trilho, border_radius=altura // 2)
        pygame.draw.rect(tela, (255, 255, 255, 32), trilho.inflate(-8, -8), 1, border_radius=max(1, altura // 2 - 5))
        pygame.draw.rect(tela, cor_borda, trilho, 2, border_radius=altura // 2)

        raio = max(13, altura // 2 - 6)
        x_off = int((trilho.left + altura // 2) + (trilho.w - altura) * self.AnimValor)
        pygame.draw.circle(tela, (0, 0, 0, 58), (x_off, trilho.centery + 3), raio)
        pygame.draw.circle(tela, (247, 249, 255), (x_off, trilho.centery), raio)
        pygame.draw.circle(tela, cor_borda, (x_off, trilho.centery), raio, 2)
        pygame.draw.circle(tela, (255, 255, 255, 90), (x_off - raio // 3, trilho.centery - raio // 3), max(3, raio // 3))

        if self.Style.get("mostrar_estado", True):
            self.TextoEstado.DefinirTexto("ON" if self.Valor else "OFF")
            self.TextoEstado.DefinirCor((236, 241, 255))
            texto_x = trilho.left + int(trilho.w * (0.32 if self.Valor else 0.68))
            self.TextoEstado.Desenhar(tela, (texto_x, trilho.centery))

    def Desenhar(self, tela):
        cor_texto = self.DesenharCorpo(tela)
        self.DesenharTexto(tela, cor_texto)
        self.DesenharAlavanca(tela)


class BotaoSelecaoUniverso(BotaoAlavanca):
    def __init__(self, rect, texto="", valor=False, acao=None, cor_universo=(112, 140, 255), style=None):
        self.CorUniverso = cor_universo
        self.CorUniversoClara = tuple(min(255, c + 58) for c in cor_universo)
        estilo = {
            "fundo": (25, 31, 68),
            "fundo_hover": (40, 53, 106),
            "fundo_press": (18, 23, 52),
            "borda": (72, 88, 160),
            "borda_hover": self.CorUniversoClara,
            "texto": (224, 231, 255),
            "texto_hover": (255, 255, 255),
            "selecionado_fundo": tuple(max(0, int(c * 0.72)) for c in cor_universo),
            "selecionado_hover": tuple(min(255, int(c * 0.9) + 38) for c in cor_universo),
            "selecionado_borda": self.CorUniversoClara,
            "selecionado_texto": (255, 255, 255),
            "offset_texto_x": 0,
            "tamanho_texto": 23,
            "crescimento_hover": 1.035,
            "raio": 24,
            "linha_lateral": False,
            "brilho_alpha": 25,
            "mostrar_estado": False,
            "anel_hover": True,
        }
        if style:
            estilo.update(style)

        super().__init__(rect, texto, valor, acao, estilo)

    def PegarCoresAtuais(self):
        fundo, borda, texto = super().PegarCoresAtuais()
        if not self.Ativo:
            return fundo, borda, texto

        if self.AnimValor > 0:
            fundo = self.MisturarCor(fundo, self.Style["selecionado_fundo"], self.AnimValor)
            borda = self.MisturarCor(borda, self.Style["selecionado_borda"], self.AnimValor)
            texto = self.MisturarCor(texto, self.Style["selecionado_texto"], self.AnimValor)
            fundo = self.MisturarCor(fundo, self.Style["selecionado_hover"], self.HoverAnim * 0.55)
        return fundo, borda, texto

    def DesenharTexto(self, tela, cor_texto):
        self.Texto.DefinirCor(cor_texto)
        self.Texto.Desenhar(tela, self.Rect.center)

    def DesenharAlavanca(self, tela):
        tamanho = max(20, self.Rect.h // 4)
        x = self.Rect.right - tamanho - max(16, self.Rect.w // 18)
        y = self.Rect.y + max(14, self.Rect.h // 6)
        centro = (x + tamanho // 2, y + tamanho // 2)
        raio = tamanho // 2

        cor_base = self.MisturarCor((77, 87, 126), self.CorUniversoClara, self.AnimValor)
        pygame.draw.circle(tela, (0, 0, 0, 70), (centro[0], centro[1] + 3), raio)
        pygame.draw.circle(tela, cor_base, centro, raio)
        pygame.draw.circle(tela, (255, 255, 255, 70), (centro[0] - raio // 3, centro[1] - raio // 3), max(3, raio // 3))

        if self.AnimValor > 0.45:
            alpha = int(255 * min(1, (self.AnimValor - 0.45) / 0.55))
            check = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
            ponto1 = (int(tamanho * 0.26), int(tamanho * 0.54))
            ponto2 = (int(tamanho * 0.43), int(tamanho * 0.70))
            ponto3 = (int(tamanho * 0.76), int(tamanho * 0.31))
            pygame.draw.lines(check, (255, 255, 255, alpha), False, [ponto1, ponto2, ponto3], max(3, tamanho // 7))
            tela.blit(check, (x, y))
