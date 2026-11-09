# Sistema Integrado de Futuro Sustentável em Marte (SIFSM)

Repositório oficial do projeto desenvolvido para a Fase 7, focado no gerenciamento e na simulação computacional de infraestrutura autossustentável para colônias marcianas (Módulo Aurora Siger).

## 🚀 Tecnologias Utilizadas
* Python (Simulações e Integração com Banco de Dados)
* Oracle Database (Persistência e Estruturação SQL)
* Git & GitHub (Controle de Versão)
## Alerta energético integrado ao Circuit Design

Execute `python codigo_fonte.py` e selecione **10**. A opção funciona sem Oracle
ou bibliotecas externas e permite leitura manual, análise do CSV existente e
exportação da tabela verdade para `data/circuito/`.

A regra é `Alerta = (A e B) ou C`: A indica consumo maior ou igual ao limite;
B indica módulo crítico; C indica falha. Informe leitura e limite na mesma
unidade. O CSV original não informa B/C: os estados fornecidos pelo operador
são aplicados a todas as linhas. Os limites são didáticos e configuráveis.

### Arduino / Tinkercad

Abra o circuito existente e copie o conteúdo de
`simulador/alerta_energetico/alerta_energetico.ino` para o editor de código Texto.
Botões A/B/C: D2/D3/D4 ligados a GND com INPUT_PULLUP. LED: D8 com resistor de
220 ohms em série para GND. Piezo: positivo D9, negativo GND.

Inicie a simulação. No Monitor Serial (9600 baud), envie `SET 110` seguido de
Enter para reproduzir A=1, B=1, C=0. Use a coluna `comando_serial` do CSV para
reproduzir cada leitura. `BTN` devolve o controle aos botões. O LED e o piezo
seguem o alerta. A transferência Python → Tinkercad é manual por comandos;
não há conexão automática em tempo real.

Tabela esperada, em ordem 000 a 111: **0, 1, 0, 1, 0, 1, 1, 1**.

Validação Python: `python -m unittest discover -s tests -v`.
O novo sketch ainda precisa ser compilado e validado no simulador.


## Arquivos do circuito e validação

![Esquema eletrônico exportado do Tinkercad](docs/circuito/esquema-circuito.png)

- [Esquema original em PDF](docs/circuito/Projeto-FIAP.pdf)
- [Lista de componentes exportada](docs/circuito/lista-componentes.csv)
- [Guia da montagem e roteiro de testes](docs/circuito/README.md)
- [Tabela verdade e comandos para o simulador](docs/circuito/tabela-verdade.csv)
- [Resultado dos testes Python](docs/circuito/resultado-testes-python.txt)

O PDF e a lista de componentes são exportações fornecidas pelo autor.
A imagem acima foi renderizada a partir desse PDF. O código Arduino está em
[simulador/alerta_energetico](simulador/alerta_energetico/alerta_energetico.ino).

## 1.7 Arquitetura computacional e eficiência

O protótipo SIFSM pode ser executado em uma CPU convencional. As operações atuais — CRUD dos módulos, avaliação da regra lógica de irrigação, organização de chamados em fila e consultas à tabela hash — são pequenas e sequenciais, portanto não exigem GPU, NPU ou TPU. A CPU é adequada para controlar o fluxo do programa, validar entradas e executar as regras determinísticas.

Na arquitetura proposta para a Aurora Siger, o processamento deve ser distribuído conforme a necessidade. As regras de segurança e automação, como bloquear uma operação diante de uma leitura inválida, devem ser executadas localmente em um controlador embarcado ou microcontrolador. Isso reduz a latência e mantém funções essenciais disponíveis mesmo se a conexão com um servidor central falhar. O armazenamento persistente dos registros pode ficar em um banco de dados local da colônia, com cópias de segurança em outro módulo. A aplicação Python deste repositório representa a camada de controle e análise; o Oracle é a opção de banco prevista no código.

As simulações numéricas e a regressão linear também podem ser executadas na CPU para o volume pequeno de dados usado no protótipo. Uma GPU só seria justificável em análises paralelas maiores, como processamento de imagens ou simulações físicas detalhadas. Uma NPU ou TPU faria sentido apenas se a colônia executasse modelos de IA com grande demanda de inferência; não é requisito para os agentes simulados atuais. Aceleradores aumentam a capacidade em tarefas adequadas, mas têm custo energético e de manutenção, por isso sua adoção deve ser comparada ao benefício obtido.

A hierarquia de memória influencia o desempenho: dados usados repetidamente podem permanecer em memória principal ou cache, enquanto o banco guarda o histórico persistente. Consultas frequentes e transferências excessivas entre sensores, memória, processador e banco podem consumir tempo e energia. A tabela hash demonstrada no projeto favorece a busca por código em memória, enquanto o banco mantém os dados entre execuções. Em uma implantação, convém transmitir leituras agregadas ou eventos relevantes, em vez de movimentar continuamente todo o histórico. O protótipo não mede consumo real de CPU, memória ou aceleradores; essa análise é conceitual e deverá ser validada com medições na infraestrutura escolhida.

## 1.8 Sustentabilidade, cidadania digital e impacto socioambiental

O SIFSM relaciona dados, regras e simulações para apoiar o uso responsável dos recursos da Aurora Siger. A regra de irrigação considera se o módulo agrícola está ativo, a umidade e a solicitação manual; a simulação de bateria estima a evolução da carga diante de um perfil de consumo. Esses recursos podem ajudar a identificar condições de desperdício e comparar decisões antes de aplicá-las na colônia. Como os valores usados são simulados, as saídas são apoio à análise e não substituem medições físicas ou validação da tripulação.

A simulação permite testar cenários sem gastar água, energia ou materiais em experimentos reais. Associada ao armazenamento e à automação local, pode apoiar o planejamento de energia e a resiliência: regras críticas continuam operando mesmo com falha de comunicação, e o histórico de eventos ajuda a investigar problemas. Para tornar esse benefício verificável, uma implantação futura deverá comparar previsões com leituras reais e registrar os erros e as limitações dos modelos.

Os registros operacionais podem revelar hábitos, horários e atividades da tripulação. Por isso, os dados devem ser limitados ao necessário para a operação, ter acesso controlado e ser mantidos pelo tempo adequado. Relatórios devem explicar quais informações são coletadas e como são usadas, permitindo transparência e revisão humana. As credenciais do banco não devem ficar expostas no código-fonte; devem ser fornecidas por configuração segura e protegidas contra acesso indevido.

O processamento também tem impacto ambiental: servidores, armazenamento, redes e modelos de IA consomem energia e exigem equipamentos e materiais. No protótipo, os agentes são baseados em regras e não dependem de um modelo pesado, o que evita processamento desnecessário. Caso a solução evolua para IA ou infraestrutura acelerada, a equipe deverá avaliar se o ganho operacional compensa energia, calor, manutenção e recursos utilizados. A tecnologia deve ser acessível e inclusiva, com decisões relevantes explicáveis e supervisão humana, evitando que sugestões automatizadas prejudiquem pessoas ou priorizem eficiência em detrimento da segurança e da dignidade da tripulação.

