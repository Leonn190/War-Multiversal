import pygame
from Codigo.Prefabs.Tela import Tela
from Codigo.Prefabs.Botao import Botao
from Codigo.Prefabs.Texto import Texto


class TelaInicial(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)
        self.Titulo = Texto("WAR MULTIVERSAL", tamanho=78, cor=(248, 249, 255), negrito=True)
        self.Subtitulo = Texto("Domine territórios. Planeje turnos. Quebre universos.", tamanho=30, cor=(166, 177, 220))
        self.BotaoJogar = Botao((760, 650, 400, 92), "JOGAR")
        self.Botoes = [self.BotaoJogar]

    def Atualizar(self, dt):
        super().Atualizar(dt)

    def DesenharFundo(self, tela):
        largura, altura = tela.get_size()
        tela.fill((7, 8, 18))

        for i in range(0, altura, 48):
            intensidade = 16 + int(30 * (i / max(1, altura)))
            pygame.draw.line(tela, (intensidade, intensidade + 4, intensidade + 18), (0, i), (largura, i), 1)

        pygame.draw.circle(tela, (23, 35, 88), (int(largura * 0.18), int(altura * 0.22)), int(min(largura, altura) * 0.24))
        pygame.draw.circle(tela, (43, 20, 79), (int(largura * 0.82), int(altura * 0.78)), int(min(largura, altura) * 0.28))
        pygame.draw.circle(tela, (9, 11, 24), (int(largura * 0.18), int(altura * 0.22)), int(min(largura, altura) * 0.18))

    def Desenhar(self, tela):
        layout = self.Controlador.Layout
        self.DesenharFundo(tela)
        self.Titulo.Desenhar(tela, (layout.X(960), layout.Y(350)))
        self.Subtitulo.Desenhar(tela, (layout.X(960), layout.Y(445)))

        for botao in self.Botoes:
            botao.Desenhar(tela)
