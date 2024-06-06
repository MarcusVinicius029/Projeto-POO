from .MachineLearning.machineLearning import Bitcoin_model, Ethereum_model, Solana_model
from .Data.data import Bitcoin_data, Ethereum_data, Solana_data, Dolar_data, Criptomoedas_data
import pandas as pd

class DataControler:

    @classmethod
    def get_moeda_df(cls, moeda, time="day", model=False, n=1, atual=False):
        if moeda == "bitcoin":
            if atual == False:        
                cls.bitcoin_data = Bitcoin_data(n, time, model)
                return cls.bitcoin_data.df
            else:
                cls.criptomoedas_data = Criptomoedas_data(n, "BTC", time, atual)
                return cls.criptomoedas_data.df
        elif moeda == "ethereum":
            if atual == False:    
                cls.ethereum_data = Ethereum_data(n, time, model)
                return cls.ethereum_data.df
            else:
                cls.criptomoedas_data = Criptomoedas_data(n, "ETH", time, atual)
                return cls.criptomoedas_data.df
        elif moeda == "solana":
            if atual == False:    
                cls.solana_data = Solana_data(n, time, model)
                return cls.solana_data.df
            else:
                cls.criptomoedas_data = Criptomoedas_data(n, "SOL", time, atual)
                return cls.criptomoedas_data.df
        elif moeda == "dolar":
            cls.dolar_data = Dolar_data(n, atual)
            return cls.dolar_data.df
        else:
            cls.criptomoedas_data = Criptomoedas_data(n, moeda, time, atual)
            return cls.criptomoedas_data.df
        
    @classmethod
    def get_previsao(cls, df, X, moeda, tipo="Price"):
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
