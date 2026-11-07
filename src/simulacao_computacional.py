import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def executar_simulacao():
    print("--- Iniciando Simulação de Consumo e Bateria ---")
    # Tópico 1.4: Simulação Computacional e Integração Matemática
    # Fenômeno: Descarga da Bateria Principal da Colônia (Aurora Siger)

    # 1. Parâmetros do Sistema
    CAPACIDADE_BATERIA = 5000.0  # Capacidade total em Ampere-hora (Ah)
    TEMPO_SIMULACAO = 24.0       # Ciclo de 24 horas (h)
    SOC_INICIAL = 1.0            # Bateria inicia com 100% de carga (1.0)

    # 2. Modelagem do Consumo (Descarga)
    def corrente_descarga(t):
        """
        Representa a corrente de descarga (Amperes) ao longo do tempo.
        Combina um consumo base da colônia com um pico operacional diurno.
        """
        consumo_base = 120.0
        # Pico que simula alta atividade na colônia usando uma função trigonométrica
        pico_operacional = 80.0 * np.sin(np.pi * t / 24)**2 
        return consumo_base + pico_operacional

    # 3. Execução da Simulação com Tratamento de Erros
    tempos = np.linspace(0, TEMPO_SIMULACAO, 300)
    soc_valores = []
    corrente_valores = corrente_descarga(tempos)

    try:
        print("Iniciando simulação do Estado de Carga (SoC)...")
        
        # Cálculo do SoC iterativo utilizando Integração Numérica (Contagem de Coulomb)
        for t_atual in tempos:
            # A função quad calcula a integral definida (área sob a curva) da corrente
            carga_consumida, erro_est = quad(corrente_descarga, 0, t_atual)
            
            # Fórmula do SoC baseada na integração da corrente
            soc_atual = SOC_INICIAL - (carga_consumida / CAPACIDADE_BATERIA)
            soc_valores.append(max(soc_atual, 0.0))  # Limita o piso da bateria a 0%

        # Integração Matemática: Valor Médio da Função de Consumo
        carga_total_24h, _ = quad(corrente_descarga, 0, TEMPO_SIMULACAO)
        corrente_media = carga_total_24h / TEMPO_SIMULACAO
        
        print(f"Simulação concluída com sucesso.")
        print(f"Carga total consumida em 24h: {carga_total_24h:.2f} Ah")
        print(f"Corrente média de descarga: {corrente_media:.2f} A")

    except Exception as e:
        print(f"Falha na execução da simulação matemática: {e}")

    # 4. Visualização dos Resultados
    plt.figure(figsize=(10, 8))

    # Gráfico 1: Corrente de Descarga e Área sob a Curva
    plt.subplot(2, 1, 1)
    plt.plot(tempos, corrente_valores, label="Corrente de Demanda $I(t)$", color="darkred")
    plt.fill_between(tempos, corrente_valores, alpha=0.3, color="red", 
                     label=r"Carga Consumida $\int I(t) dt$")
    plt.axhline(corrente_media, color="blue", linestyle="--", 
                label=f"Corrente Média ({corrente_media:.1f} A)")
    plt.title("Perfil de Consumo Energético da Aurora Siger (24h)")
    plt.ylabel("Corrente de Descarga (A)")
    plt.legend()
    plt.grid(True)

    # Gráfico 2: Estado de Carga (SoC)
    plt.subplot(2, 1, 2)
    plt.plot(tempos, np.array(soc_valores) * 100, label="Estado de Carga (SoC %)", color="green", linewidth=2)
    plt.axhline(20, color="orange", linestyle="--", label="Alerta de Bateria Baixa (20%)")
    plt.xlabel("Tempo (horas)")
    plt.ylabel("Nível da Bateria (%)")
    plt.ylim(0, 105)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    executar_simulacao()