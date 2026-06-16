import pygame
from Codigo.Prefabs.Tela import Tela
from Codigo.Prefabs.Botao import Botao, BotaoSelecaoUniverso
from Codigo.Prefabs.Texto import Texto
from Codigo.Prefabs.CampoUniversos import CampoUniversos
from Codigo.Prefabs.Painel import Painel


class TelaRanqueada(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)
        self.Tempo = 0
        self.Titulo = Texto("RANQUEADA", tamanho=72, cor=(248, 250, 255), negrito=True)
        self.Subtitulo = Texto("Escolha os universos que podem aparecer na partida", tamanho=27, cor=(172, 186, 235))
        self.Aviso = Texto("Selecione pelo menos 2 universos com 40 personagens no total", tamanho=23, cor=(150, 164, 210))
        self.CampoUniversos = CampoUniversos(quantidade=14, seed=910)
        self.PainelUniversos = Painel((160, 270, 1600, 610), {
            "fundo": (13, 18, 42, 218),
            "borda": (94, 120, 240, 145),
            "sombra": (0, 0, 0, 115),
            "offset_sombra": 18,
            "raio": 42,
            "padding_borda_interna": 14,
        })
        self.Universos = [
            ("Marvel", (220, 62, 77)),
            ("DC", (62, 119, 232)),
            ("The Boys", (216, 66, 51)),
            ("Invencível", (244, 211, 74)),
            ("League Of Legends", (88, 181, 218)),
            ("Overwatch", (239, 151, 58)),
            ("One Piece", (80, 171, 245)),
            ("My Hero Academia", (72, 206, 130)),
            ("Pokemon", (246, 203, 65)),
            ("Gerais", (166, 116, 246)),
        ]
        self.Selecionados = set(self.Controlador.Config.get("Universos Ranqueados", []))
        self.CriarControles()

    def CriarControles(self):
        estilo_voltar = {
            "fundo": (31, 38, 75),
            "fundo_hover": (55, 69, 132),
            "borda": (126, 150, 255),
            "borda_hover": (202, 213, 255),
            "tamanho_texto": 26,
            "raio": 22,
            "crescimento_hover": 1.035,
        }
        estilo_jogar = {
            "fundo": (33, 86, 71),
            "fundo_hover": (48, 151, 111),
            "fundo_press": (22, 66, 52),
            "borda": (99, 237, 179),
            "borda_hover": (184, 255, 222),
            "tamanho_texto": 32,
            "raio": 26,
            "crescimento_hover": 1.045,
            "linha_lateral": False,
        }
        estilo_universo = {
            "offset_sombra": 8,
            "offset_sombra_hover": 10,
        }

        self.BotaoVoltar = Botao((70, 64, 250, 68), "Voltar", self.Voltar, estilo_voltar)
        self.BotaoJogar = Botao((710, 770, 500, 86), "Jogar", self.Jogar, estilo_jogar)
        self.BotoesUniverso = []

        largura = 270
        altura = 98
        espaco_x = 28
        espaco_y = 124
        inicio_x = 229
        inicio_y = 404

        for indice, (nome, cor) in enumerate(self.Universos):
            coluna = indice % 5
            linha = indice // 5
            x = inicio_x + coluna * (largura + espaco_x)
            y = inicio_y + linha * espaco_y
            botao = BotaoSelecaoUniverso(
                (x, y, largura, altura),
                nome,
                nome in self.Selecionados,
                lambda valor, nome=nome: self.AlterarUniverso(nome, valor),
                cor,
                estilo_universo,
            )
            self.BotoesUniverso.append(botao)

        self.Botoes = [self.BotaoVoltar] + self.BotoesUniverso + [self.BotaoJogar]

    def Entrar(self):
        self.Controlador.Sonoridades.TocarTema()

    def Voltar(self):
        self.Controlador.DefinirTela("TelaInicial")

    def AlterarUniverso(self, nome, ativo):
        if ativo:
            self.Selecionados.add(nome)
        elif nome in self.Selecionados:
            self.Selecionados.remove(nome)
        self.Controlador.Config["Universos Ranqueados"] = list(self.Selecionados)
        self.Controlador.SalvarConfiguracoes()

    def Jogar(self):
        if len(self.Selecionados) < 2:
            self.Controlador.MostrarMensagem("Selecione pelo menos 2 universos para buscar partida.")
            return

        quantidade_personagens = self.Controlador.Comunicacao.ContarPersonagensUniversos(self.Selecionados)
        if quantidade_personagens < 40:
            self.Controlador.MostrarMensagem("Os universos selecionados precisam somar pelo menos 40 personagens.")
            return

        self.Controlador.UniversosRanqueadosSelecionados = list(self.Selecionados)
        self.Controlador.DefinirTela("TelaFila")

    def Atualizar(self, dt):
        self.Tempo += dt
        largura, altura = self.Controlador.Tela.get_size()
        self.CampoUniversos.Atualizar(dt, largura, altura)
        self.PainelUniversos.AtualizarRect(self.Controlador.Layout)
        super().Atualizar(dt)

    def DesenharFundo(self, tela):
        largura, altura = tela.get_size()
        tela.fill((5, 7, 18))

        for y in range(0, altura, 54):
            intensidade = 11 + int(18 * (y / max(1, altura)))
            pygame.draw.line(tela, (intensidade, intensidade + 5, intensidade + 20), (0, y), (largura, y), 1)

        deslocamento = int((self.Tempo * 16) % 104)
        for x in range(-104, largura + 104, 104):
            pygame.draw.line(tela, (13, 19, 44), (x + deslocamento, 0), (x + deslocamento - 230, altura), 1)

        self.CampoUniversos.Desenhar(tela)
        camada = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.circle(camada, (34, 57, 139, 110), (int(largura * 0.14), int(altura * 0.18)), int(min(largura, altura) * 0.25))
        pygame.draw.circle(camada, (83, 44, 132, 92), (int(largura * 0.86), int(altura * 0.76)), int(min(largura, altura) * 0.32))
        pygame.draw.rect(camada, (0, 0, 0, 82), (0, 0, largura, altura))
        tela.blit(camada, (0, 0))

    def Desenhar(self, tela):
        layout = self.Controlador.Layout
        self.DesenharFundo(tela)
        self.PainelUniversos.Desenhar(tela)
        self.Titulo.Desenhar(tela, (layout.X(960), layout.Y(178)))
        self.Subtitulo.Desenhar(tela, (layout.X(960), layout.Y(244)))
        self.Aviso.Desenhar(tela, (layout.X(960), layout.Y(682)))

        for botao in self.Botoes:
            botao.Desenhar(tela)
