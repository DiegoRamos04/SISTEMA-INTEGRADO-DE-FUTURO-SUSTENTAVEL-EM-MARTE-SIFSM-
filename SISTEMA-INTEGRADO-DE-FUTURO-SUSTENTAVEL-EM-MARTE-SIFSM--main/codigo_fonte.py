import src.banco_de_dados as db
import os

def limpar_tela():
    # Limpa o terminal dependendo do sistema operacional
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    while True:
        limpar_tela()
        print("---- SIFSM: MÓDULOS AURORA SIGER ----")
        print("1 - Cadastrar Módulo")
        print("2 - Listar Módulos")
        print("3 - Alterar Módulo")
        print("4 - Excluir Módulo")
        print("5 - Sair")
        
        escolha = input("\nEscolha -> ")
        
        if escolha == '1':
            nome = input("Nome do módulo (Ex: Habitação, Laboratório): ")
            consumo = input("Consumo de energia (kW): ")
            status = input("Status operacional (Ex: Nominal, Crítico): ")
            db.cadastrar_modulo(nome, consumo, status)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '2':
            db.listar_modulos()
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '3':
            id_mod = input("Digite o ID do módulo a ser alterado: ")
            novo_consumo = input("Novo consumo (kW): ")
            novo_status = input("Novo status: ")
            db.alterar_modulo(id_mod, novo_consumo, novo_status)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '4':
            id_mod = input("Digite o ID do módulo a ser excluído: ")
            db.excluir_modulo(id_mod)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '5':
            print("\nEncerrando o SIFSM...")
            break
            
        else:
            print("\nOpção inválida! Tente novamente.")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    menu_principal()