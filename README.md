# Sistema Integrado de Futuro Sustentável em Marte (SIFSM)

Protótipo acadêmico para organizar informações operacionais da colônia Aurora Siger e demonstrar decisões sustentáveis por meio de regras, estruturas de dados, simulação numérica, regressão linear e agentes de IA simulados. O projeto combina componentes executáveis com abstrações didáticas; não representa um sistema certificado para operação real em Marte.

## Arquivos da entrega

| Arquivo/pasta | Conteúdo |
| --- | --- |
| `codigo_fonte.py` | Aplicação principal e menu textual do SIFSM. |
| `src/` | Módulos de banco de dados, lógica, estruturas, simulação, regressão, agentes e alerta energético. |
| `data/script_banco.sql` | Criação da tabela Oracle `modulos_aurora`. |
| `dados_aurora_siger.csv` | Base sintética usada pelo alerta energético e gerada pelo modelo linear. |
| `circuito_logico.png` | Esquema do circuito com nome padronizado para a entrega. |
| `src/simulacao_computacional.py` | Simulação de descarga e estado de carga da bateria. |
| `simulador/alerta_energetico/alerta_energetico.ino` | Sketch para Arduino Uno/Tinkercad, relacionado à regra de alerta. |
| `docs/circuito/` | Esquema, lista de componentes, tabela-verdade, roteiro e registros de validação do circuito. |
| `docs/graficos_ou_imagens/` | Gráficos ilustrativos da simulação e do modelo. |
| `relatorio_tecnico.md` | Relatório técnico completo do protótipo, dados, decisões, limitações e melhorias. |
| `link_video.txt` | Local para registrar o link não listado da apresentação. Substituir o texto de pendência pelo link final antes de compactar a entrega. |
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

## Configuração do banco

1. Crie a tabela executando `data/script_banco.sql` no Oracle.
2. Configure as credenciais e o DSN do Oracle no módulo `src/banco_de_dados.py` antes de usar o CRUD.
3. As opções 1 a 4 do menu dependem do Oracle e de uma rede com acesso ao servidor. Se o banco não estiver disponível, utilize as opções locais e apresente o CRUD como dependente do serviço externo.

**Antes de compartilhar a entrega, substitua qualquer credencial que tenha sido incluída diretamente no código e revogue/rotacione a senha exposta.** Não publique senhas em ZIP, Git ou capturas de tela.

## Como executar

Na raiz do projeto:

```bash
python codigo_fonte.py
```

O menu apresenta as opções de CRUD (1–4, Oracle), regra de irrigação (5), estruturas de dados (6), simulação da bateria (7), modelo linear (8), assistente multiagente simulado (9) e alerta energético/circuito (10). Digite `0` para sair.

Também é possível executar módulos diretamente:

```bash
python src/regras.py
python src/estruturas.py
python src/simulacao_computacional.py
python src/modelagem_linear.py
python src/alerta_energetico.py
python -m unittest discover -s tests -v
```

As simulações e o modelo exibem resultados no terminal e abrem gráficos. O modelo gera/sobrescreve `dados_aurora_siger.csv`; os gráficos são gravados em `docs/graficos_ou_imagens/`. A opção 10 permite avaliar uma leitura manual, o CSV ou imprimir/exportar a tabela-verdade em `data/circuito/`. No modo CSV, os estados de módulo crítico e falha são informados pelo operador, pois não existem nessas colunas do arquivo.

## Circuito lógico

A regra do alerta é `S = (A ∧ B) ∨ C`: A representa consumo no limite ou acima dele, B indica módulo crítico e C indica falha. A saída aciona o LED e o piezo no sketch. O esquema padronizado está em `circuito_logico.png`; consulte também `docs/circuito/README.md` para tabela-verdade, componentes, mapeamento dos pinos e roteiro de reprodução. A comunicação entre Python e o Arduino é demonstrada por comandos seriais copiados manualmente; não há integração em tempo real.

## Escopo acadêmico

Leituras, previsões e respostas dos agentes são didáticas ou sintéticas. O Oracle é uma alternativa de persistência externa; o circuito é uma representação embarcada; os agentes são baseados em regras e respostas predefinidas. Veja `relatorio_tecnico.md` para as premissas, limitações, arquitetura e análise socioambiental.
