#!/usr/bin/env python3

# ATENÇÃO: NENHUM IMPORT ADICIONAL É PERMITIDO!
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


def gerar_kernel_desfoque(n):
    """
    Gera um kernel de desfoque de tamanho n x n. Esse kernel deve possuir a
    soma dos seus elementos igual a 1.
    """
    return [[1 / (n ** 2) for _ in range(n)] for _ in range(n)]


class Imagem:
    """
    Essa classe cria objetos de imagem. Seus atributos são altura, largura e pixels, onde
    cada pixel é uma lista de tamanho largura X altura e cada elemento é um valor no intervalo [0, 255]
    (preto mais escuro ao branco mais claro).

    Seus métodos permitem manipular a imagem com diversos filtros, obter o valor de cada pixel
    e alterá-los.
    """
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        """
        Retorna o valor do pixel na posição (x, y). Caso a coordenada seja negativa (fora do tamanho
        da imagem) ele obtém o pixel da posição 0; em contrapartida, se a coordenada for superior
        ao tamanho máximo da imagem ela retorna a última posição do tamanho da imagem.

        Essa condição é essencial para a aplicação da correlação.
        """
        if x >= self.largura:
            x = self.largura - 1
        elif x < 0:
            x = 0
        if y >= self.altura:
            y = self.altura - 1
        elif y < 0:
            y = 0

        return self.pixels[(x + y * self.largura)]

    def set_pixel(self, x, y, c):
        """
        Altera o valor do pixel na posição (x, y). Os pixels da imagem são passados como lista.
        """
        self.pixels[(x + y * self.largura)] = c

    def aplicar_por_pixel(self, func):
        """
        Altera o valor de cada pixel da imagem por meio de uma função e retorna a nova imagem
        alterada.
        """
        resultado = Imagem.new(self.largura, self.altura)
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor)
        return resultado

    def corrigir_pixel_imagem(self):
        """
        Altera os valores dos pixels que não estão no intervalo [0, 255] ou não são números inteiros.
        Para valores negativos, o pixel é definido para 0; valores maiores que 255 têm o pixel definido para 255;
        para números decimais, o valor é arredondado para o inteiro mais próximo.
        """
        for i in range(self.largura):
            for j in range(self.altura):
                pixel = self.get_pixel(i, j)
                if pixel < 0:
                    pixel = 0
                elif pixel > 255:
                    pixel = 255
                self.set_pixel(i, j, round(pixel))

    def correlacao(self, kernel):
        """
        Retorna uma nova imagem correlacionada com um kernel. É uma função de filtragem
        de imagem por correlação.
        """
        meio = len(kernel) // 2           # meio do kernel independente do seu tamanho
        imagem_temp = Imagem.new(self.largura, self.altura)
        for i in range(imagem_temp.largura):
            for j in range(imagem_temp.altura):
                new_pixel = 0
                for m in range(len(kernel)):
                    for n in range(len(kernel)):
                        new_pixel += self.get_pixel((i - meio + n), (j - meio + m)) * kernel[m][n]
                imagem_temp.set_pixel(i, j, new_pixel)
        return imagem_temp

    def invertido(self):
        """
        Retorna o valor do pixel invertido.
        """
        return self.aplicar_por_pixel(lambda c: 255 - c)

    def borrado(self, n):
        """
        Retorna a imagem com o filtro de borrar. Recebe um parâmetro inteiro n. Quanto maior esse valor,
        maior o efeito de blur.
        """
        img_borrado = self.correlacao(gerar_kernel_desfoque(n))
        img_borrado.corrigir_pixel_imagem()
        return img_borrado

    def nitidez(self, n):
        """
        Retorna a imagem com o filtro de nitidez (sharpen). Recebe um parâmetro inteiro n. Quanto maior esse valor,
        maior o efeito de nitidez.
        """
        img_borrada = self.borrado(n)
        img_nitidez = Imagem.new(self.largura, self.altura)
        for i in range(self.largura):
            for j in range(self.altura):
                s = round(2 * self.get_pixel(i, j) - img_borrada.get_pixel(i, j))
                img_nitidez.set_pixel(i, j, s)
        img_nitidez.corrigir_pixel_imagem()
        return img_nitidez

    def bordas(self, k1, k2):
        """
        Retorna a imagem com o filtro de detecção de bordas. Recebe dois kernels específicos.
        """
        img1 = self.correlacao(k1)
        img2 = self.correlacao(k2)
        img_bordas = Imagem.new(self.largura, self.altura)
        for i in range(self.largura):
            for j in range(self.altura):
                o = round(math.sqrt(img1.get_pixel(i, j) ** 2 + img2.get_pixel(i, j) ** 2))
                img_bordas.set_pixel(i, j, o)
        img_bordas.corrigir_pixel_imagem()
        return img_bordas

    # Abaixo deste ponto estão utilitários para carregar, salvar,
    # mostrar e testar imagens.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, arquivo):
        """
        Carrega uma imagem a partir de um arquivo e retorna uma instância
        da classe representando essa imagem. Também realiza a conversão
        para escala de cinza.

        Modo de usar:
           i = Imagem.carregar('imagens_teste/gato.png')
        """
        with open(arquivo, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, largura, altura):
        """
        Cria uma nova imagem vazia (blank image) (tudo 0) para uma dada largura e altura.

        Modo de uso:
            i = Imagem.new(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, arquivo, modo='PNG'):
        """
        Salva uma dada imagem no disco ou para um objeto semelhante a um
        arquivo. Se "arquivo" é dado como uma string, o tipo de arquivo
        será inferido do próprio nome. Se "arquivo" for dado como um
        objeto semelhante a um arquivo, o tipo de arquivo será determinaddo
        pelo parâmetro "modo".
        """
        out = PILImage.new(mode='L', size=(self.largura, self.altura))
        out.putdata(self.pixels)
        if isinstance(arquivo, str):
            out.save(arquivo)
        else:
            out.save(arquivo, modo)
        out.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo
        a imagem como um GIF. É um utilitário para fazer a função
        mostrar ficar mais limpa.
        """
        buff = BytesIO()
        self.salvar(buff, modo='GIF')
        return base64.b64encode(buff.getvalue())

    def mostrar(self):
        """
        Mostra a imagem em uma janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se o Tk não está inicializado de forma apropriada, não faz nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evendo de redimensionamento (causando um loop infinito). Veja
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.altura,
                                width=self.largura, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)

        def on_resize(event):
            # Realiza o redimensionamento da imagem quando a janela é redimensionada.
            # O procedimento é:
            #  * Converter para uma imagem PIL
            #  * Redimensionar essa imagem
            #  * Obter o GIF codificado em base64 a partir da imagem redimensionada
            #  * Colocar essa imagem em um label tkinter
            #  * Mostrar essa imagem no canvas
            new_img = PILImage.new(mode='L', size=(self.largura, self.altura))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)

        # Finalmente, vincular essa função para que ela seja chamada
        # quando a janela for redimensionada.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))

        # when the window is closed, the program should stop
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()

    def reafter():
        tcl.after(500, reafter)

    tcl.after(500, reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco somente será rodado quando você, explicitamente,
    #  rodar seu script, e não quando os testes forem executados. Este é um
    #  bom lugar para gerar imagens, etc.
    pass

    # Questão 2 --------------
    # i = Imagem.carregar('imagens_teste/peixe.png')
    # temp = i.invertido()
    # temp.salvar('resultados_teste/peixe_invertido.png')

    # Questão 3 --------------
    # i = Imagem.carregar('imagens_teste/porco.png')
    # temp = i.correlacao([[0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                      [1, 0, 0, 0, 0, 0, 0, 0, 0],
    #                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                      [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    # temp.salvar('resultados_teste/porco_correlacao.png')

    # Tópico 5.1: Desfoque | aplicar filtro na imagem gato com um kernel de desfoque de tamanho 5
    # i = Imagem.carregar('imagens_teste/gato.png')
    # temp = i.borrado(5)
    # temp.salvar('resultados_teste/gato_borrado.png')

    # Questão 5 --------------
    # Aplicar filtro de nitidez com kernel de tamanho 11 na imagem python.png
    # i = Imagem.carregar('imagens_teste/python.png')
    # temp = i.nitidez(11)
    # temp.salvar('resultados_teste/python_nitidez.png')

    # Questão 6 --------------
    # Aplicar o filtro de detecção de bordas com dois kernels na imagem obra.png
    # i = Imagem.carregar('imagens_teste/obra.png')
    # temp = i.bordas([[-1, 0, 1],
    #                  [-2, 0, 2],
    #                  [-1, 0, 1]], [[-1, -2, -1],
    #                                [0,   0,  0],
    #                                [1,   2,  1]])
    # temp.salvar('resultados_teste/obra_bordas.png')

    # O código a seguir fará com que as janelas em Imagem.mostrar
    # sejam mostradas de modo apropriado, se estivermos rodando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
