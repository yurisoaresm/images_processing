# Problem Set 2
Este *problem set* é uma tarefa de programação que os alunos da disciplina “MIT 6.009: Fundamentals of Programming” recebem na primeira semana de aula, entregue como pset2 para a disciplina "Linguagens de Programação" na Universidade de Vila Velha.

**Feito por**: [Yuri Soares](https://github.com/yurisoaresm "Perfil do Yuri Soares no GitHub"),

E **orientado** por: [prof. Abrantes Araújo S. Filho](https://github.com/abrantesasf "Perfil do prof. Abrantes Araújo S. Filho no GitHub").

Este documento README explica como o projeto funciona. Dentro do código também há [docstrings](https://en.wikipedia.org/wiki/Docstring#Python "Sobre docstrings em Python") que explicam o funcionamento de cada função.

> No decorrer do projeto há algumas questões sobre certas funcionalidades dos algoritmos; elas foram feitas como parte da tarefa e auxiliam no entendimento do código. Todas as perguntas estão formatadas como este parágrafo.

## 1 Pre-requisitos
Para execução do programa é preciso ter o Python 3.5 (ou superior) instalado na máquina ([Download Python mais recente](https://www.python.org/downloads/ "Página Download Python")). Ele também usa a biblioteca [Pillow](https://pillow.readthedocs.io/en/stable/ "Sobre a biblioteca Pillow") para carregar e salvar imagens. 

## 2 Introdução
Este programa é composto por algoritmos capazes de criar, carregar, salvar e manipular (inverter, desfocar, detectar bordas etc) imagens digitais.

O arquivo `pset2.py` é o programa de manipulação de imagem. Nele há todos os filtros e ferramentas para o objetivo deste pset. Já o `pset2_testes.py` é um arquivo de testes, criado para comparar os resultados obtidos com os esperados.

Para executar os testes você pode executar o seguinte comando no terminal:

    $ python3 pset2_testes.py TestImagem

Para executar um caso de teste em particular, use por exemplo:

    $ python3 pset2_testes.py TestInvertido.test_invertido_1

### 2.1 Classe e Representação de uma imagem Digital
Há diversas maneiras de representar uma imagem digital, porém a adotada neste programa é a de pixels (mais comum). Cada imagem possui duas dimensões: largura e altura, formando uma matriz de pixels. Cada pixel é um valor para uma cor. Aqui, trabalhamos com tons de cinza; portanto, para cada pixel da imagem aplicamos um valor no intervalo [0, 255], onde 0 é o preto mais escuro e 255 o branco mais claro.

![Figura 1](https://py.processing.org/tutorials/color/imgs/grayscale.jpg "Figura 1: tonz de cinza representando um pixel")

Neste programa cada imagem é representada pela classe Imagem, com seus atributos largura, altura e pixels. Os pixels são uma **lista** de valores armazenados em [row-major](https://en.wikipedia.org/wiki/Row-_and_column-major_order "Row- and column-major order"). 

Um objeto 2 x 1 dessa classe seria: `i = Imagem(2, 1 [0, 255])`

### 2.2 Carregando e Salvando Imagens
Dentro da pasta [imagens_teste](https://github.com/yurisoaresm/images_processing/tree/master/imagens_teste "Ir para pasta imagens_teste") há várias imagens para serem usadas como testes do programa. No diretório [resultados_teste](https://github.com/yurisoaresm/images_processing/tree/master/resultados_teste "Ir para pasta resultados_teste") há algumas imagens pré-prontas para serem comparadas com os resultados obtidos e outras são imagens salvas no decorrer do programa.

A classe Imagem possui métodos para `carregar()` (recebe o caminho da imagem), `new()` (cria uma imagem preta, ou seja, com pixels iguais a 0) e `salvar()` (recebe o caminho do diretório) imagens.

## 3 Filtragem de inversão
O primeiro filtro deste programa é o de inverter cada pixel da imagem. Ele altera cada pixel de tom escuro no seu correspondente de cor clara e vice-versa. 

Para tanto, a função `invertido()` retorna o resultado de outra função `aplicar_por_pixel(func)`. Esta recebe como parâmetro o cálculo de inversão por meio de uma [função lâmbda](https://www.w3schools.com/python/python_lambda.asp "Python Lambda") (função anônima; lambda c: 255 - c) e o aplica para cada pixel da imagem original, retornando, por sua vez, a imagem invertida.

### *Questão 1* 
> Data uma imagem com as seguintes condições: altura = 1, largura = 4, e pixels = [29, 89, 136, 200], se você passar essa imagem pelo filtro de inversão, qual seria o output esperado? 

O resultado do filtro de inversão seria uma nova imagem com as mesmas dimensões, porém com sua matriz de pixel invertida ([255 - 29, 255 - 89, 255 - 136, 255 - 200]), ou seja, os tons mais escuros seriam os mais claros e vice-versa (praticamente ela altera o sentido das cores da imagem original). As duas imagens podem ser vistas abaixo (ignorando as proporções dos pixels):

![questao1](https://user-images.githubusercontent.com/91438344/188511717-37a505a2-ed16-4ef9-9b7f-52de2909d59c.jpg)

### *Questão 2*
> Faça a depuração e, quando terminar, seu código deve conseguir passar em todos os testes do grupo de teste TestInvertido. Execute seu filtro de inversão na imagem imagens_teste/peixe.png, salve o resultado como uma imagem PNG e salve a imagem em seu repositório GitHub.

O resultado obtido:

![Figura 2](https://raw.githubusercontent.com/yurisoaresm/images_processing/master/resultados_teste/peixe_invertido.png "Figura 2: peixe com filtro de inversão")

## 4 Filtragem por Correlação
### 4.1 Correlação e Kernel
Correlacionar uma imagem é uma forma de alterá-la por meio de um kernel. Um kernel é uma matriz n x n de tamanho ímpar. Há vários kernels que modificam imagens para obter resultados específicos, como os kernels de *blur*. 

Cada pixel de uma imagem correlacionada é o resultado da **combinação linear** dos pixels ao redor da posição (x, y) (sabendo que a posição 0, 0 é o canto superior esquerdo da imagem), onde os pesos são definidos pelo kernel.

![kernel-borda](https://user-images.githubusercontent.com/91438344/188511471-09b92eeb-af0b-44e6-8d06-03e01b9f23eb.jpg)

### *Questão 3*
> Considere uma etapa de correlacionar uma imagem com o seguinte kernel:
> | 0.00  | -0.07 | 0.00  |
> |-------|-------|-------|
> | -0.45 | 1.20  | -0.25 |
> | 0.00  | -0.12 | 0.00  |

> Agora considere a seguinte matriz como um recorte da imagem em questão:
> | 80  | 53  | 99  |
> |-----|-----|-----|
> | 129 | [127] | 148 |
> | 175 | 174 | 193 |

> Qual será o valor do pixel na imagem de saída no local indicado pelo destaque em colchete? Observe que neste ponto ainda não arredondamos ou recortamos o valor, informe exatamente como você calculou. Observação: demonstre passo a passo os cálculos realizados.

Aplicando a combinação linear: 80 * 0.00 + 53 * (-0.07) + 99 * 0.00 + 129 * (-0.45) + 127 * 1.20 + 148 * (-0.25) + 175 * 0.00 + 174 * (-0.12) + 193 * 0.00 = 0 + (-3.71) + 0 + (-58.05) + 152.4 + (-37) + 0 + (-20.88) + 0 = **32.76**

### 4.2 Problemas com Bordas
Ao aplicar um determinado kernel na borda de uma imagem, alguns dos pixels estarão fora dos limites da imagem (lembrando que a posição central do kernel é passada para cada em cada pixel da imagem). Para aplicar a correlação nesses casos, cada pixel fora do limite da imagem na posição x assumirá o valor de pixel da imagem na posição central do kernel; idem para y. 

Um exemplo prático está na figura abaixo, onde um kernel 3 x 3 (em vermelho; seus valores estão ocultos para fim didático) está sendo aplicado a uma imagem aleatória de tamanho 3 x 3 e com pixels iguais a [87, 94, 35, 32, 44, 55, 0, 0, 0]. Ao aplicar o kernel no primeiro pixel (canto superior esquerdo; destaque laranja) da imagem, os lados acima e à esquerda transpassam os limites da imagem. Nessas posições não há valores de cor para calcular a combinação linear. Nesse caso, o primeiro pixel da imagem mais próximo dessa posição será usado para o cálculo matemático. (ver desenho da direita). O mesmo se aplica a cada caso onde os valores do kernel ultrapassem os limites da matriz.

A função correlação abaixo executa essa tarefa. A variável meio calcula a parte inteira da divisão que gera a distância das bordas ao centro do kernel.

    def correlacao(self, kernel):
    meio = len(kernel) // 2           
    imagem_temp = Imagem.new(self.largura, self.altura)
    for i in range(imagem_temp.largura):
        for j in range(imagem_temp.altura):
            new_pixel = 0
            for m in range(len(kernel)):
                for n in range(len(kernel)):
                    new_pixel += self.get_pixel((i - meio + n), (j - meio + m)) * kernel[m][n]
            imagem_temp.set_pixel(i, j, new_pixel)
    return imagem_temp

### 4.3 Normalização
Note que pelos cálculos os pixels da imagem correlacionada podem não ser uma imagem **ideal**, isto é, estão fora do intervalo [0, 255] e/ou ser floats. Para consertar esses pequenos desvios, existe uma função que é aplicada a imagem correlacionada para corrigir as divergências dos extremos: se o pixel for menor que 0, seu valor passa a ser 0; se maior que 255, será definido para 255; e arredonda o número para o inteiro mais próximo.

### *Questão 4*
> Quando você tiver implementado seu código, tente executá-lo em imagens_teste/porco.png com o seguinte kernel 9 × 9:
> | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
> |---|---|---|---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
> | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
> | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
> | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
> | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
> | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
> | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
> | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

O resultado obtido:

![Figura 3](https://raw.githubusercontent.com/yurisoaresm/images_processing/master/resultados_teste/porco_correlacao.png "Figura 3: porco com correlação")

## 5 Desfoque
O efeito de desfoque (ou *blur*) numa imagem é o resultado da sua correlação com um kernel n x n onde a soma dos valores dos elementos é igual a 1. É fácil notar que se o tamanho de um kernel é sempre n x n (onde n é um número inteiro), cada valor do kernel deve ser 1 / n² (a soma das partes gera 1). A função `gerar_kernel_desfoque(n)` cria um kernel de tamanho n, onde quanto maior for o valor de n, tanto maior o efeito de *blur*.

## 6 Nitidez
A nitidez é um filtro capaz de melhorar uma imagem, torando-a mais agradável visualmente (sem serrilhado). Outro nome dado a esse filtro é **máscara de não nitidez** (*Unsharp mask*) porque sua aplicação é a subtração do **dobro** de cada pixel de uma imagem normal (não filtrada) o pixel correspondente da sua correlação com *blur*. Matematicamente falando, seja (x, y) as coordenadas de um pixel de uma imagem, S o resultado, I a imagem normal e B a a imagem borrada, então: `S(x, y) = 2I(x, y) - B(x, y)`. A função `nitidez()` recebe um valor n que é o tamnanho do kernel de defoque. Para valores altos, o efeito de nitidez também aumentará.

### *Questão 5*
> Se quisermos usar uma versão desfocada B que foi feita com um kernel de desfoque de caixa de 3 × 3, que kernel k poderíamos usar para calcular toda a imagem nítida com uma única correlação? Justifique sua resposta mostrando os cálculos.

Pela forma supracitada, suponhamos que um pixel I(x, y) seja igual a **k**. Então o que a fórmula supracitada faz é: 2 * k - (1 / n²) * k. Se colocarmos k em evidência, temos: k (2 - (1/n²)). Note que o pixel k da imagem com *unsharp mask* é o resultado da conta fatorada. Logo, podemos criar dois kernels, um para dobrar o valor dos pixels da imagem e outro para borrá-la, e subtrair este daquele. Usando um kernel de desfoque 3 x 3, temos:

    k1 = [0, 0, 0]
         [0 , 2, 0]
         [0, 0, 0]          // Este kernel duplica o valor de cada pixel
    k2 = [1/9, 1/9, 1/9]
         [1/9, 1/9, 1/9]
         [1/9, 1/9, 1/9]    // Kernel de desfoque, conforme explicado no tópico 5
    k = k1 - k2 = [0 - 1/9, 0 - 1/9, 0 - 1/9] = [-1/9, -1/9, -1/9]
                  [0 - 1/9, 2 - 1/9, 0 - 1/9]   [-1/9, 17/9, -1/9]
                  [0 - 1/9, 0 - 1/9, 0 - 1/9]   [-1/9, -1/9, -1/9] // Resultado da subtração de matrizes

## 7 Detecção de Bordas
Para detectar bordas numa imagem usamos o [operador Sobal](https://en.wikipedia.org/wiki/Sobel_operator "Sobel Operator"). Ele combina duas correlações de uma imagem para detectar suas bordas. Os kernels utilizados são [-1,  0,  1], [-2,  0,  2], [-1,  0,  1]] e [-1, -2, -1], [0,   0,  0], [1,   2,  1]]

### *Questão 6*
> Explique o que cada um dos kernels acima, por si só, está fazendo. Tente executar mostrar nos resultados dessas correlações intermediárias para ter uma noção do que está acontecendo aqui.

Cada kernel faz uma "varredura" da imagem na horizontal e vertical. Um enfatiza as bordas num centido cima-baixo, outro esquerda-direito. Após isso, o operador combina os dois filtros para obter a melhor representação das bordas da imagem. A figura abaixo ilustra o processo para obtenção das bordas:

![bordas-xadrez](https://user-images.githubusercontent.com/91438344/188511448-be78427e-7266-4629-b87f-8c0c6cdab679.jpg)
