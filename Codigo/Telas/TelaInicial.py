"""
Tela inicial do War Multiversal.

Por enquanto ela é propositalmente simples:
- mostra identidade visual inicial;
- testa o sistema de tela;
- testa o sistema de subtela;
- testa botões;
- testa pipeline gráfica;
- testa transição.

Depois essa tela pode ganhar:
- animação de fundo;
- login;
- seleção de campanha;
- multiplayer;
- carregamento de saves.
"""

import math

import pygame

from Prefabs.Botao import Botao
from Prefabs.Subtela import Subtela
from Prefabs.Tela import Tela


class TelaInicial(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)

        self.fonte_titulo = pygame.font.SysFont("arial", 64, bold=True)
        self.fonte_subtitulo = pygame.font.SysFont("arial", 24)
        self.fonte_botao = pygame.font.SysFont("arial", 25, bold=True)
        self.fonte_pequena = pygame.font.SysFont("arial", 18)

        self.tempo = 0
        self.botoes = []
        self.recriar_layout()

    def recriar_layout(self):
        largura, altura = self.obter_tamanho_janela()
        centro_x = largura // 2

        largura_botao = 340
        altura_botao = 56
        inicio_y = int(altura * 0.52)
        espaco = 72

        self.botoes = [
            Botao(
                (centro_x - largura_botao // 2, inicio_y, largura_botao, altura_botao),
                "Nova Guerra",
                self.abrir_nova_guerra,
                self.fonte_botao,
            ),
            Botao(
                (centro_x - largura_botao // 2, inicio_y + espaco, largura_botao, altura_botao),
                "Relatórios",
                self.abrir_relatorios,
                self.fonte_botao,
            ),
            Botao(
                (centro_x - largura_botao // 2, inicio_y + espaco * 2, largura_botao, altura_botao),
                "Sair",
                self.controlador.abrir_subtela_confirmacao_saida,
                self.fonte_botao,
            ),
        ]

    def abrir_nova_guerra(self):
        self.controlador.abrir_subtela(SubtelaMensagem(
            self.controlador,
            "Nova Guerra",
            "Sistema de partida ainda não criado.\nEste botão já prova o fluxo de subtelas.",
        ))

    def abrir_relatorios(self):
        self.controlador.abrir_subtela(SubtelaMensagem(
            self.controlador,
            "Relatórios",
            "O gerador de relatórios será ligado nas próximas etapas.\nA tela já nasce reservada para isso.",
        ))

    def processar_eventos(self, eventos):
        largura_antigo, altura_antigo = self.largura, self.altura
        self.largura, self.altura = self.obter_tamanho_janela()

        if (self.largura, self.altura) != (largura_antigo, altura_antigo):
            self.recriar_layout()

        for botao in self.botoes:
            botao.processar_eventos(eventos)

    def atualizar(self, dt):
        self.tempo += dt
        for botao in self.botoes:
            botao.atualizar_logica()

    def desenhar(self, surface):
        largura, altura = surface.get_size()

        self.desenhar_fundo(surface, largura, altura)
        self.desenhar_titulo(surface, largura, altura)

        for botao in self.botoes:
            botao.desenhar(surface)

        rodape = "War Multiversal • protótipo estrutural • tela/subtela/pipeline prontos"
        rodape_surf = self.fonte_pequena.render(rodape, True, (150, 160, 190))
        surface.blit(rodape_surf, (24, altura - 34))

    def desenhar_fundo(self, surface, largura, altura):
        surface.fill((8, 10, 18))

        # Grade de fundo, mantendo o visual centralizado em um único lugar.
        passo = 48
        deslocamento = int((self.tempo * 18) % passo)

        for x in range(-passo, largura + passo, passo):
            pygame.draw.line(surface, (18, 23, 42), (x + deslocamento, 0), (x + deslocamento - 180, altura), 1)

        for y in range(0, altura, passo):
            pygame.draw.line(surface, (14, 18, 34), (0, y), (largura, y), 1)

        # Núcleos multiversais abstratos.
        for i in range(5):
            raio = 70 + i * 42 + int(math.sin(self.tempo * 1.5 + i) * 8)
            cor = (30 + i * 8, 38 + i * 5, 80 + i * 18)
            pygame.draw.circle(surface, cor, (largura // 2, int(altura * 0.28)), raio, width=2)

    def desenhar_titulo(self, surface, largura, altura):
        titulo = self.fonte_titulo.render("WAR MULTIVERSAL", True, (235, 240, 255))
        sombra = self.fonte_titulo.render("WAR MULTIVERSAL", True, (65, 80, 150))

        titulo_rect = titulo.get_rect(center=(largura // 2, int(altura * 0.25)))
        sombra_rect = sombra.get_rect(center=(largura // 2 + 4, int(altura * 0.25) + 5))

        surface.blit(sombra, sombra_rect)
        surface.blit(titulo, titulo_rect)

        subtitulo = self.fonte_subtitulo.render(
            "turnos simultâneos • iniciativa • guerra entre universos",
            True,
            (165, 178, 220),
        )
        subtitulo_rect = subtitulo.get_rect(center=(largura // 2, titulo_rect.bottom + 34))
        surface.blit(subtitulo, subtitulo_rect)


class SubtelaMensagem(Subtela):
    def __init__(self, controlador, titulo, mensagem):
        super().__init__(controlador, largura=620, altura=330)
        self.titulo = titulo
        self.mensagem = mensagem

        self.fonte_titulo = pygame.font.SysFont("arial", 34, bold=True)
        self.fonte_texto = pygame.font.SysFont("arial", 22)
        self.fonte_botao = pygame.font.SysFont("arial", 24, bold=True)

        self.botao_ok = Botao(
            (0, 0, 180, 52),
            "OK",
            self.controlador.fechar_subtela,
            self.fonte_botao,
        )

    def atualizar(self, dt):
        super().atualizar(dt)
        self.botao_ok.rect.center = (self.rect.centerx, self.rect.bottom - 62)
        self.botao_ok.atualizar_logica()

    def processar_eventos(self, eventos):
        self.botao_ok.processar_eventos(eventos)

    def desenhar(self, surface):
        pygame.draw.rect(surface, (16, 20, 36), self.rect, border_radius=22)
        pygame.draw.rect(surface, (110, 130, 210), self.rect, width=2, border_radius=22)

        titulo_surf = self.fonte_titulo.render(self.titulo, True, (235, 240, 255))
        surface.blit(titulo_surf, (self.rect.x + 34, self.rect.y + 30))

        y = self.rect.y + 95
        for linha in self.mensagem.split("\n"):
            linha_surf = self.fonte_texto.render(linha, True, (190, 200, 230))
            surface.blit(linha_surf, (self.rect.x + 34, y))
            y += 32

        self.botao_ok.desenhar(surface)


class SubtelaConfirmarSaida(Subtela):
    def __init__(self, controlador):
        super().__init__(controlador, largura=560, altura=300)

        self.fonte_titulo = pygame.font.SysFont("arial", 34, bold=True)
        self.fonte_texto = pygame.font.SysFont("arial", 22)
        self.fonte_botao = pygame.font.SysFont("arial", 23, bold=True)

        self.botao_cancelar = Botao(
            (0, 0, 190, 52),
            "Cancelar",
            self.controlador.fechar_subtela,
            self.fonte_botao,
        )
        self.botao_sair = Botao(
            (0, 0, 190, 52),
            "Sair",
            self.controlador.encerrar,
            self.fonte_botao,
            cor_fundo=(64, 28, 36),
            cor_fundo_hover=(100, 42, 52),
            cor_borda=(220, 110, 120),
        )

    def atualizar(self, dt):
        super().atualizar(dt)

        y = self.rect.bottom - 68
        self.botao_cancelar.rect.center = (self.rect.centerx - 110, y)
        self.botao_sair.rect.center = (self.rect.centerx + 110, y)

        self.botao_cancelar.atualizar_logica()
        self.botao_sair.atualizar_logica()

    def processar_eventos(self, eventos):
        self.botao_cancelar.processar_eventos(eventos)
        self.botao_sair.processar_eventos(eventos)

    def desenhar(self, surface):
        pygame.draw.rect(surface, (16, 20, 36), self.rect, border_radius=22)
        pygame.draw.rect(surface, (130, 145, 220), self.rect, width=2, border_radius=22)

        titulo_surf = self.fonte_titulo.render("Sair do jogo?", True, (245, 246, 255))
        titulo_rect = titulo_surf.get_rect(center=(self.rect.centerx, self.rect.y + 62))
        surface.blit(titulo_surf, titulo_rect)

        texto_surf = self.fonte_texto.render(
            "A guerra multiversal será encerrada.",
            True,
            (190, 200, 230),
        )
        texto_rect = texto_surf.get_rect(center=(self.rect.centerx, self.rect.y + 126))
        surface.blit(texto_surf, texto_rect)

        self.botao_cancelar.desenhar(surface)
        self.botao_sair.desenhar(surface)
