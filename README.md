# Sistema Integrado de Futuro Sustentável em Marte (SIFSM)

Protótipo acadêmico para organizar informações operacionais da colônia Aurora Siger e demonstrar decisões sustentáveis por meio de regras, estruturas de dados, simulação numérica, regressão linear e agentes de IA simulados. O projeto combina componentes executáveis com abstrações didáticas; não representa um sistema certificado para operação real em Marte.

## Arquivos da entrega

| Arquivo/pasta | Conteúdo |
| --- | --- |
| `codigo_fonte.py` | Aplicação principal e menu textual do SIFSM. |
| `src/` | Módulos de banco de dados, lógica, estruturas, simulação, regressão, agentes e alerta energético. |
| `data/script_banco.sql` | Criação da tabela Oracle `modulos_aurora`. |
| `dados_aurora_siger.csv` | Base sintética usada pelo alerta energético e gerada pelo modelo linear. |
| `docs/circuito/circuito_logico.png` | Esquema do circuito. |
| `src/simulacao_computacional.py` | Simulação de descarga e estado de carga da bateria. |
| `simulador/alerta_energetico/alerta_energetico.ino` | Sketch para Arduino Uno/Tinkercad, relacionado à regra de alerta. |
| `docs/circuito/` | Esquema, lista de componentes, tabela-verdade, roteiro e registros de validação do circuito. |
| `docs/graficos_ou_imagens/` | Gráficos ilustrativos da simulação e do modelo. |
| `docs/relatorio_tecnico.md` | Relatório técnico completo do protótipo, dados, decisões, limitações e melhorias. |
| `docs/link_video.txt` | Local para registrar o link não listado da apresentação. Substituir o texto de pendência pelo link final antes de compactar a entrega. |
| `tests/test_alerta.py` | Testes automatizados da regra energética e da exportação CSV. |

## Requisitos

- Python 3.10 ou superior.
- Pacotes: `numpy`, `pandas`, `matplotlib`, `scipy`, `scikit-learn`, `statsmodels` e `oracledb`.
- Oracle Database acessível somente para as opções de CRUD. As demais demonstrações são locais, mas os módulos de análise requerem os pacotes indicados.

Instale os pacotes em um ambiente virtual:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
python -m pip install numpy pandas matplotlib scipy scikit-learn statsmodels oracledb
```

## Configuração do banco de dados Oracle

O esquema está em `data/script_banco.sql`; execute-o no Oracle antes de usar o CRUD. As opções 1 a 4 e a sincronização da opção 6 dependem de uma conexão Oracle funcional. A opção 6 carrega os módulos do banco para as estruturas em memória; sem Oracle, ela apresenta erro e não executa uma demonstração local alternativa. Para demonstrar apenas as estruturas sem banco, execute `python src/estruturas.py`.

Sem Oracle, as opções 5, 7, 8, 9 e 10 são locais, desde que as dependências Python estejam instaladas.

## Como executar

Na raiz do projeto:

```bash
python codigo_fonte.py
```
## Navegação no Menu SIFSM
Ao iniciar o programa, será apresentado um menu com 10 opções principais. Abaixo, um resumo de como utilizar cada bloco do sistema:

- Opções de 1 a 4 (Gestão de Dados / CRUD): Cadastram, listam, alteram e excluem módulos no Oracle. O ID é gerado pelo banco; no cadastro, informe nome, consumo e status.
- Opção 5 (Regra Booleana de Irrigação): Solicita três entradas 0/1 — módulo ativo, umidade adequada e acionamento manual — e informa se a irrigação é liberada.
- Opção 6 (Sincronização e Estruturas de Dados): Lê os módulos do Oracle e demonstra seu carregamento na tabela hash e na fila de inspeção. Requer banco disponível; para demonstração autônoma das estruturas, execute `python src/estruturas.py`.
- Opção 7 (Simulação Computacional): Executa o modelo numérico de descarga de bateria da colônia, gerando e exibindo gráficos temporais que são salvos na pasta docs/graficos_ou_imagens/.
- Opção 8 (Modelagem Linear): Executa a geração de dados, treino, separação de base de teste e avaliação da regressão múltipla do consumo energético. Esta etapa gera automaticamente o arquivo dados_aurora_siger.csv.
- Opção 9 (Assistente de IA / Sistema Multiagente): Testa o agente triador simulado, que avalia a solicitação da tripulação, aciona guardrails (regras de escopo) e faz o handoff para agentes especialistas (Energia, Manutenção, etc.).
- Opção 10 (Alerta Energético e Circuito Lógico): Demonstra a regra booleana (A e B) ou C. Permite testar leituras manuais, processar lotes via CSV ou gerar a Tabela Verdade, simulando a comunicação serial para o Arduino/Tinkercad.
  
Também é possível executar módulos diretamente:

```bash
python src/regras.py
python src/estruturas.py
python src/simulacao_computacional.py
python src/modelagem_linear.py
python src/alerta_energetico.py
```

As simulações e o modelo exibem resultados no terminal e abrem gráficos. O modelo gera/sobrescreve `dados_aurora_siger.csv`; os gráficos são gravados em `docs/graficos_ou_imagens/`. A opção 10 permite avaliar uma leitura manual, o CSV ou imprimir/exportar a tabela-verdade em `data/circuito/`. No modo CSV, os estados de módulo crítico e falha são informados pelo operador, pois não existem nessas colunas do arquivo.

## Rodando os testes automatizados
Para validar a integridade das lógicas de alerta, utilize o comando de testes nativo do Python:

```bash
python -m unittest discover -s tests -v
```
## Circuito lógico

A regra do alerta é `S = (A ∧ B) ∨ C`: A representa consumo no limite ou acima dele, B indica módulo crítico e C indica falha. A saída aciona o LED e o piezo no sketch. O esquema está em `docs/circuito/circuito_logico.png`; consulte também `docs/circuito/README.md` para tabela-verdade, componentes, mapeamento dos pinos e roteiro de reprodução. A comunicação entre Python e o Arduino é demonstrada por comandos seriais copiados manualmente; não há integração em tempo real e a validação no Tinkercad ainda está pendente.

## Escopo acadêmico

Leituras, previsões e respostas dos agentes são didáticas ou sintéticas. O Oracle é uma persistência externa; o circuito é uma representação embarcada; os agentes usam regras e respostas predefinidas, sem consulta real aos dados. Veja `docs/relatorio_tecnico.md` para as premissas, limitações, arquitetura e análise socioambiental. O link de vídeo está em `docs/link_video.txt` e precisa ser substituído pelo link real antes da entrega.
