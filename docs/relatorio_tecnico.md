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

Em `src/alerta_energetico.py`, A significa leitura maior ou igual ao limite configurado, B significa módulo crítico e C significa falha. A saída é:

`S = (A ∧ B) ∨ C`

A falha aciona o alerta independentemente dos outros sinais; caso contrário, o alerta exige simultaneamente consumo alto e módulo crítico. A função também valida números finitos e não negativos. Os limites são definidos pelo operador para fins didáticos, não são parâmetros de engenharia. 

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

O sketch `simulador/alerta_energetico/alerta_energetico.ino` lê três botões, calcula a mesma expressão, aciona LED e piezo e aceita os comandos seriais `SET 000` a `SET 111`; `BTN` retorna ao modo de botões. O mapeamento dos pinos e o roteiro estão em `docs/circuito/README.md`. Python exporta os comandos para reprodução manual; não há comunicação automática. A documentação registra testes do código Python, enquanto a validação compilada no Tinkercad deve ser tratada como pendente até que seja executada e registrada.

Embora essa lógica pudesse ser implementada via hardware utilizando circuitos integrados de portas lógicas (como a família 74HC), optou-se pela simulação via microcontrolador (Arduino) devido à maior flexibilidade de integração com o restante do sistema em Python.


## 6. Estruturas de dados

`src/estruturas.py` demonstra três estruturas adequadas a diferentes operações do cenário:

- **Tabela hash (dicionário):** associa código de módulo ao nome e permite busca direta pela chave.
- **Fila FIFO:** organiza chamados de manutenção na ordem de chegada, atendendo primeiro o chamado mais antigo.
- **Pilha LIFO:** mantém ações em ordem inversa de registro, útil para consultar/remover o evento mais recente do histórico.

As estruturas são mantidas em memória durante a execução e não substituem a persistência do banco. O método de “desfazer” remove a última entrada da pilha; não reverte automaticamente a alteração correspondente no banco.

## 7. Simulação computacional e matemática

`src/simulacao_computacional.py` representa a corrente de descarga ao longo de um ciclo de 24 horas por:

`I(t) = 120 + 80 sen²(πt/24)` amperes, para `0 ≤ t ≤ 24 h`.

A bateria tem capacidade didática de 5000 Ah e inicia com estado de carga (SoC) de 100%. A carga consumida até o instante t é calculada por integração numérica da corrente, e o SoC é estimado como `SoC(t) = SoC inicial − carga consumida/capacidade`. A integração total do perfil resulta em 3840 Ah em 24 horas; a corrente média é 160 A e o SoC final estimado é 23,2%, sob as premissas simplificadas do modelo. A implementação usa `scipy.integrate.quad`, gera 300 pontos para visualização e apresenta a linha de referência de bateria baixa em 20%.

O gráfico mostra perfil de corrente, área integrada e evolução do SoC. O modelo não considera eficiência do inversor, tensão variável, recarga solar, temperatura da bateria, envelhecimento, limites de descarga ou variação real de carga. Portanto, é uma demonstração matemática, não dimensionamento de bateria.

## 8. Modelagem linear

`src/modelagem_linear.py` gera dados sintéticos e ajusta regressão linear múltipla para estimar `Consumo_Energetico` com temperatura externa, quantidade de tripulantes e área do módulo. A relação sintética usada para criar o alvo é aproximadamente:

`Consumo = 50 − 0,6 × Temperatura + 4,5 × Tripulantes + 0,3 × Área + ruído`.

O script exibe estatísticas descritivas, matriz de correlação, intercepto e coeficientes ajustados; calcula MSE, MAE e R²; avalia VIF e salva um gráfico de dispersão. O sinal negativo da temperatura indica que temperaturas mais baixas (mais negativas) elevam o consumo estimado dentro dos dados simulados; os coeficientes de tripulantes e área são positivos por construção.

**Limitação de avaliação:** atualmente as métricas são calculadas nos mesmos registros usados para ajustar o modelo. Elas descrevem o ajuste aos dados de treinamento, mas não são uma estimativa independente de desempenho em dados novos. A base é gerada por uma fórmula conhecida com ruído e não representa medições reais. As unidades do CSV são didáticas e devem ser padronizadas antes de qualquer interpretação física.

## 9. IA integrada por agentes

`src/agentes_ia.py` representa uma arquitetura multiagente simples:

1. Um guardrail de entrada bloqueia mensagens curtas ou termos definidos como sensíveis.
2. O agente triador classifica a solicitação por palavras-chave.
3. O triador encaminha (handoff) para especialista em energia, manutenção ou dados.
4. Um guardrail de saída verifica termos que simulam dados sensíveis.
5. A resposta é apresentada no terminal.

Os agentes usam regras e textos predefinidos; não consultam de fato o Oracle, não executam ferramentas externas e não são um modelo generativo. As respostas numéricas fixas são exemplos ilustrativos, não telemetria atual. Sessões e RAG são conceituais, sem recuperação de documentos ou persistência de contexto implementada. Recomendações automatizadas devem ser revisadas por uma pessoa, especialmente em situações de segurança e suporte à vida.

## 10. Arquitetura computacional e eficiência

O volume do protótipo é pequeno e pode ser processado por CPU convencional. CRUD, regras booleanas e roteamento dos agentes não justificam GPU, NPU ou TPU. A CPU executa o fluxo de controle e os cálculos; NumPy/SciPy e scikit-learn processam as análises no tamanho de dados atual. A tabela hash mantém buscas rápidas em memória durante a execução, enquanto o banco Oracle representa persistência entre execuções.

Em uma arquitetura conceitual da colônia, regras críticas poderiam rodar localmente em microcontrolador para reduzir latência e manter automações essenciais durante falhas de comunicação. Dados históricos poderiam permanecer em armazenamento persistente e leituras agregadas/eventos relevantes seriam enviados à camada analítica, reduzindo movimentação de dados. GPU ou aceleradores só seriam avaliados para cargas paralelas maiores, após comparar benefício operacional, consumo elétrico, calor, manutenção e custo computacional. Este protótipo não mede uso de CPU, memória, largura de banda ou energia do processamento; a análise é conceitual.

## 11. Sustentabilidade, cidadania digital e impacto socioambiental

O alerta, a simulação de bateria e a análise de consumo demonstram como regras e cenários podem apoiar o planejamento de recursos. Simular permite comparar hipóteses antes de consumir água, energia ou materiais em experimentos físicos. O histórico de chamados e a execução local de regras podem contribuir para resiliência operacional, mas isso precisaria ser validado com dados de sensores e ensaios reais.

Dados de operação podem revelar horários, hábitos e atividades da tripulação. Uma implantação responsável deve coletar apenas o necessário, limitar acessos, definir retenção, explicar o uso dos dados e permitir revisão humana. Respostas de IA devem ser identificadas como sugestões e não decisões finais. Também se deve avaliar impactos de servidores, redes, armazenamento e IA, incluindo energia, calor, materiais e manutenção. O protótipo usa agentes baseados em regras e evita depender de processamento pesado; diversidade, acessibilidade, transparência e segurança da tripulação devem orientar qualquer evolução.

## 12. Tratamento de erros e validação

O projeto inclui validação de bits e números no alerta, verificação de CSV e tratamento de exceções em operações de banco, regras, simulação e agentes. `tests/test_alerta.py` cobre as oito combinações da tabela-verdade, casos no limite, falha, entradas inválidas, leitura de CSV e exportação de comandos. O arquivo `docs/circuito/resultado-testes-python.txt` registra uma execução anterior desses testes; isso não equivale a teste do Oracle nem validação física do circuito.

## 13. Limitações e melhorias futuras

- Usar variáveis de ambiente ou gerenciador de segredos para o Oracle e consultas SQL parametrizadas.
- Evoluir a interface textual (CLI/Terminal) para um Dashboard Web interativo.
- Substituir a simulação do Tinkercad e a leitura de arquivos CSV locais por sensores IoT reais.
- Expandir os agentes simulados conectando-os a uma API real de LLM (como OpenAI ou Google Gemini) utilizando arquitetura RAG.
- Validar CRUD no Oracle com dados de teste ou oferecer persistência local equivalente para demonstração sem rede.
- Substituir respostas fixas dos agentes por funções determinísticas ligadas ao CSV/banco, mantendo revisão humana e guardrails.
- Medir uso de recursos computacionais somente em uma implantação de referência, sem atribuir ao protótipo resultados não coletados.

## 14. Síntese

O SIFSM demonstra, em escopo acadêmico, os principais conceitos pedidos: menu, CRUD previsto em banco externo, arquivos estruturados, validação, regras booleanas, circuito, estruturas de dados, integração numérica, regressão múltipla, agentes simulados, arquitetura e reflexão socioambiental. As partes que dependem de ambiente externo — Oracle e validação física no Tinkercad — devem ser apresentadas como dependências/propostas enquanto não houver evidência de execução. As conclusões são limitadas pelos dados sintéticos e pelas simplificações descritas neste relatório.
