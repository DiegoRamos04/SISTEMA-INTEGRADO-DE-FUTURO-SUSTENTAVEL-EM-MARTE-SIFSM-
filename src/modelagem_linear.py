import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor

def executar_modelo():
    print("--- Iniciando Previsão Energética (Modelagem Linear) ---")
    # 1. Geração de dados simulados

    np.random.seed(42)
    n_amostras = 200

    # Variáveis explicativas (X)
    temperatura_externa = np.random.uniform(-80, -20, n_amostras) # Temperatura em Marte (°C)
    tripulantes = np.random.randint(2, 10, n_amostras)            # Quantidade de pessoas no módulo
    tamanho_modulo = np.random.uniform(50, 150, n_amostras)       # Área do módulo em m²

    # Variável resposta (y) com ruído aleatório para simular a realidade
    # Lógica: Menor temperatura (mais negativa) exige mais aquecimento, mais tripulantes e maior área gastam mais energia
    consumo_energia = (50 
                       - 0.6 * temperatura_externa 
                       + 4.5 * tripulantes 
                       + 0.3 * tamanho_modulo 
                       + np.random.normal(0, 4, n_amostras)) # Ruído

    # Criação do DataFrame e salvamento (simulando a leitura de um arquivo do projeto)
    df = pd.DataFrame({
        'Temperatura_Externa': temperatura_externa,
        'Tripulantes': tripulantes,
        'Tamanho_Modulo': tamanho_modulo,
        'Consumo_Energetico': consumo_energia
    })
    df.to_csv('dados_aurora_siger.csv', index=False)

    # 2. Análise exploratória dos dados 

    print("--- Estrutura dos Dados ---")
    df.info()
    print("\n--- Estatísticas Descritivas ---")
    print(df.describe())

    print("\n--- Matriz de Correlação ---")
    print(df.corr())


    # 3. Construção do modelo de Regressão Múltipla 
    X = df[['Temperatura_Externa', 'Tripulantes', 'Tamanho_Modulo']]
    y = df['Consumo_Energetico']
    model = LinearRegression()
    model.fit(X, y)

    print("\n--- Equação do Modelo ---")
    print(f"Intercepto: {model.intercept_:.4f}")
    print(f"Coeficientes: {model.coef_}")


    # 4. Avaliação do modelo 

    y_pred = model.predict(X)

    mse = mean_squared_error(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    print("\n--- Métricas de Avaliação ---")
    print(f"MSE: {mse:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"R²: {r2:.4f}")
    print("\n--- Interpretação dos Coeficientes e Unidades ---")
    print("1. Temperatura (°C): Coeficiente negativo.")
    print("   -> Quanto mais frio, maior o gasto com aquecimento.")
    print("2. Tripulantes (pessoas): Coeficiente positivo.")
    print("   -> Cada pessoa extra eleva o suporte à vida.")
    print("3. Tamanho (m²): Coeficiente positivo.")
    print("   -> Módulos maiores exigem mais energia.")
    print(f"4. Avaliação (R² = {r2:.2f}):")
    print("   -> O modelo explica a variação do consumo (kWh didático).")

    # 5. Verificação de multicolinearidade (VIF)

    print("\n--- Verificação de VIF ---")
    vif = pd.DataFrame()
    vif['Variável'] = X.columns
    vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    print(vif)

    # Gráfico de dispersão (Exemplo: Tripulantes vs Consumo)
    print("\nGerando gráfico de dispersão...")
    plt.scatter(df['Tripulantes'], df['Consumo_Energetico'], color='blue', alpha=0.6)
    plt.title('Tripulantes vs Consumo Energético na Aurora Siger')
    plt.xlabel('Número de Tripulantes')
    plt.ylabel('Consumo Energético (kWh)')
    plt.savefig("docs/graficos_ou_imagens/grafico_dispersao.png")
    plt.show()

if __name__ == "__main__":
    executar_modelo()
