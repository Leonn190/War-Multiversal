import pygame
from ConfigFixa import SalvarConfig
from Codigo.Visual.PipelineGrafica import PipelineGrafica
from Codigo.Visual.TransicaoTela import TransicaoTela
from Codigo.Visual.LayoutResponsivo import LayoutResponsivo
from Codigo.Telas.Telas.TelaInicial import TelaInicial
from Codigo.Telas.Telas.TelaConfiguracoes import TelaConfiguracoes
from Codigo.Telas.Telas.TelaRanqueada import TelaRanqueada
from Codigo.Telas.Telas.TelaFila import TelaFila
from Codigo.Telas.Telas.TelaCustomizada import TelaCustomizada
from Codigo.Prefabs.Texto import Texto
from Codigo.Prefabs.Mensagem import CampoMensagens
from Codigo.Client.Sonoridades import Sonoridades
from Codigo.Client.Comunicacao import Comunicacao


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
        self.TextoFPS = Texto("", tamanho=22, cor=(190, 205, 255), negrito=True, centralizado=False)
        self.Mensagens = CampoMensagens()
        self.Sonoridades = Sonoridades(config)
        self.Comunicacao = Comunicacao()
        self.PartidaAtual = None
        self.UniversosRanqueadosSelecionados = list(config.get("Universos Ranqueados", []))
        self.Telas = {
            "TelaInicial": TelaInicial,
            "TelaConfiguracoes": TelaConfiguracoes,
            "TelaRanqueada": TelaRanqueada,
            "TelaFila": TelaFila,
            "TelaCustomizada": TelaCustomizada,
        }

    def DefinirTela(self, nome):
        if nome not in self.Telas:
            return

        if self.TelaAtual:
            self.TelaAtual.Sair()

        self.NomeTelaAtual = nome
        self.TelaAtual = self.Telas[nome](self)
        self.TelaAtual.Entrar()
        self.Subtelas.clear()
        self.Transicao.Iniciar(0.35, invertida=True)

        if nome in ("TelaInicial", "TelaConfiguracoes", "TelaRanqueada", "TelaFila", "TelaCustomizada"):
            self.Sonoridades.TocarTema()

    def AbrirSubtela(self, subtela):
        self.Subtelas.append(subtela)
        subtela.Entrar()

    def FecharSubtela(self):
        if not self.Subtelas:
            return

        subtela = self.Subtelas.pop()
        subtela.Sair()

    def MostrarMensagem(self, texto, duracao=2.7):
        self.Mensagens.Adicionar(texto, duracao)

    def SalvarConfiguracoes(self):
        SalvarConfig(self.Config)
        self.Sonoridades.AplicarVolume()

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
                    elif self.NomeTelaAtual != "TelaInicial":
                        self.DefinirTela("TelaInicial")
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

        self.Mensagens.Atualizar(dt)
        self.Transicao.Atualizar(dt)

    def DesenharFPS(self):
        if not self.Config.get("FPS Visivel", True):
            return

        fps = int(self.Relogio.get_fps())
        self.TextoFPS.DefinirTexto(f"FPS: {fps}")
        self.TextoFPS.DefinirCor((190, 205, 255))
        x = self.Layout.Largura - self.TextoFPS.Rect.w - self.Layout.X(24)
        y = self.Layout.Y(18)
        self.TextoFPS.Desenhar(self.Tela, (x, y))

    def Desenhar(self):
        self.Pipeline.IniciarFrame()

        if self.TelaAtual:
            self.TelaAtual.Desenhar(self.Tela)

        for subtela in self.Subtelas:
            subtela.Desenhar(self.Tela)

        self.Mensagens.Desenhar(self.Tela, self.Layout)
        self.DesenharFPS()
        self.Transicao.Desenhar(self.Tela)
        self.Pipeline.Aplicar()

    def Rodar(self):
        while self.Rodando:
            fps = int(self.Config.get("FPS", 60))
            if fps <= 0:
                fps = 60

            dt = self.Relogio.tick(fps) / 1000
            self.ProcessarEventos()
            self.Atualizar(dt)
            self.Desenhar()

    def Encerrar(self):
        self.SalvarConfiguracoes()
        self.Rodando = False

    def encerrar(self):
        self.Encerrar()

    def abrir_subtela(self, subtela):
        self.AbrirSubtela(subtela)

    def fechar_subtela(self):
        self.FecharSubtela()
