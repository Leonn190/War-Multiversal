from pathlib import Path
import pygame


class Sonoridades:
    def __init__(self, config=None):
        self.Config = config or {}
        self.Raiz = Path(__file__).resolve().parents[2]
        self.MusicaAtual = None
        self.CaminhoTema = self.Raiz / "Recursos" / "Sonoridades" / "Musicas" / "Theme.mp3"

    def MixerPronto(self):
        return pygame.mixer.get_init() is not None

    def VolumeAtual(self):
        if self.Config.get("Mudo", False):
            return 0
        return float(max(0, min(1, self.Config.get("Volume", 0.5))))

    def AplicarVolume(self):
        if not self.MixerPronto():
            return
        pygame.mixer.music.set_volume(self.VolumeAtual())

    def TocarMusica(self, caminho, loop=True, reiniciar=False):
        if not self.MixerPronto():
            return False

        caminho = Path(caminho)
        if not caminho.exists():
            return False

        caminho_texto = str(caminho)
        if self.MusicaAtual == caminho_texto and pygame.mixer.music.get_busy() and not reiniciar:
            self.AplicarVolume()
            return True

        try:
            pygame.mixer.music.load(caminho_texto)
            pygame.mixer.music.play(-1 if loop else 0)
            self.MusicaAtual = caminho_texto
            self.AplicarVolume()
            return True
        except pygame.error:
            self.MusicaAtual = None
            return False

    def TocarTema(self):
        return self.TocarMusica(self.CaminhoTema, loop=True)

    def PararMusica(self):
        if not self.MixerPronto():
            return
        pygame.mixer.music.stop()
        self.MusicaAtual = None

    def PararTudo(self):
        if not self.MixerPronto():
            return
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        self.MusicaAtual = None
