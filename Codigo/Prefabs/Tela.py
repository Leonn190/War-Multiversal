class Tela:
    def __init__(self, controlador):
        self.Controlador = controlador
        self.Botoes = []
        self.Textos = []
        self.Nome = self.__class__.__name__

    def Entrar(self):
        pass

    def Sair(self):
        pass

    def ProcessarEventos(self, eventos):
        pass

    def Atualizar(self, dt):
        mouse_pos = self.Controlador.MousePos
        for botao in self.Botoes:
            botao.AtualizarRect(self.Controlador.Layout)
            botao.Atualizar(self.Controlador.Eventos, mouse_pos)

    def Desenhar(self, tela):
        pass
