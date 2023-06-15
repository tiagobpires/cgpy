## [Primeira Avaliação - Computação Gráfica I](http://www.lia.ufc.br/~yuri/20231/cg/trabcg1.html)

### Descrição do trabalho

O trabalho é um jogo onde você deve utilizar as setas "<-" e "->" para se mover pela tela e desviar dos polígonos que estão caindo. No final do jogo, é exibido pelo terminal quantos polígonos você conseguiu desviar!


### Instruções para execução

1. Criar e ativar ambiente virtual (opcional)

```sh
python -m venv venv
```

No Windows:

```sh
venv\Scripts\activate.bat
```

No Linux:

```sh
source venv/bin/activate
```

2. Instalar bibliotecas necessárias

```sh
pip install -r requirements.txt
```

3. Executar arquivo

```sh
python main.py
```


### Requisitos do trabalho

1. O programa possui uma tela de abertura com rasterização de tela (retas brancas ligando as formas), circunferências e elipse. 

2. As figuras criadas na tela de abertura são preenchidas com o algoritmo Flood Fill em uma animação.

3. Após clicar em "Enter", é exibida uma pequena animação das formas caindo. Nela, as figuras são transformadas em polígonos e são aplidas as 3 principais transformações geométricas: translação, escala e rotação.

4. Quando o jogo se inicia, são utilizadas duas janelas e duas viewports. As primeiras são a do próprio jogo e não possuem diferenças com o tamanho da tela. Já as segundas são o "minimap" exposto no lado superior direito. Nele, são apresentadas transformações de translação e escala (zoom)

5. No jogo, são gerados polígonos aleatoriamente. Dentre eles, existem polígonos normais (uma cor), polígonos com gradientes de cores (definidas por vértice) e texturas coloridas, todos preenchidos por scanline.

6. Também são feitas transformações de forma aleatória nos polígonos caindo. São elas: translação, escala e rotação.

OBS: Todas as letras foram feitas utilizando imagens/texturas. De biblioteca gráfica, foi utilizado apenas o "set_pixel" e "get_pixel", como requisitado.
