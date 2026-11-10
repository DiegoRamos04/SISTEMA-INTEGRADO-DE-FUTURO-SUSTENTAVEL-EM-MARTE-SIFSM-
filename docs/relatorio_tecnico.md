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
- `data/script_banco.sql`: definição da tabela Oracle.
- `dados_aurora_siger.csv`: base sintética de consumo e características dos módulos, localizada na raiz do projeto.
- `docs/circuito/circuito_logico.png`: cópia do esquema com o nome padronizado para a entrega ZIP.
- `simulador/alerta_energetico/alerta_energetico.ino`: lógica de circuito para Arduino Uno/Tinkercad.
- `docs/circuito/`: pasta contendo o PDF do projeto, README específico, arquivos CSV (como lista de componentes e tabela verdade) e evidências de validação (arquivos .txt).
- `docs/relatorio_tecnico.md`: dentro da pasta docs, temos o nosso relatório técnico, que contempla toda a explicação técnica do projeto.
- `docs/link_video.txt`: arquivo reservado ao link do vídeo; no estado atual contém um lembrete de pendência, não um link publicado.
- `docs/graficos_ou_imagens/`: gráficos gerados pela simulação (simulacao_bateria.png) e pelo modelo (grafico_dispersao.png), além do print de execução do menu do algoritmo (menu_execucao.png).
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

`data/script_banco.sql` cria a tabela Oracle `modulos_aurora`, com `id_modulo` como chave primária de identidade, `nome_modulo`, `consumo_energia` e `status_operacional`. O módulo `src/banco_de_dados.py` prevê as operações CREATE, READ, UPDATE e DELETE: cadastrar, listar, alterar consumo/status e excluir módulo por ID. O CRUD depende de Oracle acessível, driver `oracledb`, credenciais válidas e tabela previamente criada. A execução local sem banco não comprova transações no Oracle. No cadastro, o ID é gerado pela tabela; a interface pede nome, consumo e status.

## 4. Menu e fluxos demonstráveis

Execute `python codigo_fonte.py` na raiz. As opções do menu são:

| Opção | Funcionalidade | Dependência/saída |
| --- | --- | --- |
| 1–4 | CRUD de módulos | Oracle; solicita dados e apresenta resultado/erro |
| 5 | Regra de irrigação | Entrada booleana 0/1 e decisão liberada/bloqueada |
| 6 | Sincronização e estruturas de dados | Lê módulos do Oracle e os carrega em hash e fila; requer conexão Oracle |
| 7 | Simulação de bateria | NumPy, SciPy e Matplotlib; imprime valores e exibe gráfico |
| 8 | Modelo linear de consumo | Pandas, NumPy, scikit-learn, statsmodels e Matplotlib; imprime análise e exibe gráfico |
| 9 | Assistente da colônia | Agentes simulados com roteamento e guardrails |
| 10 | Alerta energético/circuito | Local; leitura manual, CSV ou tabela-verdade; exporta CSV para `data/circuito/` |

O menu principal possui ainda `0` para encerrar. A opção 6 depende do Oracle e não possui fallback local; para demonstrar hash, fila e pilha sem banco, execute `python src/estruturas.py`.

## 5. Regras lógicas e circuito

### 5.1 Irrigação

Em `src/regras.py`, A indica módulo agrícola ativo, B indica umidade adequada e C indica acionamento manual de emergência. A decisão é:

`I = (A ∧ ¬B) ∨ C`

Assim, a irrigação é liberada quando o módulo está ativo e a umidade está baixa, ou quando há acionamento manual de emergência. Entradas diferentes de 0/1 são rejeitadas.

### 5.2 Alerta energético e saída embarcada

Em `src/alerta_energetico.py`, a lógica de criticidade foi modelada para acionar alertas caso ocorra consumo alto simultâneo a um módulo crítico, ou em caso de falha sistêmica. A saída é dada por:

`S = (A ∧ B) ∨ C`

Para representar essa lógica no nível de hardware, o projeto inclui um sketch para prototipagem virtual de IoT com Arduino Uno/Tinkercad. O arquivo `simulador/alerta_energetico/alerta_energetico.ino` lê três entradas digitais (botões), calcula a expressão booleana e aciona atuadores (LED e piezo), além de aceitar comandos seriais. O sketch ainda precisa ser compilado e executado no Tinkercad; até que essa validação seja registrada, o circuito deve ser apresentado como implementação proposta, não como teste concluído.

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

A visualização gráfica detalha o perfil de corrente, a área sob a curva e a respectiva queda do SoC, conforme ilustrado em `(simulacao_bateria.png)`. Vale ressaltar que essa é uma prova de conceito estritamente matemática. Para não fugir do escopo didático, variáveis do mundo real, como eficiência do inversor, recarga solar e desgaste térmico da bateria, ficaram de fora. Ou seja, o script valida a lógica de cálculo via integração, mas não substitui um dimensionamento elétrico real.

O código usa `scipy.integrate.quad` para calcular as integrais; a malha de 300 instantes é usada para desenhar as curvas, não como método de integração. A resolução dessa malha afeta a suavidade visual do gráfico, enquanto a integração numérica é calculada pela rotina de quadratura. Os valores continuam sujeitos às premissas simplificadas do perfil de corrente.

## 8. Modelagem linear

`src/modelagem_linear.py` gera dados sintéticos e ajusta regressão linear múltipla para estimar `Consumo_Energetico` com temperatura externa, quantidade de tripulantes e área do módulo. A relação sintética usada para criar o alvo é aproximadamente:

`Consumo = 50 − 0,6 × Temperatura + 4,5 × Tripulantes + 0,3 × Área + ruído`.

O script exibe estatísticas descritivas e matriz de correlação, separa os registros em 80% para treino e 20% para teste com `train_test_split`, ajusta o modelo somente no conjunto de treino e calcula MSE, MAE e R² no conjunto de teste. Também imprime a interpretação qualitativa dos coeficientes, calcula VIF e salva um gráfico de dispersão em `docs/graficos_ou_imagens/grafico_dispersao.png`. O sinal negativo da temperatura indica que temperaturas mais baixas (mais negativas) elevam o consumo estimado dentro dos dados simulados; os coeficientes de tripulantes e área são positivos por construção.

A separação treino/teste oferece uma avaliação mais informativa do que medir o ajuste nos mesmos dados usados para treinar. Ainda assim, o teste é feito em uma base sintética criada pela mesma fórmula e não comprova desempenho com dados reais. O VIF é calculado e exibido, mas seus valores precisam ser interpretados; calcular essa métrica, por si só, não comprova ausência de multicolinearidade. As unidades e o alvo permanecem didáticos, sem validação física.

## 9. IA integrada por agentes

`src/agentes_ia.py` representa uma arquitetura multiagente inspirada em frameworks modernos de agentes (como o OpenAI Agents SDK), estruturada da seguinte forma:

- Um **input guardrail** bloqueia mensagens curtas ou termos definidos como sensíveis antes do processamento principal. É uma demonstração simples de filtragem, não uma garantia completa de segurança.
- O **agente triador** classifica a intenção da solicitação por palavras-chave em linguagem natural.
- O triador realiza o **handoff** (delegação de controle) para o agente especialista correto (energia, manutenção ou dados).
- Os especialistas retornam textos predefinidos por correspondência de palavras-chave. No código atual, não há funções determinísticas conectadas ao CSV ou ao banco; valores apresentados pelos agentes são exemplos fictícios, não telemetria consultada.
- Um **output guardrail** verifica a resposta final para impedir o vazamento de dados sensíveis.

Os agentes usam regras e textos predefinidos; não consultam de fato o Oracle nem o CSV e não são um modelo generativo autônomo. Sessões (memória de contexto), RAG e ferramentas conectadas são possibilidades conceituais, não funcionalidades implementadas. Recomendações automatizadas devem ser revisadas por uma pessoa, especialmente em assuntos de segurança e suporte à vida.

## 10. Arquitetura computacional e eficiência

Como o SIFSM ainda é um protótipo, o seu volume de processamento atual roda perfeitamente em uma **CPU de propósito geral**. O fluxo principal do sistema, que inclui o CRUD, as regras booleanas e o roteamento dos agentes, junto com as análises matemáticas (NumPy, SciPy, scikit-learn), não exige a capacidade de processamento paralelo de uma **GPU** ou de hardwares dedicados como **NPUs** e **TPUs** (ASICs). Além disso, a hierarquia de memória foi aplicada na prática, em que utilizamos uma tabela hash na memória primária para garantir buscas rápidas em tempo de execução, deixando o armazenamento persistente a cargo do banco Oracle.

Pensando em um cenário real de implantação na colônia Aurora Siger, a arquitetura migraria naturalmente para um modelo de computação heterogênea. As automações de suporte à vida e as regras críticas precisariam rodar localmente (computação na borda) usando microcontroladores ou NPUs, o que garante baixa latência e eficiência energética sem depender de respostas de um servidor central. Por outro lado, o treinamento de modelos preditivos e o processamento pesado da telemetria ficariam nas mãos de aceleradores robustos, como GPUs ou TPUs. 

Para lidar com o gargalo de movimentação de dados e poupar a largura de banda, os dados históricos ficariam retidos no armazenamento secundário, enviando apenas blocos agregados de informação para a camada analítica. Por fim, a infraestrutura central de servidores em Marte tiraria proveito de tecnologias modernas, como **chiplets** e **empilhamento 3D** (a exemplo das memórias HBM). Essa abordagem coloca a memória fisicamente mais perto das unidades de processamento, reduzindo o desperdício de energia e a geração de calor, que são fatores decisivos para manter a colônia sustentável e resiliente.

## 11. Sustentabilidade, cidadania digital e impacto socioambiental

O SIFSM pode ser descrito em três níveis: a **camada física** (representada conceitualmente pelo circuito e módulos), a **camada de controle** (regras lógicas em Python e sketch Arduino) e a **camada analítica** (simulação matemática e regressão). Essa organização ilustra como integrar energia, dados, automação e simulação para apoiar decisões de uso de recursos. Simular hipóteses antes de experimentos físicos pode reduzir desperdício, mas o protótipo não mede essa redução nem controla uma rede inteligente ou armazenamento real.

Do ponto de vista socioambiental, o projeto considera princípios de inovação responsável. Dados operacionais podem revelar rotinas e aspectos privados da tripulação; uma implantação exigiria transparência, retenção mínima e proteção contra usos indevidos. Servidores, redes, armazenamento e IA também podem consumir energia e gerar calor. O protótipo não mede esses impactos; discute como eles deveriam ser considerados ao escolher infraestrutura e processamento.

Por fim, as sugestões autônomas geradas pelo sistema são mantidas sob revisão humana, reforçando que a tecnologia deve ser socialmente responsável, diversa e voltada estritamente para a preservação do equilíbrio e da segurança da vida na colônia Aurora Siger.

## 12. Tratamento de erros e validação

O projeto inclui validação de bits e números no alerta, verificação de CSV e tratamento de exceções em operações de banco, regras, simulação e agentes. `tests/test_alerta.py` cobre as oito combinações da tabela-verdade, casos no limite, falha, entradas inválidas, leitura de CSV e exportação de comandos. O arquivo `docs/circuito/resultado-testes-python.txt` registra uma execução anterior desses testes; isso não equivale a teste do Oracle nem validação física do circuito.

Há blocos `try`/`except` em partes relevantes do banco, das regras, da simulação e dos agentes; alguns fluxos também usam `else` e `finally`. Isso demonstra tratamento de erros no protótipo, mas não garante que todo erro possível seja tratado. Por exemplo, a sincronização da opção 6 depende de conexão Oracle e apenas informa a falha, sem oferecer demonstração local alternativa.

## 13. Limitações e melhorias futuras

- Usar variáveis de ambiente ou gerenciador de segredos para o Oracle e consultas SQL parametrizadas.
- Evoluir a interface textual (CLI/Terminal) para um Dashboard Web interativo.
- Substituir a simulação do Tinkercad e a leitura de arquivos CSV locais por sensores IoT reais.
- Expandir os agentes simulados conectando-os a uma API real de LLM (como OpenAI ou Google Gemini) utilizando arquitetura RAG.
- Validar CRUD no Oracle com dados de teste ou oferecer persistência local equivalente para demonstração sem rede.
- Se a equipe decidir avançar além da simulação, conectar funções determinísticas dos agentes ao CSV/banco, mantendo revisão humana e guardrails.
- Repetir a avaliação do modelo com dados independentes ou reais, se forem disponibilizados, e interpretar os valores de VIF observados.
- Medir uso de recursos computacionais somente em uma implantação de referência, sem atribuir ao protótipo resultados não coletados.

## 14. Síntese

No contexto acadêmico, o SIFSM reúne navegação por menu, CRUD previsto para Oracle, arquivo CSV, regras booleanas, estruturas de dados, simulação matemática, regressão múltipla e agentes simulados, além de discussões sobre arquitetura e sustentabilidade. As funcionalidades são demonstradas em opções separadas; o programa ainda não reúne os resultados em uma análise operacional única com recomendação final.

Algumas partes dependem de infraestrutura externa, como a persistência no Oracle e a validação do circuito no Tinkercad. Nesta etapa, os resultados analíticos usam dados sintéticos e simplificações descritas neste relatório. Assim, o SIFSM deve ser entendido como uma prova de conceito acadêmica, não como um sistema operacional validado para a colônia.
