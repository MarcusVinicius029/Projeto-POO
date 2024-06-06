import abc
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import numpy as np

class Machine_Learning(abc.ABC):
    """
    Classe abstrata base para modelos de Machine Learning.
    """

    @abc.abstractmethod
    def treina_modelo(self):
        """
        Método abstrato para treinar o modelo.

        """
        pass

    @abc.abstractmethod
    def preve_valores(self):
        """
        Método abstrato para prever valores.

        """
        pass

    @abc.abstractmethod
    def calcula_atributos_do_modelo(self):
        """
        Método abstrato para calcular atributos do modelo.

        """
        pass
   
class Bitcoin_model(Machine_Learning):
    """
    Classe para modelar o preço do Bitcoin utilizando ARIMA.

    Attributes:
    df (DataFrame): DataFrame contendo os dados de preços do Bitcoin.
    modelo_preco (ARIMA): Modelo ARIMA treinado.
    y_pred_tot (Series): Previsões do modelo para todo o período do DataFrame.
    y_pred (Series): Previsões futuras do modelo para o perído n.
    """

    def __init__(self, dataFrame, tipo):
        """
        Inicializa a classe Bitcoin_model com um DataFrame e treina o modelo.

        Parameters:
        dataFrame (DataFrame): DataFrame contendo os dados de mercado do Bitcoin.
        tipo (string): String contendo o nome da coluna alvo
        df_alvo (DataFrame): DataFrame composto pela coluna alvo
        """
        self.df = dataFrame
        self.tipo = tipo
        self.df_alvo = self.df.loc[:, tipo]
        self.treina_modelo()
    
    def treina_modelo(self):
        """
        Treina o modelo ARIMA com os dados de fechamento do preço do Bitcoin.

        Define os atributos modelo_preco e y_pred_tot da classe.
        """
        self.modelo_preco = ARIMA(self.df_alvo, order=(2, 1, 2), freq="D").fit()
        self.y_pred_tot = self.modelo_preco.predict()
    
    def preve_valores(self, X):
        """
        Faz previsões para os próximos períodos usando o modelo treinado.

        Parameters:
        X (int): O número de dias, a partir da data atual, para os quais se deseja fazer a previsão de valor.
        X (str): Data para a qual se quer fazer a previsão (Ano-Mês-Dia).
        X (dateTime): Data para a qual se quer fazer a previsão (Ano-Mês-Ano).

        Returns:
        Series: DataFrame contendo as previsões.
        """
        self.y_pred = self.modelo_preco.forecast(X)
        return round(self.y_pred, 2)
    
    def calcula_atributos_do_modelo(self, n):
        """
        Calcula e retorna atributos do modelo ARIMA.

        Parâmetros:
        n (int): Tipo de atributo a calcular:
            - n = 1: Retorna o erro quadrático médio (MSE) das previsões.
            - n = 2: Retorna os parâmetros do modelo ARIMA.

        Retorna:
        float: O erro quadrático médio (MSE) se n = 1.
        pd.Series: Parâmetros do modelo ARIMA se n = 2.
        None: Se n não for 1 ou 2.
        """
        if n == 1:
            mse = ((self.df_alvo - self.y_pred_tot)**2).mean()
            return mse
        elif n == 2:
            return self.modelo_preco.params
        else:
            return None

class Ethereum_model(Machine_Learning):
    """
    Classe para modelar o preço do Ethereum utilizando ARIMA.

    Attributes:
    df (DataFrame): DataFrame contendo os dados de preços do Ethereum.
    modelo_preco (ARIMA): Modelo ARIMA treinado.
    y_pred_tot (Series): Previsões do modelo para todo o período do DataFrame.
    y_pred (Series): Previsões futuras do modelo para o perído n.
    """

    def __init__(self, dataframe, tipo):
        """
        Inicializa a classe Ethereum_model com um DataFrame e treina o modelo.

        Parameters:
        dataframe (DataFrame): DataFrame contendo dados de mercado do ethereum.
        tipo (string): String contendo o nome da coluna alvo
        df_alvo (DataFram): Dataframe contendo a coluna alvo
        """
        self.df = dataframe
        self.tipo = tipo
        self.df_alvo = self.df[self.tipo]
        self.treina_modelo()

    def treina_modelo(self):
        """
        Treina o modelo ARIMA com os dados de fechamento do preço do Ethereum.

        Define os atributos modelo_preco e y_pred_tot da classe.
        """
        self.modelo_preco = ARIMA(self.df_alvo, freq="D", order=(3, 1, 5)).fit()
        self.y_pred_tot = self.modelo_preco.predict()

    def preve_valores(self, X):
        """
        Faz previsões para os próximos períodos usando o modelo treinado.

        Parameters:
        X (int): O número de dias, a partir da data atual, para os quais se deseja fazer a previsão de valor.
        X (str): Data para a qual se quer fazer a previsão (Ano-Mês-Dia).
        X (dateTime): Data para a qual se quer fazer a previsão (Ano-Mês-Ano).

        Returns:
        Series: DataFrame contendo as previsões.
        """
        self.y_pred = self.modelo_preco.forecast(X)
        return round(self.y_pred, 2)

    def calcula_atributos_do_modelo(self, n):
        """
        Calcula e retorna atributos do modelo ARIMA.

        Parâmetros:
        n (int): Tipo de atributo a calcular:
            - n = 1: Retorna o erro quadrático médio (MSE) das previsões.
            - n = 2: Retorna os parâmetros do modelo ARIMA.

        Retorna:
        float: O erro quadrático médio (MSE) se n = 1.
        pd.Series: Parâmetros do modelo ARIMA se n = 2.
        None: Se n não for 1 ou 2.
        """
        if n == 1:
            sme = ((self.df_alvo - self.y_pred_tot)**2).mean()
            return sme
        elif n == 2:
            return self.modelo_preco.params
        else:
            return None

class Solana_model(Machine_Learning):
    """
    Classe para modelagem de preços da Solana usando ARIMA.

    Esta classe herda de Machine_Learning e implementa métodos específicos
    para treinar o modelo ARIMA, prever valores futuros e calcular atributos do modelo.
    """

    def __init__(self, dataframe, tipo):
        """
        Inicializa a classe Solana_model com um DataFrame e treina o modelo ARIMA.

        Parâmetros:
        dataframe (pd.DataFrame): DataFrame contendo os dados históricos de preços da Solana.
        """
        self.df = dataframe
        self.tipo = tipo
        self.df_alvo = self.df[self.tipo]

        self.treina_modelo()
    
    def treina_modelo(self):
        """
        Treina o modelo ARIMA usando os dados de fechamento do preço da Solana.

        Define os atributos:
        - modelo_preco: O modelo ARIMA treinado.
        - y_pret_tot: Previsões do modelo para os dados de treino.
        """
        self.modelo_preco = ARIMA(self.df_alvo, order=(1, 1, 25)).fit()
        self.y_pret_tot = self.modelo_preco.predict()

    def preve_valores(self, X):
        """
        Faz previsões para os próximos períodos usando o modelo treinado.

        Parameters:
        X (int): O número de dias, a partir da data atual, para os quais se deseja fazer a previsão de valor.
        X (str): Data para a qual se quer fazer a previsão (Ano-Mês-Dia).
        X (dateTime): Data para a qual se quer fazer a previsão (Ano-Mês-Ano).

        Returns:
        Series: DataFrame contendo as previsões.
        """
        self.y_pred = self.modelo_preco.forecast(X)
        return round(self.y_pred, 2)
    
    def calcula_atributos_do_modelo(self, n):
        """
        Calcula e retorna atributos do modelo ARIMA.

        Parâmetros:
        n (int): Tipo de atributo a calcular:
            - n = 1: Retorna o erro quadrático médio (MSE) das previsões.
            - n = 2: Retorna os parâmetros do modelo ARIMA.

        Retorna:
        float: O erro quadrático médio (MSE) se n = 1.
        pd.Series: Parâmetros do modelo ARIMA se n = 2.
        None: Se n não for 1 ou 2.
        """
        if n == 1:
            mse = ((self.df_alvo - self.y_pret_tot)**2).mean()
            return mse
        elif n == 2:
            return self.modelo_preco.params
        else:
            return None
