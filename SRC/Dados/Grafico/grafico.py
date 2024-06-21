import matplotlib.pyplot as plt

class Graficos:
    """
    Classe para gerar gráficos de valores e previsões de preços utilizando matplotlib.

    Métodos:
        gerar_grafico_de_valores(df): Gera um gráfico de linha ou dispersão dos valores ao longo do tempo.
        gerar_grafico_de_previsao(y_pred, df): Gera um gráfico de linha com a previsão dos valores e os valores reais.
    """

    def gerar_grafico_de_valores(self, df):
        """
        Gera um gráfico de linha ou de dispersão dos valores ao longo do tempo.

        Args:
            df (pandas.DataFrame): DataFrame contendo os dados a serem plotados, com uma coluna 'Price' para os valores.
        """
        # Verifica se há mais de um ponto de dados para determinar o tipo de gráfico a ser gerado
        if len(df) > 1:
            momentos = df.index.values

            # Converte os índices para string para facilitar a rotulagem no gráfico
            for n in range(len(df.index.values)):
                momentos[n] = str(momentos[n])

            # Configura e plota o gráfico de linha
            plt.figure(figsize=(10, 6))
            plt.plot(momentos, df['Price'], marker='o', color='b', linestyle='-', linewidth=2, markersize=8, label="Preço")

            # Configurações do gráfico
            plt.title('Valores ao longo do tempo')
            plt.xlabel('Data')
            plt.ylabel('Valor')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.grid(True)
            plt.legend()
            plt.show()
        else:
            # Caso haja apenas um ponto de dados, plota um gráfico de dispersão
            momento = str(df.index[0])
            valor = df['Price']

            plt.figure(figsize=(10, 6))
            plt.scatter(momento, valor, color="b", label='Preço', s=100)
            plt.title('Valores ao longo do tempo')
            plt.xlabel('Data')
            plt.ylabel('Preço')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.grid(True)
            plt.legend()
            plt.show()

    def gerar_grafico_de_previsao(self, y_pred, df):
        """
        Gera um gráfico de linha com a previsão dos valores e os valores reais.

        Args:
            y_pred (pandas.Series): Série contendo os valores previstos.
            df (pandas.DataFrame): DataFrame contendo os valores reais, com uma coluna 'Price'.
        """
        # Verifica se há mais de um ponto de previsão para determinar o tipo de gráfico a ser gerado
        if len(y_pred) != 1:
            dias = sorted(set(y_pred.index) | set(df.index))
            
            # Configura e plota o gráfico de linha com previsão e valores reais
            plt.figure(figsize=(10, 6))
            plt.title('Valores e Previsão!')
            plt.scatter(y_pred.index, y_pred, color="Orange", s=100, label="Previsão")
            plt.plot(df.index, df, marker='o', color='b', linestyle='-', linewidth=2, markersize=8, label="Preço")
            plt.xticks(dias, rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.grid(True)
            plt.show()
        else:
            # Caso haja apenas um ponto de previsão, plota um gráfico de dispersão
            dia = y_pred.index.values
            valor = y_pred.Price
            dias = sorted(set(y_pred.index) | set(df.index))
            
            plt.figure(figsize=(10, 6))
            plt.title('Valores e Previsão!')
            plt.scatter(dia, valor, color="Orange", s=100, label="Previsão")
            plt.plot(df.index, df, marker='o', color='b', linestyle='-', linewidth=2, markersize=8, label="Preço")
            plt.xticks(dias, rotation=45)
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()
