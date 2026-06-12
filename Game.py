import os
import ctypes

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame

try:
    import moderngl
except ImportError:
    moderngl = None

from Codigo.Client.ControladorJogo import ControladorJogo

if hasattr(ctypes, "windll") and hasattr(ctypes.windll, "shell32"):
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("war.multiversal")

pygame.init()
pygame.mixer.init()


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

CONFIG = {
    "FPS": 200,
    "Volume": 0.5,
    "Claridade": 75,
    "Mudo": False,
    "FPS Visivel": True,
    "Shader": True,
    "LarguraBase": 1920,
    "AlturaBase": 1080,
}

Game = ControladorJogo(TELA, RELOGIO, CONFIG, tela_display=JANELA, janela_opengl=JANELA_OPENGL)
Game.DefinirTela("TelaInicial")

try:
    Game.Rodar()
finally:
    Game.Encerrar()
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    pygame.quit()
