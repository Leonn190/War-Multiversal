import os
import ctypes

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame

try:
    import moderngl
except ImportError:
    moderngl = None

from ConfigFixa import CarregarConfig, SalvarConfig
from Codigo.Client.ControladorJogo import ControladorJogo

if hasattr(ctypes, "windll") and hasattr(ctypes.windll, "shell32"):
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("war.multiversal")

pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    pass


def CriarJanela():
    flags = pygame.NOFRAME

    if moderngl is not None:
        try:
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

            try:
                return pygame.display.set_mode((1920, 1080), flags | pygame.OPENGL | pygame.DOUBLEBUF, vsync=0), True
            except TypeError:
                return pygame.display.set_mode((1920, 1080), flags | pygame.OPENGL | pygame.DOUBLEBUF), True
        except pygame.error:
            pass

    return pygame.display.set_mode((1920, 1080), flags), False


JANELA, JANELA_OPENGL = CriarJanela()
TELA = pygame.Surface((1920, 1080)).convert_alpha()
pygame.display.set_caption("War Multiversal")

RELOGIO = pygame.time.Clock()
CONFIG = CarregarConfig()

Game = ControladorJogo(TELA, RELOGIO, CONFIG, tela_display=JANELA, janela_opengl=JANELA_OPENGL)
Game.DefinirTela("TelaInicial")

try:
    Game.Rodar()
finally:
    SalvarConfig(CONFIG)
    Game.Encerrar()
    if hasattr(Game, "Sonoridades"):
        Game.Sonoridades.PararTudo()
    if pygame.mixer.get_init():
        pygame.mixer.stop()
    pygame.quit()
