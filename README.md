# Compilador
Projeto que converte um código escrito em uma linguagem simplificada (LGG) para a linguagem C. A interface do projeto simula uma pequena IDE, permitindo que o usuário escreva, compile e veja o código gerado em C. Além disso, o projeto suporta um modo noturno e destaca a sintaxe da linguagem LGG no editor.
Este projeto foi desenvolvido como parte de um estudo em compiladores, análise léxica, análise sintática, e geração de código. O LGG Compiler inclui a capacidade de interpretar e processar comandos básicos como declarações de variáveis, condicionais, laços while e for, e operações de entrada/saída (leia e escreva).

# Funcionalidades
Editor de código com Highlight: Realça a sintaxe da linguagem LGG no editor.
Modo Noturno: Interface gráfica com alternância entre modo claro e escuro.
Geração de Código C: Traduz o código escrito em LGG diretamente para C.
Verificação de Erros: Verifica erros de sintaxe durante a compilação e alerta o usuário.
Interpretação de Estruturas de Controle: Suporta comandos como se ... entao ... senao, laços enquanto e for.
Suporte a Entrada e Saída: Comandos leia e escreva traduzidos para scanf e printf no código C.

# Estrutura do Projeto
O código está dividido em várias funções que realizam a análise léxica, análise sintática e geração de código C. Aqui estão as principais partes do projeto:

* Tokenização: O código é dividido em tokens (palavras-chave, operadores, identificadores, etc.) usando expressões regulares.
* Análise Sintática (Parsing): Funções específicas são usadas para interpretar as construções da linguagem LGG, como declarações, condicionais e laços.
* Geração de Código C: Cada construção da linguagem LGG é convertida em seu equivalente na linguagem C.

# Principais Funções
```parse_declara()```: Processa a declaração de variáveis e adiciona à tabela de símbolos.

```parse_cmd_if()```: Interpreta as estruturas condicionais se ... entao ... senao e gera código if ... else em C.

```parse_cmd_while()```: Analisa laços enquanto e os converte para while em C.

```parse_cmd_for()```: Processa laços for da LGG e os traduz para a estrutura for em C.

```parse_cmd_leitura() e parse_cmd_escrita()```: Convertem os comandos de entrada/saída (leia e escreva) para scanf e printf.

# Requisitos
* Python 3.8 ou superior
* Biblioteca tkinter (para interface gráfica)
