import os
import subprocess
import src.banco_de_dados as db 
import src.estruturas as estruturas
import src.agentes_ia as agentes_ia
def sincronizar_banco_estruturas():
    print("\n--- Sincronizando Oracle DB com Memória Interna (Hash/Fila) ---")
    
    # 1. Instancia as estruturas (substitua 'Sistema' pelo nome exato da sua classe no estruturas.py)
    sistema_memoria = estruturas.Sistema() 
    
    try:
        # 2. Abre conexão e busca os dados reais
        conexao = db.conectar() # Use a sua função de conexão real do banco_de_dados.py
        cursor = conexao.cursor()
        
        # Ajuste 'modulos' e os nomes das colunas para os que você usa na sua tabela Oracle
        cursor.execute("SELECT id_modulo, nome FROM modulos") 
        registros = cursor.fetchall()
        
        # 3. Carrega os dados nas Estruturas de Dados
        for linha in registros:
            id_mod = linha[0]
            nome_mod = linha[1]
            
            # Alimenta a Tabela Hash
            sistema_memoria.cadastrar_modulo_hash(id_mod, nome_mod)
            
            # Simula a entrada do módulo na Fila de Processamento/Manutenção
            sistema_memoria.adicionar_fila(f"Inspeção de rotina: {nome_mod}")
            
        print(f"Sucesso: {len(registros)} módulos carregados do Oracle para a Tabela Hash e Fila!")
        
        # 4. Demonstra os dados carregados na memória
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
        print("\n" + "=" * 55)
        print(" 0 - Encerrar Sistema")
        
        escolha = input("\nEscolha uma opção -> ")
        
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
            subprocess.run(["python", "regras.py"])
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '6':
            limpar_tela()
            print("Demonstrando operação das Estruturas de Dados...\n")
            # Executa o script de estruturas
            subprocess.run(["python", "estruturas.py"])
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '7':
            limpar_tela()
            print("Calculando Simulação de Bateria e gerando gráficos (Aguarde)...\n")
            # Dica: Feche a janela do gráfico do matplotlib para o terminal continuar
            subprocess.run(["python", "simulação computacional.py"])
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '8':
            limpar_tela()
            print("Treinando Modelo de Regressão Linear Múltipla e gerando gráfico...\n")
            # Dica: Feche a janela do gráfico do matplotlib para o terminal continuar
            subprocess.run(["python", "modelagem_linear.py"])
            input("\nPressione ENTER para continuar...")

        elif escolha == '9':
           print("\n--- Assistente Virtual Aurora Siger ---")
           print("Digite 'sair' para voltar ao menu.")
           while True:
               pergunta = input("Você: ")
               if pergunta.lower() == 'sair':
                   break
               agentes_ia.processar_solicitacao_ia(pergunta)
            
        elif escolha == '0':
            print("\nEncerrando o SIFSM. Até a próxima missão em Marte!")
            break
            
        else:
            print("\nOpção inválida! Tente novamente digitando um número de 0 a 8.")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    menu_principal()