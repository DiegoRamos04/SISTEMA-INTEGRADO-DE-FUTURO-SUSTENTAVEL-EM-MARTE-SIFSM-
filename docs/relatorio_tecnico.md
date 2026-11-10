# Relatório técnico — SIFSM / Aurora Siger

## 1. Identificação e objetivo

O Sistema Integrado de Futuro Sustentável em Marte (SIFSM) é um protótipo acadêmico para demonstrar como dados operacionais, regras lógicas e análises computacionais podem apoiar a gestão de uma colônia marciana fictícia, a Aurora Siger. O escopo foi mantido didático: dados são sintéticos ou informados pelo operador, a IA é simulada por regras e o circuito é apresentado por um sketch compatível com Arduino Uno/Tinkercad. O sistema não controla infraestrutura real nem substitui decisões humanas.

O protótipo reúne cadastro de módulos, análise de consumo, regra de alerta, organização de chamados e histórico, simulação de bateria, regressão linear e um fluxo multiagente demonstrativo.

## 2. Organização dos arquivos

- `codigo_fonte.py`: menu e ponto de entrada da aplicação, localizado na raiz do projeto.
- `src/banco_de_dados.py`: conexão Oracle e CRUD de módulos.
- `src/regras.py`: regra booleana de irrigação.
- `src/estruturas.py`: tabela hash, fila e pilha.
- `src/alerta_energetico.py`: avaliação de telemetria/CSV, tabela-verdade e exportação de comandos seriais.
- `src/simulacao_computacional.py`: modelo de descarga da bateria e gráficos.
- `src/modelagem_linear.py`: geração/análise de dados e regressão múltipla.
- `src/agentes_ia.py`: triagem, agentes especialistas, handoffs e guardrails simulados.
- `data/circuito/script_banco.sql`: definição da tabela Oracle (movido para dentro de data/circuito).
- `dados_aurora_siger.csv`: base sintética de consumo e características dos módulos, localizada na raiz do projeto.
- `docs/circuito/circuito_logico.png`: cópia do esquema com o nome padronizado para a entrega ZIP.
- `simulador/alerta_energetico/alerta_energetico.ino`: lógica de circuito para Arduino Uno/Tinkercad.
- `docs/circuito/`: pasta contendo o PDF do projeto, README específico, arquivos CSV (como lista de componentes e tabela verdade) e evidências de validação (arquivos .txt).
- `docs/graficos_ou_imagens/`: gráficos gerados pela simulação (simulacao_bateria.png) e pelo modelo (grafico_dispersao.png), além do arquivo link_video.txt e o próprio relatorio_tecnico.md.
- `tests/`: diretório contendo os testes do projeto, incluindo test_alerta.py.

## 3. Dados e armazenamento

### 3.1 Base CSV

`dados_aurora_siger.csv` contém 200 registros sintéticos e quatro campos:

| Campo | Significado | Unidade/observação |
| --- | --- | --- |
| `Temperatura_Externa` | Temperatura externa simulada | °C; valores gerados entre -80 e -20 |
| `Tripulantes` | Quantidade simulada de ocupantes | pessoas; valores inteiros entre 2 e 9 |
| `Tamanho_Modulo` | Área simulada do módulo | m²; valores entre 50 e 150 |
| `Consumo_Energetico` | Consumo sintético calculado com ruído | variável do exercício; a unidade deve ser tratada como didática |

A geração usa semente aleatória fixa (`42`) para permitir reproduzir os mesmos dados. O modelo linear regenera o CSV ao ser executado. O arquivo não contém estado de criticidade nem falha; por isso, o módulo de alerta pede esses valores ao operador em vez de inferi-los.

### 3.2 Banco relacional e CRUD

`data/script_banco.sql` cria a tabela Oracle `modulos_aurora`, com `id_modulo` como chave primária de identidade, `nome_modulo`, `consumo_energia` e `status_operacional`. O módulo `src/banco_de_dados.py` prevê as operações CREATE, READ, UPDATE e DELETE: cadastrar, listar, alterar consumo/status e excluir módulo por ID. O CRUD depende de Oracle acessível, driver `oracledb`, credenciais válidas e tabela previamente criada. A execução local sem banco não comprova transações no Oracle.

As credenciais devem ser fornecidas por configuração segura e nunca incluídas na entrega pública. Antes de distribuir o projeto, substituir credenciais eventualmente presentes no código e rotacionar senhas já expostas.

## 4. Menu e fluxos demonstráveis

Execute `python codigo_fonte.py` na raiz. As opções do menu são:

| Opção | Funcionalidade | Dependência/saída |
| --- | --- | --- |
| 1–4 | CRUD de módulos | Oracle; solicita dados e apresenta resultado/erro |
| 5 | Regra de irrigação | Entrada booleana 0/1 e decisão liberada/bloqueada |
| 6 | Estruturas de dados | Demonstra busca hash, fila FIFO e pilha LIFO |
| 7 | Simulação de bateria | NumPy, SciPy e Matplotlib; imprime valores e exibe gráfico |
| 8 | Modelo linear de consumo | Pandas, NumPy, scikit-learn, statsmodels e Matplotlib; imprime análise e exibe gráfico |
| 9 | Assistente da colônia | Agentes simulados com roteamento e guardrails |
| 10 | Alerta energético/circuito | Local; leitura manual, CSV ou tabela-verdade; exporta CSV para `data/circuito/` |

O menu principal possui ainda `0` para encerrar. Também é possível executar cada módulo separadamente; os comandos estão no README.

## 5. Regras lógicas e circuito

### 5.1 Irrigação

Em `src/regras.py`, A indica módulo agrícola ativo, B indica umidade adequada e C indica acionamento manual de emergência. A decisão é:

`I = (A ∧ ¬B) ∨ C`

Assim, a irrigação é liberada quando o módulo está ativo e a umidade está baixa, ou quando há acionamento manual de emergência. Entradas diferentes de 0/1 são rejeitadas.

### 5.2 Alerta energético e saída embarcada

Em `src/alerta_energetico.py`, a lógica de criticidade foi modelada para acionar alertas caso ocorra consumo alto simultâneo a um módulo crítico, ou em caso de falha sistêmica. A saída é dada por:

`S = (A ∧ B) ∨ C`

Para validar essa lógica no nível de hardware sem riscos físicos, o projeto utiliza a prototipagem virtual de IoT por meio do Tinkercad. O sketch `simulador/alerta_energetico/alerta_energetico.ino` representa um microcontrolador (Arduino) que lê três entradas digitais (botões), calcula a expressão booleana e aciona atuadores (LED e piezo), além de aceitar comandos seriais. Essa abordagem demonstra como uma decisão computacional de eficiência e segurança é traduzida para automação embarcada na camada física.

| A | B | C | S |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |

O mapeamento dos pinos e o roteiro de uso estão descritos em `docs/circuito/README.md`. Vale destacar que o script em Python apenas exporta os comandos para reprodução manual, pois não há comunicação automática em tempo de execução. Enquanto a documentação registra os testes do código Python, a validação compilada no Tinkercad deve ser tratada como pendente até que seja totalmente executada e registrada.

Embora essa lógica pudesse ser implementada via hardware utilizando circuitos integrados de portas lógicas (como a família 74HC), optou-se pela simulação via microcontrolador (Arduino) devido à maior flexibilidade de integração com o restante do sistema em Python.


## 6. Estruturas de dados

`src/estruturas.py` demonstra três estruturas adequadas a diferentes operações do cenário:

- **Tabela hash (dicionário):** associa código de módulo ao nome e permite busca direta pela chave.
- **Justificativa:** Diferente de uma busca linear em listas, a função hash transforma a chave em um índice, permitindo busca rápida (complexidade O(1)) e acesso direto aos módulos operacionais, essencial para respostas em tempo real.

- **Fila FIFO:** organiza chamados de manutenção na ordem de chegada, atendendo primeiro o chamado mais antigo.
- **Justificativa:** Em um ambiente crítico como uma colônia marciana, o suporte técnico ou os chamados de manutenção devem seguir uma regra justa e sequencial. A estrutura de Fila garante o princípio FIFO, assegurando que as solicitações da tripulação não sejam negligenciadas e que quem acionou o sistema primeiro seja o primeiro a ter seu problema resolvido.

- **Pilha LIFO:** mantém ações em ordem inversa de registro, útil para consultar/remover o evento mais recente do histórico.
- **Justificativa:** Sistemas de controle frequentemente exigem o registro de ações para permitir auditorias ou a função de "desfazer" falhas operacionais. A estrutura de Pilha aplica a lógica natural do princípio LIFO, onde a última ação realizada pelo sistema ou operador fica no topo, sendo a primeira a ser acessada e desfeita em caso de necessidade. As estruturas são mantidas em memória durante a execução e não substituem a persistência do banco. O método de “desfazer” remove a última entrada da pilha; não reverte automaticamente a alteração correspondente no banco.

Dessa forma, o protótipo do SIFSM demonstra que sistemas reais não dependem de uma única estrutura de dados, combinando de forma orquestrada a busca rápida da Tabela Hash, a fila de atendimento FIFO e a pilha de histórico LIFO para resolver cada parte do problema com a solução mais adequada.

## 7. Simulação computacional e matemática

`src/simulacao_computacional.py` representa a corrente de descarga ao longo de um ciclo de 24 horas por:

`I(t) = 120 + 80 sen²(πt/24)` amperes, para `0 ≤ t ≤ 24 h`.

A bateria tem capacidade didática de 5000 Ah e inicia com estado de carga (SoC) de 100%. A carga consumida até o instante t é calculada por integração numérica da corrente, e o SoC é estimado como `SoC(t) = SoC inicial − carga consumida/capacidade`. A integração total do perfil resulta em 3840 Ah em 24 horas; a corrente média é 160 A e o SoC final estimado é 23,2%, sob as premissas simplificadas do modelo. A implementação usa `scipy.integrate.quad`, gera 300 pontos para visualização e apresenta a linha de referência de bateria baixa em 20%.

A visualização gráfica detalha o perfil de corrente, a área sob a curva e a respectiva queda do SoC [simulacao_bateria.png](docs/graficos_ou_imagens/simulacao_bateria.png). Vale ressaltar que essa é uma prova de conceito estritamente matemática. Para não fugir do escopo didático, variáveis do mundo real, como eficiência do inversor, recarga solar e desgaste térmico da bateria, ficaram de fora. Ou seja, o script valida a lógica de cálculo via integração, mas não substitui um dimensionamento elétrico real.

Na parte de cálculo, a malha de tempo foi configurada com passos curtos e controlados. Essa precaução evita instabilidades numéricas comuns em discretizações (como os erros acumulados por intervalos muito largos no método de Euler). Esse cuidado garante que a estimativa de consumo faça sentido físico e não crie anomalias na linha do tempo da colônia.

## 8. Modelagem linear

`src/modelagem_linear.py` gera dados sintéticos e ajusta regressão linear múltipla para estimar `Consumo_Energetico` com temperatura externa, quantidade de tripulantes e área do módulo. A relação sintética usada para criar o alvo é aproximadamente:

`Consumo = 50 − 0,6 × Temperatura + 4,5 × Tripulantes + 0,3 × Área + ruído`.

O script exibe estatísticas descritivas, matriz de correlação, intercepto e coeficientes ajustados; calcula MSE, MAE e R²; avalia VIF e salva um gráfico de dispersão [grafico_dispersao.png](docs/graficos_ou_imagens/grafico_dispersao.png). O sinal negativo da temperatura indica que temperaturas mais baixas (mais negativas) elevam o consumo estimado dentro dos dados simulados; os coeficientes de tripulantes e área são positivos por construção.

Seguindo as premissas de modelagem de regressão linear múltipla, a análise de correlação e a verificação de fatores de inflação de variância (VIF) asseguram que as variáveis explicativas selecionadas não apresentam redundância crítica ou multicolinearidade excessiva, garantindo a estabilidade e a interpretabilidade dos coeficientes obtidos.

## 9. IA integrada por agentes

`src/agentes_ia.py` representa uma arquitetura multiagente inspirada em frameworks modernos de agentes (como o OpenAI Agents SDK), estruturada da seguinte forma:

- Um **input guardrail** atua como tripwire, bloqueando mensagens curtas ou termos definidos como sensíveis antes do processamento principal, garantindo a segurança do sistema.
- O **agente triador** classifica a intenção da solicitação por palavras-chave em linguagem natural.
- O triador realiza o **handoff** (delegação de controle) para o agente especialista correto (energia, manutenção ou dados).
- O especialista acessa funções determinísticas (**function tools** simuladas) para garantir que as respostas numéricas respeitem os registros oficiais do sistema (CSVs e banco de dados), impedindo alucinações de telemetria.
- Um **output guardrail** verifica a resposta final para impedir o vazamento de dados sensíveis.

Os agentes usam regras e textos predefinidos; não consultam de fato o Oracle e não são um modelo generativo autônomo. Sessões (memória de contexto) e RAG são conceituais. Recomendações automatizadas devem ser revisadas por uma pessoa, respeitando o princípio de que a IA integrada deve atuar sob supervisão em ambientes de suporte à vida.

## 10. Arquitetura computacional e eficiência

Como o SIFSM ainda é um protótipo, o seu volume de processamento atual roda perfeitamente em uma **CPU de propósito geral**. O fluxo principal do sistema, que inclui o CRUD, as regras booleanas e o roteamento dos agentes, junto com as análises matemáticas (NumPy, SciPy, scikit-learn), não exige o paralelismo massivo de uma **GPU** ou de hardwares dedicados como **NPUs** e **TPUs** (ASICs). Além disso, a hierarquia de memória foi aplicada na prática, em que utilizamos uma tabela hash na memória primária para garantir buscas rápidas em tempo de execução, deixando o armazenamento persistente a cargo do banco Oracle.

Pensando em um cenário real de implantação na colônia Aurora Siger, a arquitetura migraria naturalmente para um modelo de computação heterogênea. As automações de suporte à vida e as regras críticas precisariam rodar localmente (computação na borda) usando microcontroladores ou NPUs, o que garante baixa latência e eficiência energética sem depender de respostas de um servidor central. Por outro lado, o treinamento de modelos preditivos e o processamento pesado da telemetria ficariam nas mãos de aceleradores robustos, como GPUs ou TPUs. 

Para lidar com o gargalo de movimentação de dados e poupar a largura de banda, os dados históricos ficariam retidos no armazenamento secundário, enviando apenas blocos agregados de informação para a camada analítica. Por fim, a infraestrutura central de servidores em Marte tiraria proveito de tecnologias modernas, como **chiplets** e **empilhamento 3D** (a exemplo das memórias HBM). Essa abordagem coloca a memória fisicamente mais perto das unidades de processamento, reduzindo o desperdício de energia e a geração de calor, que são fatores decisivos para manter a colônia sustentável e resiliente.

## 11. Sustentabilidade, cidadania digital e impacto socioambiental

O SIFSM reflete uma arquitetura de integração dividida em três níveis: a **camada física** (representada pelo circuito e módulos), a **camada de controle** (regras lógicas em Python e automação local) e a **camada analítica** (simulação matemática e regressão). A articulação dessas camadas demonstra como a integração entre energia, dados, automação e simulação contribui diretamente para o uso responsável dos recursos. Ao simular hipóteses em ambiente virtual antes de consumir insumos físicos, o sistema otimiza a operação e apoia uma colônia mais autônoma e resiliente, utilizando redes inteligentes e armazenamento para lidar com contingências.

Do ponto de vista institucional, o projeto alinha-se aos princípios **ESG** (Ambiental, Social e de Governança), assumindo uma postura de inovação responsável. A cidadania digital e a economia dos dados são tratadas com rigor, reconhecendo que dados operacionais podem revelar a rotina e a privacidade da tripulação, o que exige transparência, retenção mínima e proteção contra usos indevidos. Além disso, ao otimizar processos localmente e evitar processamentos desnecessários, o sistema mitiga os impactos ambientais (como consumo de energia e dissipação de calor) gerados por infraestruturas de IA e data centers. 

Por fim, as sugestões autônomas geradas pelo sistema são mantidas sob revisão humana, reforçando que a tecnologia deve ser socialmente responsável, diversa e voltada estritamente para a preservação do equilíbrio e da segurança da vida na colônia Aurora Siger.

## 12. Tratamento de erros e validação

O projeto inclui validação de bits e números no alerta, verificação de CSV e tratamento de exceções em operações de banco, regras, simulação e agentes. `tests/test_alerta.py` cobre as oito combinações da tabela-verdade, casos no limite, falha, entradas inválidas, leitura de CSV e exportação de comandos. O arquivo `docs/circuito/resultado-testes-python.txt` registra uma execução anterior desses testes; isso não equivale a teste do Oracle nem validação física do circuito.

As operações de banco de dados, regras e simulação utilizam blocos estruturados de `try` e `except` para capturar falhas operacionais e de conexão (como `ValueError` ou falhas no Oracle) sem abortar o sistema abruptamente, empregando também `else` para fluxos de sucesso e `finally` para encerramentos seguros de operação, garantindo a estabilidade exigida na infraestrutura.

## 13. Limitações e melhorias futuras

- Usar variáveis de ambiente ou gerenciador de segredos para o Oracle e consultas SQL parametrizadas.
- Evoluir a interface textual (CLI/Terminal) para um Dashboard Web interativo.
- Substituir a simulação do Tinkercad e a leitura de arquivos CSV locais por sensores IoT reais.
- Expandir os agentes simulados conectando-os a uma API real de LLM (como OpenAI ou Google Gemini) utilizando arquitetura RAG.
- Validar CRUD no Oracle com dados de teste ou oferecer persistência local equivalente para demonstração sem rede.
- Substituir respostas fixas dos agentes por funções determinísticas ligadas ao CSV/banco, mantendo revisão humana e guardrails.
- Medir uso de recursos computacionais somente em uma implantação de referência, sem atribuir ao protótipo resultados não coletados.

## 14. Síntese

No contexto acadêmico, o SIFSM cumpriu o que propôs ao amarrar bem as tecnologias estudadas ao longo da fase. O projeto integrou a navegação via menu no terminal, as operações de CRUD integradas ao banco e a arquivos auxiliares, além de validações com tratamento de erros. A prática mostrou que dá para conectar regras lógicas booleanas à automação embarcada, organizar o fluxo da colônia usando estruturas de dados adequadas (tabelas hash, filas e pilhas) e embasar as decisões com simulações matemáticas e modelos de regressão múltipla. O sistema também incorporou conceitos de arquitetura de hardware, fluxos multiagentes inteligentes e uma reflexão crítica sobre sustentabilidade e cidadania digital.

Cabe destacar que algumas partes dependem de infraestruturas externas, como a persistência no Oracle e a validação física dos circuitos no Tinkercad, funcionando nesta etapa como dependências ou modelos conceituais de simulação. Além disso, as análises dependem de bases de dados sintéticas e das simplificações assumidas no projeto. No fim das contas, a entrega funciona como uma prova de conceito coesa para apoiar a gestão e a autonomia da colônia Aurora Siger.
