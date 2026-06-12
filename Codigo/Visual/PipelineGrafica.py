import pygame

try:
    import moderngl
except ImportError:
    moderngl = None


class PipelineGrafica:
    def __init__(self, tela_base, tela_display, janela_opengl=False, config=None):
        self.TelaBase = tela_base
        self.TelaDisplay = tela_display
        self.JanelaOpenGL = janela_opengl
        self.Config = config or {}
        self.Contexto = None
        self.Textura = None
        self.Programa = None
        self.Buffer = None
        self.Vao = None
        self.ShaderAtivo = bool(self.Config.get("Shader", True))

        if self.JanelaOpenGL and moderngl is not None:
            try:
                self.Contexto = moderngl.create_context()
                self.Contexto.enable(moderngl.BLEND)
                self.CriarPipelinePadrao()
            except Exception:
                self.Contexto = None
                self.JanelaOpenGL = False

    def CriarPipelinePadrao(self):
        self.Programa = self.Contexto.program(
            vertex_shader='''
                #version 330
                in vec2 in_pos;
                in vec2 in_uv;
                out vec2 uv;
                void main() {
                    gl_Position = vec4(in_pos, 0.0, 1.0);
                    uv = in_uv;
                }
            ''',
            fragment_shader='''
                #version 330
                uniform sampler2D textura_tela;
                in vec2 uv;
                out vec4 fragColor;
                void main() {
                    fragColor = texture(textura_tela, uv);
                }
            ''',
        )

        vertices = [
            -1.0, -1.0, 0.0, 0.0,
             1.0, -1.0, 1.0, 0.0,
            -1.0,  1.0, 0.0, 1.0,
             1.0,  1.0, 1.0, 1.0,
        ]

        import struct
        self.Buffer = self.Contexto.buffer(struct.pack(f"{len(vertices)}f", *vertices))
        self.Vao = self.Contexto.vertex_array(self.Programa, [(self.Buffer, "2f 2f", "in_pos", "in_uv")])
        self.Textura = self.Contexto.texture(self.TelaBase.get_size(), 4)
        self.Textura.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.Programa["textura_tela"] = 0

    def IniciarFrame(self):
        self.TelaBase.fill((8, 9, 18))

        if self.Contexto is not None:
            self.Contexto.clear(0.03, 0.035, 0.07, 1.0)

    def Aplicar(self):
        if self.JanelaOpenGL and self.Contexto is not None:
            dados = pygame.image.tostring(self.TelaBase, "RGBA", True)

            if self.Textura.size != self.TelaBase.get_size():
                self.Textura.release()
                self.Textura = self.Contexto.texture(self.TelaBase.get_size(), 4)
                self.Textura.filter = (moderngl.NEAREST, moderngl.NEAREST)

            self.Textura.write(dados)
            self.Textura.use(0)
            self.Vao.render(moderngl.TRIANGLE_STRIP)
            pygame.display.flip()
            return

        self.TelaDisplay.blit(self.TelaBase, (0, 0))
        pygame.display.flip()
