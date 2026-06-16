import pygame
from Codigo.Prefabs.Tela import Tela
from Codigo.Prefabs.Botao import Botao
from Codigo.Prefabs.Texto import Texto
from Codigo.Prefabs.CampoUniversos import CampoUniversos
from Codigo.Prefabs.Painel import Painel


class TelaInicial(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)
        self.Tempo = 0
        self.Titulo = Texto("WAR MULTIVERSAL", tamanho=84, cor=(248, 250, 255), negrito=True)
        self.CampoUniversos = CampoUniversos(quantidade=15, seed=777)
        self.PainelCentral = Painel((610, 480, 700, 520), {
            "fundo": (14, 18, 42, 185),
            "borda": (94, 120, 240, 125),
            "sombra": (10, 13, 31, 190),
            "offset_sombra": 14,
            "raio": 36,
            "padding_borda_interna": 12,
        })
        self.CriarBotoes()

    def CriarBotoes(self):
        estilo_principal = {
            "fundo": (31, 43, 89),
            "fundo_hover": (59, 82, 168),
            "fundo_press": (20, 28, 64),
            "borda": (102, 141, 255),
            "borda_hover": (196, 211, 255),
            "tamanho_texto": 32,
            "raio": 24,
            "crescimento_hover": 1.045,
            "offset_sombra": 9,
            "offset_sombra_hover": 12,
        }
        estilo_secundario = {
            **estilo_principal,
            "fundo": (37, 34, 77),
            "fundo_hover": (87, 65, 156),
            "borda": (160, 128, 255),
            "borda_hover": (218, 198, 255),
        }
        estilo_config = {
            **estilo_principal,
            "fundo": (29, 60, 75),
            "fundo_hover": (42, 104, 126),
            "borda": (104, 215, 255),
            "borda_hover": (185, 238, 255),
        }
        estilo_sair = {
            **estilo_principal,
            "fundo": (73, 32, 47),
            "fundo_hover": (128, 43, 65),
            "fundo_press": (54, 22, 34),
            "borda": (245, 106, 136),
            "borda_hover": (255, 180, 194),
        }

        self.BotaoRanqueado = Botao((710, 535, 500, 86), "Ranqueado", self.AbrirRanqueado, estilo_principal)
        self.BotaoCustomizado = Botao((710, 645, 500, 86), "Customizado", self.AbrirCustomizado, estilo_secundario)
        self.BotaoConfiguracoes = Botao((710, 755, 500, 86), "Configurações", self.AbrirConfiguracoes, estilo_config)
        self.BotaoSair = Botao((710, 865, 500, 86), "Sair", self.Controlador.Encerrar, estilo_sair)
        self.Botoes = [self.BotaoRanqueado, self.BotaoCustomizado, self.BotaoConfiguracoes, self.BotaoSair]

    def Entrar(self):
        self.Controlador.Sonoridades.TocarTema()

    def AbrirRanqueado(self):
        self.Controlador.DefinirTela("TelaRanqueada")

    def AbrirCustomizado(self):
        self.Controlador.DefinirTela("TelaCustomizada")

    def AbrirConfiguracoes(self):
        self.Controlador.DefinirTela("TelaConfiguracoes")

    def Atualizar(self, dt):
        self.Tempo += dt
        largura, altura = self.Controlador.Tela.get_size()
        self.CampoUniversos.Atualizar(dt, largura, altura)
        self.PainelCentral.AtualizarRect(self.Controlador.Layout)
        super().Atualizar(dt)

    def DesenharFundo(self, tela):
        largura, altura = tela.get_size()
        tela.fill((5, 7, 18))

        for y in range(0, altura, 54):
            intensidade = 12 + int(20 * (y / max(1, altura)))
            pygame.draw.line(tela, (intensidade, intensidade + 5, intensidade + 20), (0, y), (largura, y), 1)

        deslocamento = int((self.Tempo * 18) % 96)
        for x in range(-96, largura + 96, 96):
            pygame.draw.line(tela, (13, 19, 44), (x + deslocamento, 0), (x + deslocamento - 230, altura), 1)

        self.CampoUniversos.Desenhar(tela)

        camada = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.circle(camada, (30, 44, 116, 128), (int(largura * 0.14), int(altura * 0.2)), int(min(largura, altura) * 0.28))
        pygame.draw.circle(camada, (91, 44, 132, 92), (int(largura * 0.86), int(altura * 0.78)), int(min(largura, altura) * 0.32))
        pygame.draw.rect(camada, (0, 0, 0, 70), (0, 0, largura, altura))
        tela.blit(camada, (0, 0))

    def Desenhar(self, tela):
        layout = self.Controlador.Layout
        self.DesenharFundo(tela)
        self.PainelCentral.Desenhar(tela)

        self.Titulo.Desenhar(tela, (layout.X(960), layout.Y(305)))

        for botao in self.Botoes:
            botao.Desenhar(tela)
