from .MachineLearning.machineLearning import Bitcoin_model, Solana_model, Ethereum_model
from .Data.data import Criptomoedas_data, Dolar_data, Previsao_data
from .Grafico.grafico import Graficos


class DataControler:
    """
    Classe para controle e obtenção de dados relacionados a criptomoedas, dólar e previsões.

    Métodos estáticos permitem acessar e manipular os dados conforme necessário.
    """

    @classmethod
    def get_moeda_df(cls, n: int, moeda: str, time: str, atual=False):
        """
        Obtém um DataFrame com os dados da moeda especificada.

        Args:
            n (int): Número de (minutos, horas ou dias) anteriores ao momento atual.
            moeda (str): Nome da criptomoeda ("BTC", "ETH", "SOL") ou "dolar".
            time (str): Período de tempo dos dados ("day", "hour", "minute").
            atual (bool, opcional): Se True, obtém os dados mais recentes. Padrão é False.

        Returns:
            pandas.DataFrame: DataFrame contendo os dados da moeda especificada.

        Raises:
            ValueError: Se a moeda especificada não for suportada ou se houver problemas na conexão.
        """
        if moeda != "dolar":
            # Obtém dados da criptomoeda especificada
            criptomoedas_data = Criptomoedas_data(n, moeda, time)
            return criptomoedas_data.df
        else:
            # Obtém dados do dólar
            dolar_data = Dolar_data(n, atual)
            return dolar_data.df

    @classmethod
    def get_previsao(cls, moeda: str, n=1, tipo="Price"):
        """
        Obtém previsões para a moeda especificada utilizando modelos de Machine Learning.

        Args:
            moeda (str): Nome da criptomoeda ("BTC", "ETH", "SOL").
            n (int, opcional): Número de previsões a serem realizadas. Padrão é 1.
            tipo (str, opcional): Tipo de previsão desejada ("Price" ou outro especificado pelo modelo).

        Returns:
            list: Lista de previsões para o tipo especificado.

        Raises:
            ValueError: Se a moeda especificada não for suportada para previsão.
        """
        # Obtém dados de previsão para a criptomoeda especificada
        previsao_df = Previsao_data(moeda).df
        if moeda == "BTC":
            modelo_btc = Bitcoin_model(previsao_df, tipo)
            return modelo_btc.preve_valores(n)
        elif moeda == "ETH":
            modelo_eth = Ethereum_model(previsao_df, tipo)
            return modelo_eth.preve_valores(n)
        elif moeda == "SOL":
            modelo_sol = Solana_model(previsao_df, tipo)
            return modelo_sol.preve_valores(n)
        else:
            raise ValueError(f"Previsão não suportada para a moeda {moeda}.")

    @classmethod
    def get_grafico_df(cls, moeda: str, n: int, time: str):
        """
        Gera e exibe um gráfico dos valores da moeda especificada ao longo do tempo.

        Args:
            moeda (str): Nome da criptomoeda ("BTC", "ETH", "SOL") ou "dolar".
            n (int): Número de (minutos, horas ou dias) anteriores ao momento atual.
            time (str): Período de tempo dos dados ("day", "hour", "minute").
        """
        # Cria um gráfico de valores para a moeda especificada
        grafico = Graficos()
        grafico.gerar_grafico_de_valores(cls.get_moeda_df(n, moeda, time))

    @classmethod
    def get_grafico_previsao(cls, moeda: str, n=1):
        """
        Gera e exibe um gráfico com os valores reais e as previsões da moeda especificada.

        Args:
            moeda (str): Nome da criptomoeda ("BTC", "ETH", "SOL").
            n (int, opcional): Número de previsões a serem realizadas. Padrão é 1.

        Raises:
            ValueError: Se a moeda especificada não for suportada para previsão.
        """
        if moeda in ["BTC", "SOL", "ETH"]:
            # Obtém previsões e dados reais para a moeda especificada
            y_pred = cls.get_previsao(moeda, n)
            df = cls.get_moeda_df(7, moeda, time="day")
            grafico = Graficos()
            grafico.gerar_grafico_de_previsao(y_pred, df.Price)
        else:
            raise ValueError(f"{moeda} não está disponível para previsão!")
