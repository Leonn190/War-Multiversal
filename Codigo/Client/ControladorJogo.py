import pygame
from Codigo.Visual.PipelineGrafica import PipelineGrafica
from Codigo.Visual.TransicaoTela import TransicaoTela
from Codigo.Visual.LayoutResponsivo import LayoutResponsivo
from Codigo.Telas.Telas.TelaInicial import TelaInicial


class ControladorJogo:
    def __init__(self, tela, relogio, config, tela_display=None, janela_opengl=False):
        self.Tela = tela
        self.TelaDisplay = tela_display or pygame.display.get_surface()
        self.Relogio = relogio
        self.Config = config
        self.JanelaOpenGL = janela_opengl
        self.Rodando = True
        self.Eventos = []
        self.MousePos = (0, 0)
        self.TelaAtual = None
        self.NomeTelaAtual = None
        self.Subtelas = []
        self.Layout = LayoutResponsivo(config.get("LarguraBase", 1920), config.get("AlturaBase", 1080))
        self.Layout.Atualizar(self.Tela.get_size())
        self.Pipeline = PipelineGrafica(self.Tela, self.TelaDisplay, janela_opengl, config)
        self.Transicao = TransicaoTela()
        self.Telas = {
            "TelaInicial": TelaInicial,
        }

    def DefinirTela(self, nome):
        if self.TelaAtual:
            self.TelaAtual.Sair()

        self.NomeTelaAtual = nome
        self.TelaAtual = self.Telas[nome](self)
        self.TelaAtual.Entrar()
        self.Subtelas.clear()
        self.Transicao.Iniciar(0.35, invertida=True)

    def AbrirSubtela(self, subtela):
        self.Subtelas.append(subtela)
        subtela.Entrar()

    def FecharSubtela(self):
        if not self.Subtelas:
            return

        subtela = self.Subtelas.pop()
        subtela.Sair()

    def ProcessarEventos(self):
        self.Eventos = pygame.event.get()
        self.MousePos = pygame.mouse.get_pos()

        for evento in self.Eventos:
            if evento.type == pygame.QUIT:
                self.Rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if self.Subtelas:
                        self.FecharSubtela()
                    else:
                        self.Rodando = False

        if self.Subtelas:
            self.Subtelas[-1].ProcessarEventos(self.Eventos)
        elif self.TelaAtual:
            self.TelaAtual.ProcessarEventos(self.Eventos)

    def Atualizar(self, dt):
        self.Layout.Atualizar(self.Tela.get_size())

        if self.TelaAtual:
            self.TelaAtual.Atualizar(dt)

        for subtela in self.Subtelas:
            subtela.Atualizar(dt)

        self.Transicao.Atualizar(dt)

    def Desenhar(self):
        self.Pipeline.IniciarFrame()

        if self.TelaAtual:
            self.TelaAtual.Desenhar(self.Tela)

        for subtela in self.Subtelas:
            subtela.Desenhar(self.Tela)

        self.Transicao.Desenhar(self.Tela)
        self.Pipeline.Aplicar()

    def Rodar(self):
        while self.Rodando:
            dt = self.Relogio.tick(self.Config.get("FPS", 60)) / 1000
            self.ProcessarEventos()
            self.Atualizar(dt)
            self.Desenhar()

    def Encerrar(self):
        pass
