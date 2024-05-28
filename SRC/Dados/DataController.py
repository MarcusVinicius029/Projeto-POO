from .MachineLearning.machineLearning import Bitcoin_model, Ethereum_model, Solana_model
from .Data.data import Bitcoin_data, Ethereum_data, Solana_data, Dolar_data

class DataControler:
    """
    Classe para controlar e manipular dados e modelos de criptomoedas.

    Esta classe gerencia a inicialização de dados, criação de modelos e previsão de valores 
    para Bitcoin, Ethereum e Solana, além de obter a cotação do dólar.
    """

    @classmethod
    def start(cls, endereco_datasets):
        """
        Inicializa os dados e modelos para Bitcoin, Ethereum e Solana.

        Parâmetros:
        endereco_datasets (list): Lista de strings com os endereços dos datasets para 
                                  Bitcoin, Ethereum e Solana, respectivamente.
        
        Atributos de Classe:
        bitcoin_data: Instância de Bitcoin_data.
        ethereum_data: Instância de Ethereum_data.
        solana_data: Instância de Solana_data.
        dolar_data: Instância de Dolar_data.
        bitcoin_df: DataFrame contendo os dados do Bitcoin.
        ethereum_df: DataFrame contendo os dados do Ethereum.
        solana_df: DataFrame contendo os dados do Solana.
        b_model: Instância de Bitcoin_model.
        e_model: Instância de Ethereum_model.
        s_model: Instância de Solana_model.
        """
        cls.bitcoin_data = Bitcoin_data(endereco_datasets[0])
        cls.ethereum_data = Ethereum_data(endereco_datasets[1])
        cls.solana_data = Solana_data(endereco_datasets[2])
        cls.dolar_data = Dolar_data()

        cls.bitcoin_df = cls.bitcoin_data.df
        cls.ethereum_df = cls.ethereum_data.df
        cls.solana_df = cls.solana_data.df

        cls.b_model = Bitcoin_model(cls.bitcoin_df)
        cls.e_model = Ethereum_model(cls.ethereum_df)
        cls.s_model = Solana_model(cls.solana_df)

    @classmethod
    def previsao_bitcoin(cls, X):
        """
        Faz a previsão de valores futuros do Bitcoin.

        Parâmetros:
        X (int, str, dateTime): O número de dias a partir da data atual, ou uma data específica 
                                (no formato "Ano-Mês-Dia"), para a qual se deseja fazer a previsão.

        Retorna:
        pd.Series: Previsões de valores futuros do Bitcoin.
        """
        return cls.b_model.preve_valores(X)
    
    @classmethod
    def obtem_prm_b_model(cls, n):
        """
        Obtém parâmetros ou métricas do modelo de Bitcoin.

        Parâmetros:
        n (int): Tipo de parâmetro ou métrica a ser retornada:
                 - n = 1: Retorna o erro quadrático médio (MSE) das previsões.
                 - n = 2: Retorna os parâmetros do modelo ARIMA.

        Retorna:
        float ou pd.Series: O erro quadrático médio (MSE) se n = 1, ou os parâmetros do modelo 
                            ARIMA se n = 2.
        """
        return cls.b_model.calcula_atributos_do_modelo(n)

    @classmethod
    def previsao_ethereum(cls, X):
        """
        Faz a previsão de valores futuros do Ethereum.

        Parâmetros:
        X (int, str, dateTime): O número de dias a partir da data atual, ou uma data específica 
                                (no formato "Ano-Mês-Dia"), para a qual se deseja fazer a previsão.

        Retorna:
        pd.Series: Previsões de valores futuros do Ethereum.
        """
        return cls.e_model.preve_valores(X)
    
    @classmethod
    def obtem_prm_e_model(cls, n):
        """
        Obtém parâmetros ou métricas do modelo de Ethereum.

        Parâmetros:
        n (int): Tipo de parâmetro ou métrica a ser retornada:
                 - n = 1: Retorna o erro quadrático médio (MSE) das previsões.
                 - n = 2: Retorna os parâmetros do modelo ARIMA.

        Retorna:
        float ou pd.Series: O erro quadrático médio (MSE) se n = 1, ou os parâmetros do modelo 
                            ARIMA se n = 2.
        """
        return cls.e_model.calcula_atributos_do_modelo(n)
    
    @classmethod
    def previsao_solana(cls, X):
        """
        Faz a previsão de valores futuros da Solana.

        Parâmetros:
        X (int, str, dateTime): O número de dias a partir da data atual, ou uma data específica 
                                (no formato "Ano-Mês-Dia"), para a qual se deseja fazer a previsão.

        Retorna:
        pd.Series: Previsões de valores futuros da Solana.
        """
        return cls.s_model.preve_valores(X)
    
    @classmethod
    def obtem_prm_s_model(cls, n):
        """
        Obtém parâmetros ou métricas do modelo de Solana.

        Parâmetros:
        n (int): Tipo de parâmetro ou métrica a ser retornada:
                 - n = 1: Retorna o erro quadrático médio (MSE) das previsões.
                 - n = 2: Retorna os parâmetros do modelo ARIMA.

        Retorna:
        float ou pd.Series: O erro quadrático médio (MSE) se n = 1, ou os parâmetros do modelo 
                            ARIMA se n = 2.
        """
        return cls.s_model.calcula_atributos_do_modelo(n)
    
    @classmethod
    def get_cotacao_dolar(cls, n):
        """
        Obtém a cotação do dólar.

        Parâmetros:
        n (int): O número de cotações a serem obtidas.

        Retorna:
        DataFrame: DataFrame com as cotações dos n dias anteriores.
        """
        return cls.dolar_data.get_cotacao(n)
