# Circuito SIFSM — alerta energético

Este diretório reúne a exportação do Circuit Design, a lista de materiais e
os arquivos usados para reproduzir a validação da regra `(A && B) || C`.

## Arquivos

| Arquivo | Finalidade |
| --- | --- |
| [Projeto-FIAP.pdf](Projeto-FIAP.pdf) | Esquema original fornecido, sem alterações |
| [lista-componentes.csv](lista-componentes.csv) | Lista original fornecida, sem alterações |
| [circuito_logico.png](esquema-circuito.png) | Prévia renderizada do PDF |
| [tabela-verdade.csv](tabela-verdade.csv) | Oito estados esperados e comandos serial |
| [resultado-testes-python.txt](resultado-testes-python.txt) | Saída da execução dos testes automatizados |
| [validacao-dados.txt](validacao-dados.txt) | Resultado de uma avaliação do CSV energético |

As exportações originais se chamavam `Projeto-FIAP (1).pdf` e `bom (1).csv`.
Somente os nomes foram padronizados. O PDF é um esquema elétrico: o código
Arduino é entregue separadamente, no arquivo `.ino`.

## Montagem prevista pelo código

| Sinal | Conexão |
| --- | --- |
| A — consumo alto | D2, botão entre entrada e GND |
| B — módulo crítico | D3, botão entre entrada e GND |
| C — falha | D4, botão entre entrada e GND |
| LED vermelho | D8, resistor de 220 ohms em série, retorno GND |
| Piezo | Positivo D9, negativo GND |

Os botões usam `INPUT_PULLUP`: pressionado equivale a entrada lógica 1 no
programa. Os rótulos S1/S2/S3 do esquema não definem A/B/C: confira o pino.
A lista fornecida inclui Arduino Uno R3, protoboard pequena, LED vermelho,
resistor 220 ohms, piezo e três botões.

## Reproduzir no Python

Na raiz do repositório, execute:

```console
python -m unittest discover -s tests -v
python codigo_fonte.py
```

No menu, escolha **10** e depois **3** para gerar a tabela verdade em
`data/circuito/tabela_verdade.csv`. O modo **1** avalia uma leitura manual e o
modo **2** avalia o CSV existente. O limite deve usar a mesma unidade da
leitura. Como o CSV não contém status nem falhas, B/C são fornecidos pelo
operador e permanecem constantes durante essa avaliação.

## Reproduzir no Tinkercad

1. Abra o circuito existente e pare a simulação antes de editar.
2. No editor Texto, cole o conteúdo de
   `simulador/alerta_energetico/alerta_energetico.ino` da raiz do projeto.
3. Inicie a simulação e abra o Monitor Serial em 9600 baud.
4. Envie cada comando abaixo, um por vez, com Enter, e confira o resultado.

| A | B | C | Comando | Alerta esperado | LED / piezo |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | SET 000 | 0 | Desligados |
| 0 | 0 | 1 | SET 001 | 1 | Ligados |
| 0 | 1 | 0 | SET 010 | 0 | Desligados |
| 0 | 1 | 1 | SET 011 | 1 | Ligados |
| 1 | 0 | 0 | SET 100 | 0 | Desligados |
| 1 | 0 | 1 | SET 101 | 1 | Ligados |
| 1 | 1 | 0 | SET 110 | 1 | Ligados |
| 1 | 1 | 1 | SET 111 | 1 | Ligados |

5. Envie `BTN` para voltar aos botões e repita a tabela fisicamente.
6. Envie `SET 102` e confirme a mensagem de erro e a preservação do estado.
7. Registre os resultados observados e uma captura da simulação.

## Estado da validação

Os quatro testes Python passaram, incluindo as oito combinações, o limite,
a prioridade de falha, valores inválidos e exportação de comandos. A avaliação
do CSV energético está registrada em `validacao-dados.txt` com parâmetros
explicitamente didáticos.

O novo sketch e seus comandos serial ainda precisam ser compilados e
validados no Tinkercad. As saídas esperadas da tabela não constituem um
registro de execução do simulador. O Python exporta comandos para reprodução
manual; não existe conexão automática em tempo real com o Tinkercad.
