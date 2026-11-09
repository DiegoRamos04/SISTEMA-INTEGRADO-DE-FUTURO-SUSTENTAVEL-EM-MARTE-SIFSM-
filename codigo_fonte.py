import os
import subprocess
import sys
from pathlib import Path
from src.alerta_energetico import executar_alerta
# Oracle é opcional para as funções locais e para o circuito.
try:
    import src.banco_de_dados as db
except ModuleNotFoundError as erro_db:
    if erro_db.name not in ('oracledb', 'pandas'):
        raise
    db = None

RAIZ = Path(__file__).resolve().parent

def executar_script(nome):
    subprocess.run([sys.executable, str(RAIZ / 'src' / nome)], cwd=RAIZ)

import src.estruturas as estruturas
import src.agentes_ia as agentes_ia
def sincronizar_banco_estruturas():
    print("\n--- Sincronizando Oracle DB com Memória Interna (Hash/Fila) ---")
    
    # 1. CORREÇÃO: O nome da classe no estruturas.py é EstruturasSIFSM
    sistema_memoria = estruturas.EstruturasSIFSM() 
    
    try:
        conexao = db.conectar()
        cursor = conexao.cursor()
        
        # 2. CORREÇÃO: Nome da tabela (modulos_aurora) e coluna (nome_modulo)
        cursor.execute("SELECT id_modulo, nome_modulo FROM modulos_aurora") 
        registros = cursor.fetchall()
        
        for linha in registros:
            id_mod = linha[0]
            nome_mod = linha[1]
            
            sistema_memoria.cadastrar_modulo_hash(id_mod, nome_mod)
            
            # 3. CORREÇÃO: O método correto no estruturas.py é enfileirar_chamado
            sistema_memoria.enfileirar_chamado(f"Inspeção de rotina: {nome_mod}")
            
        print(f"Sucesso: {len(registros)} módulos carregados do Oracle para a Tabela Hash e Fila!")
        
        print("\n[Estado atual da Tabela Hash]")
        sistema_memoria.exibir_hash() 
        
        print("\n[Estado atual da Fila de Operações]")
        sistema_memoria.exibir_fila()

    except Exception as e:
        print(f"Erro ao sincronizar com o banco de dados: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals():
            conexao.close()

def limpar_tela():
    # Limpa o terminal dependendo do sistema operacional
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    while True:
        limpar_tela()
        print("=" * 55)
        print(" SIFSM: SISTEMA INTEGRADO DE FUTURO SUSTENTÁVEL")
        print("                 AURORA SIGER - MARTE              ")
        print("=" * 55)
        print("\n[ OPERAÇÕES DE BANCO DE DADOS ]")
        print(" 1 - Cadastrar Módulo na Colônia")
        print(" 2 - Listar Status dos Módulos")
        print(" 3 - Alterar Dados do Módulo")
        print(" 4 - Excluir Módulo")
        
        print("\n[ LÓGICA E ESTRUTURAS DE DADOS ]")
        print(" 5 - Avaliar Regra Lógica (Irrigação do Módulo Agrícola)")
        print(" 6 - Executar Estruturas de Dados (Fila, Pilha e Hash)")
        
        print("\n[ SIMULAÇÕES E INTELIGÊNCIA ARTIFICIAL ]")
        print(" 7 - Simulação Computacional (Descarga de Bateria)")
        print(" 8 - Modelagem Linear (Previsão de Consumo Energético)")
        print(" 9 - Assistente Virtual da Colônia (IA Simulada)")
        print("10 - Alerta Energético / Circuito Tinkercad (Python + Arduino)")
        print("\n" + "=" * 55)
        print(" 0 - Encerrar Sistema")
        
        escolha = input("\nEscolha uma opção -> ")
        
        if escolha in ('1', '2', '3', '4') and db is None:
            print("Banco indisponível: execute: python -m pip install oracledb pandas.")
            input("Pressione ENTER para continuar...")
            continue

        if escolha == '1':
            print("\n--- NOVO MÓDULO ---")
            nome = input("Nome do módulo (Ex: Habitação, Laboratório): ")
            consumo = input("Consumo de energia (kW): ")
            status = input("Status operacional (Ex: Nominal, Crítico): ")
            db.cadastrar_modulo(nome, consumo, status)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '2':
            db.listar_modulos()
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '3':
            print("\n--- ALTERAR MÓDULO ---")
            id_mod = input("Digite o ID do módulo a ser alterado: ")
            novo_consumo = input("Novo consumo (kW): ")
            novo_status = input("Novo status: ")
            db.alterar_modulo(id_mod, novo_consumo, novo_status)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '4':
            print("\n--- EXCLUIR MÓDULO ---")
            id_mod = input("Digite o ID do módulo a ser excluído: ")
            db.excluir_modulo(id_mod)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '5':
            limpar_tela()
            print("Iniciando avaliação da regra lógica do sistema...\n")
            # Executa o script de regras
            executar_script("regras.py")
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '6':
            limpar_tela()
            print("Demonstrando operação das Estruturas de Dados...\n")
            # Executa o script de estruturas
            executar_script("estruturas.py")
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '7':
            limpar_tela()
            print("Calculando Simulação de Bateria e gerando gráficos (Aguarde)...\n")
            # Dica: Feche a janela do gráfico do matplotlib para o terminal continuar
            executar_script("simulacao_computacional.py")
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '8':
            limpar_tela()
            print("Treinando Modelo de Regressão Linear Múltipla e gerando gráfico...\n")
            # Dica: Feche a janela do gráfico do matplotlib para o terminal continuar
            executar_script("modelagem_linear.py")
            input("\nPressione ENTER para continuar...")

        elif escolha == '9':
           print("\n--- Assistente Virtual Aurora Siger ---")
           print("Digite 'sair' para voltar ao menu.")
           while True:
               pergunta = input("Você: ")
               if pergunta.lower() == 'sair':
                   break
               agentes_ia.processar_solicitacao_ia(pergunta)
            
        elif escolha == '10':
            executar_alerta()
            input("\nPressione ENTER para continuar...")

        elif escolha == '0':
            print("\nEncerrando o SIFSM. Até a próxima missão em Marte!")
            break
            
        else:
            print("\nOpção inválida! Tente novamente digitando um número de 0 a 10.")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    menu_principal()