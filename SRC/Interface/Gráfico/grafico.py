import matplotlib.pyplot as plt
import pandas as pd

class GraphPlotter:
    """
    Classe para plotar dados coletados e dados previstos de preços e volumes de vendas.

    Attributes:
    -----------
    collected_data : pd.DataFrame
        DataFrame contendo os dados coletados, com um índice de datas e colunas 'price' e 'vol'.
    predicted_data : list or array
        Lista ou array contendo os dados previstos.

    Methods:
    --------
    plot_previsao():
        Plota os dados coletados e os dados previstos de preços no mesmo gráfico.
    plot_volume_de_vendas():
        Plota os dados coletados e os dados previstos de volumes de vendas no mesmo gráfico.
    """
    def __init__(self, collected_data, predicted_data):
        """
        Inicializa a classe com os dados coletados e os dados previstos.

        Parameters:
        -----------
        collected_data : pd.DataFrame
            DataFrame contendo os dados coletados, com um índice de datas e colunas 'price' e 'vol'.
        predicted_data : list or array
            Lista ou array contendo os dados previstos.
        """
        self.collected_data = collected_data.tail(5).loc[::-1]
        self.predicted_data = predicted_data

    def plot_previsao(self):
        """
        Plota os dados coletados e os dados previstos de preços no mesmo gráfico.

        O gráfico gerado mostra os preços coletados e os previstos ao longo do tempo.
        """
        plt.figure(figsize=(10, 5))
        plt.plot(self.collected_data.price, label='Dados Coletados', color='blue')
        plt.plot(self.predicted_data, label='Dados Previstos', color='green')
        plt.title('Dados Coletados e Previstos')
        plt.xlabel('Tempo')
        plt.ylabel('Valor')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def plot_volume_de_vendas(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.collected_data.vol, label='Dados Coletados', color='blue')
        plt.plot(self.predicted_data, label='Dados Previstos', color='green')
        plt.title('Dados Coletados e Previstos')
        plt.xlabel('Tempo')
        plt.ylabel('Valor')
        plt.legend()
        plt.grid(True)
        plt.show()
    
