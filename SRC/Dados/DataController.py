from .MachineLearning.machineLearning import Bitcoin_model, Ethereum_model, Solana_model
from .Data.data import Bitcoin_data, Ethereum_data, Solana_data, Dolar_data
import pandas as pd

class DataControler:
    """
    Classe para controlar e manipular dados e modelos de criptomoedas.

    Esta classe gerencia a inicialização de dados, criação de modelos e previsão de valores 
    para Bitcoin, Ethereum e Solana, além de obter a cotação do dólar.

    Attributes:
        bitcoin_data (Bitcoin_data): Objeto para manipulação de dados da Bitcoin.
        ethereum_data (Ethereum_data): Objeto para manipulação de dados da Ethereum.
        solana_data (Solana_data): Objeto para manipulação de dados da Solana.
        dolar_data (Dolar_data): Objeto para manipulação de dados do dólar.
        b_model (Bitcoin_model): Objeto para previsão de valores da Bitcoin.
        e_model (Ethereum_model): Objeto para previsão de valores da Ethereum.
        s_model (Solana_model): Objeto para previsão de valores da Solana.
    """

    @classmethod
    def get_moeda_df(cls, moeda, model=False, n=10):
        """
        Retorna um DataFrame contendo os dados da moeda especificada.

        Args:
            moeda (str): Nome da moeda ("bitcoin", "ethereum", "solana" ou "dolar").
            model (bool, optional): Indica se o dataFrame será usado em algum modelo. 
                                    Defaut: False.
            n (int, optional): Número de dias passados para o qual se quer obter os dados de mercado.

        Returns:
            pd.DataFrame: DataFrame contendo os dados da moeda especificada.

        """
        if moeda == "bitcoin":    
            cls.bitcoin_data = Bitcoin_data(n, model)
            return cls.bitcoin_data.df
        elif moeda == "ethereum":
            cls.ethereum_data = Ethereum_data(n, model)
            return cls.ethereum_data.df
        elif moeda == "solana":
            cls.solana_data = Solana_data(n, model)
            return cls.solana_data.df
        elif moeda == "dolar":
            cls.dolar_data = Dolar_data(n)
            return cls.dolar_data.df
        else:
            return pd.DataFrame()
        
    @classmethod
    def get_previsao(cls, df, X, moeda, tipo="Price"):
        """
        Retorna a previsão de valores para uma moeda específica.

        Args:
            df (pd.DataFrame): DataFrame contendo os dados históricos da moeda.
            X (array-like): Dados de entrada para a previsão.
            moeda (str): Nome da moeda ("bitcoin", "ethereum" ou "solana").
            tipo (str, optional): Tipo de valor a ser previsto. O padrão é "Price".

        Returns:
            DataFrame: Valores previstos pelo modelo de acordo com o tipo passado.
            -1 (int): Código de erro, indica que o dataFrame passado para a função está vazio
        """
        if df.empty:
            return -1
        elif moeda == "bitcoin":
            cls.b_model = Bitcoin_model(df, tipo)
            return cls.b_model.preve_valores(X)
        elif moeda == "ethereum":
            cls.e_model = Ethereum_model(df, tipo)
            return cls.e_model.preve_valores(X)
        elif moeda == "solana":
            cls.s_model = Solana_model(df, tipo)
            return cls.s_model.preve_valores(X)
        else:
            return -1
