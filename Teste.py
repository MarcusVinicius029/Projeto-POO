import pandas as pd 
import requests as req
from datetime import datetime
from SRC.Dados.DataController import DataControler
import os
import matplotlib.pyplot as plt

# class Criptomoedas_data:

#     def __init__(self, n, criptomoeda, time):
#         self.time = time
#         self.criptomoeda = criptomoeda
#         self.n = n
#         try:
#             self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histo{self.time}?fsym={self.criptomoeda}&tsym=BRL&limit={self.n}&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")
#             if self.requisicao.status_code == 200:
#                 self.dados = self.requisicao.json()
#                 if self.dados["Response"] == "Success":
#                     self.corrige_os_dados_externos()
#                     if self.criptomoeda == "BTC" and self.time == "day":
#                         self.salva_os_dados("SRC/Dados/Data/DataSets/bitcoin_data.csv")
#                     elif self.criptomoeda == "ETH" and self.time == "day":
#                         self.salva_os_dados("SRC/Dados/Data/DataSets/ethereum_data.csv")
#                     elif self.criptomoeda == "SOL" and time == "day":
#                         self.salva_os_dados("SRC/Dados/Data/DataSets/solana_data.csv")
#                 else:
#                     raise ValueError("Dados incorretos!")
#             else:
#                 raise ValueError("Problemas na conexão!")
#         except req.exceptions.RequestException:
#             if self.time == "day":
#                 if self.criptomoeda == "BTC":
#                     self.get_dados_internos("SRC/Dados/Data/DataSets/bitcoin_data.csv")
#                 elif self.criptomoeda == "ETH":
#                     self.get_dados_internos("SRC/Dados/Data/DataSets/ethereum_data.csv")
#                 elif self.criptomoeda == "SOL":
#                     self.get_dados_internos("SRC/Dados/Data/DataSets/solana_data.csv")
#                 else:
#                     raise ValueError("Problemas na conexão!")
#             else: 
#                 raise ValueError("Problemas na conexão!")
    
#     def corrige_os_dados_externos(self):
#         self.df = pd.DataFrame([self.dados["Data"]["Data"][n]["time"] for n in range(len(self.dados["Data"]["Data"]))], columns=["time"])
#         self.df["Open"] = [self.dados["Data"]["Data"][n]["open"] for n in range(len(self.dados["Data"]["Data"]))]
#         self.df["High"] = [self.dados["Data"]["Data"][n]["high"] for n in range(len(self.dados["Data"]["Data"]))]
#         self.df["Low"] = [self.dados["Data"]["Data"][n]["low"] for n in range(len(self.dados["Data"]["Data"]))]
#         self.df["Price"] = [self.dados["Data"]["Data"][n]["close"] for n in range(len(self.dados["Data"]["Data"]))]
#         self.df["Volume"] = [self.dados["Data"]["Data"][n]["volumeto"] for n in range(len(self.dados["Data"]["Data"]))]       
#         self.df.time = self.df.time.astype(int)
#         if self.time == "day":
#             for i in range(len(self.df)):
#                     self.df.loc[i, "Data"] = datetime.fromtimestamp(self.df.loc[i, "time"]).date()
#         elif self.time == "hour":
#             for i in range(len(self.df)):
#                     self.df.loc[i, "Data"] = datetime.fromtimestamp(self.df.loc[i, "time"]).time()
#         elif self.time == "minute":
#             for i in range(len(self.df)):
#                 self.df.loc[i, "Data"] = datetime.fromtimestamp(self.df.loc[i, "time"]).minute
        
#         self.df.set_index('Data', inplace=True)
#         self.df = self.df.drop(columns=["time"])

#     def salva_os_dados(self, caminho):
#         relative_path = caminho
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         csv_path = os.path.join(script_dir, relative_path)
#         if os.path.exists(csv_path):
#             self.df.to_csv(csv_path)

#     def get_dados_internos(self, caminho):
#         relative_path = caminho
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         csv_path = os.path.join(script_dir, relative_path)
#         if os.path.exists(csv_path):
#             self.df = pd.read_csv(csv_path, delimiter=",")
#             self.corrige_os_dados_internos()
#         else:
#             raise ValueError("Arquivo não encontrado!")

#     def corrige_os_dados_internos(self):
#             self.df.Data = pd.to_datetime(self.df.Data)
#             self.df.set_index("Data", inplace= True)


# class Previsao_data:
#     def __init__(self, criptomeda):
#         self.criptomoeda = criptomeda
#         if self.criptomoeda == "BTC" or "ETH" or "SOL":
#             try:
#                 self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={self.criptomoeda}&tsym=BRL&allData=true&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")
#                 if self.requisicao.status_code == 200:
#                     self.dados = self.requisicao.json()
#                     if self.dados["Response"] == "Success":
#                         self.corrige_os_dados_externos()
#                         if self.criptomoeda == "BTC":
#                             self.salva_os_dados("SRC/Dados/Data/modelDataSets/bitcoin.csv")
#                         elif self.criptomoeda == "ETH":
#                             self.salva_os_dados("SRC/Dados/Data/modelDataSets/ethereum.csv")
#                         elif self.criptomoeda == "SOL":
#                             self.salva_os_dados("SRC/Dados/Data/modelDataSets/solana.csv")
#                     else:
#                         raise ValueError("Dados incorretos!")
#                 else:
#                     raise ValueError("Problema na conexão!")
#             except req.exceptions.RequestException:
#                 if self.criptomoeda == "BTC":
#                     self.get_dados_internos("SRC/Dados/Data/DataSets/bitcoin_data.csv")
#                 elif self.criptomoeda == "ETH":
#                     self.get_dados_internos("SRC/Dados/Data/DataSets/ethereum_data.csv")
#                 elif self.criptomoeda == "SOL":
#                     self.get_dados_internos("SRC/Dados/Data/DataSets/solana_data.csv")
#         else:
#             raise ValueError("Essa função não está disponível para essa criptomoeda!")
            
#     def corrige_os_dados_externos(self):
#         self.df = pd.DataFrame([self.dados["Data"]["Data"][n]["time"] for n in range(len(self.dados["Data"]["Data"]))], columns=["time"])
#         self.df["Open"] = [self.dados["Data"]["Data"][n]["open"] for n in range(len(self.dados["Data"]["Data"]))]
#         self.df["High"] = [self.dados["Data"]["Data"][n]["high"] for n in range(len(self.dados["Data"]["Data"]))]
#         self.df["Low"] = [self.dados["Data"]["Data"][n]["low"] for n in range(len(self.dados["Data"]["Data"]))]
#         self.df["Price"] = [self.dados["Data"]["Data"][n]["close"] for n in range(len(self.dados["Data"]["Data"]))]
#         self.df["Volume"] = [self.dados["Data"]["Data"][n]["volumeto"] for n in range(len(self.dados["Data"]["Data"]))]       
#         self.df.time = self.df.time.astype(int)
#         for i in range(len(self.df)):
#             self.df.loc[i, "Data"] = datetime.fromtimestamp(self.df.loc[i, "time"]).date()
#         self.df = self.df.loc[2482:, :]      
#         self.df.set_index('Data', inplace=True)
#         self.df = self.df.drop(columns=["time"])
                
#     def salva_os_dados(self, caminho):
#         relative_path = caminho
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         csv_path = os.path.join(script_dir, relative_path)
#         if os.path.exists(csv_path):
#             self.df.to_csv(csv_path)
#         else:
#             raise ValueError("O caminho passado não existe!")

#     def get_dados_internos(self, caminho):
#         relative_path = caminho
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         csv_path = os.path.join(script_dir, relative_path)
#         if os.path.exists(csv_path):
#             self.df = pd.read_csv(csv_path, delimiter=",")
#             self.corrige_os_dados_internos()
#         else:
#             raise ValueError("Arquivo não encontrado!")

#     def corrige_os_dados_internos(self):
#         self.df.Data = pd.to_datetime(self.df.Data)
#         self.df.set_index("Data", inplace= True)

# teste = Previsao_data("BTC")
# teste.df.Price.plot()
# plt.show()


print(type(DataControler.get_moeda_df(1, "dolar", "day", False)))