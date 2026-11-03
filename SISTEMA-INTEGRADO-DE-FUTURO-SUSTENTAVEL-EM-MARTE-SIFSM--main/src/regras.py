def avaliar_irrigacao():
    print("=== SIFSM: Lógica de Irrigação (Módulo Agrícola) ===")
    try:
        # A: Módulo Ativo
        a = int(input("Módulo agrícola ativo? (1 = Sim, 0 = Não): "))
        
        # B: Umidade Adequada
        b = int(input("Umidade do solo adequada? (1 = Sim/Alta, 0 = Não/Baixa): "))
        
        # C: Acionamento Manual
        c = int(input("Acionamento manual de emergência? (1 = Sim, 0 = Não): "))
        
        if a not in (0, 1) or b not in (0, 1) or c not in (0, 1):
            raise ValueError("Valores inválidos. Use estritamente 0 ou 1.")
            
        # Expressão Lógica: I = A AND NOT(B) OR C
        # Representação booleana: I = A . B' + C
        resultado = (a and not b) or c
        
        print("\n--- Resultado da Decisão Lógica ---")
        if resultado:
            print("Ação: Irrigação LIBERADA (Nível Lógico 1).")
        else:
            print("Ação: Irrigação BLOQUEADA (Nível Lógico 0).")
            
        return resultado
        
    except ValueError as erro:
        print(f"Erro de validação: {erro}")
    except Exception as erro:
        print(f"Erro inesperado durante a execução da regra: {erro}")
    finally:
        print("Processamento lógico encerrado.\n")

if __name__ == "__main__":
    avaliar_irrigacao()