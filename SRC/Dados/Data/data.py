import pandas as pd
from datetime import datetime
import abc
import matplotlib.pyplot as plt
import requests as req
import os


class Dados(abc.ABC):
    """
    Classe abstrata para manipulação de dados externos.
    """

    def __inti__(self, n, model = False):
        pass

    @abc.abstractmethod
    def corrige_os_dados_externos(self):
        """
        Método abstrato para corrigir os dados externos.

        Este método deve ser implementado pelas subclasses para realizar qualquer correção necessária nos dados externos.
        """
        pass

    @abc.abstractmethod
    def corrige_os_dados_internos(self):
        """
        Método abstrato para corrigir os dados internos.

        Este método deve ser implementado pelas subclasses para carregar os dados internos salvos em disco.
        """
        pass

class Bitcoin_data(Dados):
    def __init__(self, n, time, model):

        self.model = model
        self.time = time
        try:
            if model:
                self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=BRL&allData=true&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")
            else:
                self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histo{self.time}?fsym=BTC&tsym=BRL&limit={n}&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")

            if self.requisicao.status_code == 200:
                self.dados = self.requisicao.json()
                self.corrige_os_dados_externos()
            else:
                if self.time == "day":    
                    if model:
                        relative_path = "modelDataSets/bitcoin.csv"
                    else:
                        relative_path = "DataSets/bitcoin_data.csv"
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    csv_path = os.path.join(script_dir, relative_path)
                    if os.path.exists(csv_path):
                        self.df = pd.read_csv(csv_path)
                        self.corrige_os_dados_internos()
                elif self.time == "hour" and self.model == False:
                    relative_path = "DataSets_hour/bitcoin_hour.csv"
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    csv_path = os.path.join(script_dir, relative_path)
                    if os.path.exists(csv_path):
                        self.df = pd.read_csv(csv_path)
                        self.corrige_os_dados_internos()

        except req.exceptions.RequestException:
            if self.time == "day":    
                if model:
                    relative_path = "modelDataSets/bitcoin.csv"
                else:
                    relative_path = "DataSets/bitcoin_data.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df = pd.read_csv(csv_path)
                    self.corrige_os_dados_internos()
            elif self.time == "hour" and self.model == False:
                relative_path = "DataSets_hour/bitcoin_hour.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df = pd.read_csv(csv_path)
                    self.corrige_os_dados_internos()

    def corrige_os_dados_externos(self):
        self.df = pd.DataFrame([self.dados["Data"]["Data"][n]["time"] for n in range(len(self.dados["Data"]["Data"]))], columns=["time"])
        self.df["Open"] = [self.dados["Data"]["Data"][n]["open"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["High"] = [self.dados["Data"]["Data"][n]["high"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Low"] = [self.dados["Data"]["Data"][n]["low"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Price"] = [self.dados["Data"]["Data"][n]["close"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Volume"] = [self.dados["Data"]["Data"][n]["volumeto"] for n in range(len(self.dados["Data"]["Data"]))]  
        if self.time == "day":
            self.df.time = self.df.time.astype(int)
            self.df["Data"] = pd.to_datetime(self.df.time)
            for n in range(len(self.df)):
                self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"]).date()

            self.df = self.df.drop(columns=["time"])
            self.df.set_index('Data', inplace=True)
            self.df = self.df.iloc[::-1]
            self.df = self.df.asfreq("D")
            if self.model == False:
                relative_path = "DataSets/bitcoin_data.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df.to_csv(csv_path)
            elif self.model:
                relative_path = "modelDataSets/bitcoin.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df.to_csv(csv_path)            
        elif self.time == "hour" and self.model == False:
            self.df.time = self.df.time.astype(int)
            self.df["Data"] = pd.to_datetime(self.df.time)
            for n in range(len(self.df)):
                self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"])

            self.df = self.df.drop(columns=["time"])
            self.df.set_index('Data', inplace=True)
            relative_path = "DataSets_hour/bitcoin_hour.csv"
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, relative_path)
            if os.path.exists(csv_path):
                    self.df.to_csv(csv_path)

    def corrige_os_dados_internos(self):
        if self.time == "day":
            self.df.Data = pd.to_datetime(self.df.Data)
            self.df.set_index("Data", inplace= True)
            self.df = self.df.asfreq("D")
        else:
            self.df.Data = pd.to_datetime(self.df.Data)
            self.df.set_index("Data", inplace= True)   

class Ethereum_data(Dados):

    def __init__(self, n, time, model):

        self.model = model
        self.time = time
        try:
            if model:
                self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=ETH&tsym=BRL&allData=true&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")
            else:
                self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histo{self.time}?fsym=ETH&tsym=BRL&limit={n}&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")

            if self.requisicao.status_code == 200:
                self.dados = self.requisicao.json()
                self.corrige_os_dados_externos()
            else:
                if self.time == "day":    
                    if model:
                        relative_path = "modelDataSets\ethereum.csv"
                    else:
                        relative_path = "DataSets\ethereum_data.csv"
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    csv_path = os.path.join(script_dir, relative_path)
                    if os.path.exists(csv_path):
                        self.df = pd.read_csv(csv_path)
                        self.corrige_os_dados_internos()
                elif self.time == "hour" and self.model == False:
                    relative_path = "DataSets_hour\ethereum_hour.csv"
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    csv_path = os.path.join(script_dir, relative_path)
                    if os.path.exists(csv_path):
                        self.df = pd.read_csv(csv_path)
                        self.corrige_os_dados_internos()

        except req.exceptions.RequestException:
            if self.time == "day":    
                if model == False:
                    relative_path = "DataSets/ethereum_data.csv"
                elif model:
                    relative_path = "modelDataSets/ethereum.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df = pd.read_csv(csv_path)
                    self.corrige_os_dados_internos()
            elif self.time == "hour" and self.model == False:
                relative_path = "DataSets_hour\ethereum_hour.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df = pd.read_csv(csv_path)
                    self.corrige_os_dados_internos()

    def corrige_os_dados_externos(self):
        """
        Corrige os dados externos do Ethereum.

        Esta função é responsável por corrigir os dados externos obtidos da API, formatando-os em um DataFrame do Pandas.
        """
        self.df = pd.DataFrame([self.dados["Data"]["Data"][n]["time"] for n in range(len(self.dados["Data"]["Data"]))], columns=["time"])
        self.df["Open"] = [self.dados["Data"]["Data"][n]["open"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["High"] = [self.dados["Data"]["Data"][n]["high"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Low"] = [self.dados["Data"]["Data"][n]["low"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Price"] = [self.dados["Data"]["Data"][n]["close"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Volume"] = [self.dados["Data"]["Data"][n]["volumeto"] for n in range(len(self.dados["Data"]["Data"]))]  
        if self.time == "day":
            self.df.time = self.df.time.astype(int)
            self.df["Data"] = pd.to_datetime(self.df.time)
            for n in range(len(self.df)):
                self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"]).date()

            self.df = self.df.drop(columns=["time"])
            self.df.set_index('Data', inplace=True)
            self.df = self.df.iloc[::-1]
            self.df = self.df.asfreq("D")
            if self.model == False:
                relative_path = "DataSets/ethereum_data.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df.to_csv(csv_path)
            elif self.model:
                relative_path = "modelDataSets/ethereum.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df.to_csv(csv_path)            
        elif self.time == "hour" and self.model == False:
            self.df.time = self.df.time.astype(int)
            self.df["Data"] = pd.to_datetime(self.df.time)
            for n in range(len(self.df)):
                self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"])

            self.df = self.df.drop(columns=["time"])
            self.df.set_index('Data', inplace=True)
            relative_path = "DataSets_hour\ethereum_hour.csv"
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, relative_path)
            if os.path.exists(csv_path):
                    self.df.to_csv(csv_path)

    def corrige_os_dados_internos(self):
        """
        Corrige os dados internos do Ethereum.

        Esta função é responsável por corrigir os dados internos do Ethereum, se necessário.
        """
        if self.time == "day":
            self.df.Data = pd.to_datetime(self.df.Data)
            self.df.set_index("Data", inplace= True)
            self.df = self.df.asfreq("D")
        else:
            self.df.Data = pd.to_datetime(self.df.Data)
            self.df.set_index("Data", inplace= True)         

class Solana_data(Dados):
    
    def __init__(self, n, time, model):

        self.model = model
        self.time = time
        try:
            if model:
                self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=SOL&tsym=BRL&allData=true&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")
            else:
                self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histo{self.time}?fsym=SOL&tsym=BRL&limit={n}&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")

            if self.requisicao.status_code == 200:
                self.dados = self.requisicao.json()
                self.corrige_os_dados_externos()
            else:
                if self.time == "day":        
                    if model:
                        relative_path = "modelDataSets\ethereum.csv"
                    else:
                        relative_path = "DataSets\ethereum_data.csv"
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    csv_path = os.path.join(script_dir, relative_path)
                    if os.path.exists(csv_path):
                        self.df = pd.read_csv(csv_path)
                        self.corrige_os_dados_internos()

                elif self.time == "hour" and self.model == False:
                    relative_path = "DataSets_hour\solana_hour.csv"
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    csv_path = os.path.join(script_dir, relative_path)
                    if os.path.exists(csv_path):
                        self.df = pd.read_csv(csv_path)
                        self.corrige_os_dados_internos()

        except req.exceptions.RequestException:
            if self.time == "day":
                if self.model == False:
                    relative_path = "DataSets\solana_data.csv"
                elif self.model:
                    relative_path = "modelDataSets/solana.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df = pd.read_csv(csv_path)
                    self.corrige_os_dados_internos()
            elif self.time == "hour" and self.model == False:
                relative_path = "DataSets_hour\solana_hour.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df = pd.read_csv(csv_path)
                    self.corrige_os_dados_internos()

    def corrige_os_dados_externos(self):

        self.df = pd.DataFrame([self.dados["Data"]["Data"][n]["time"] for n in range(len(self.dados["Data"]["Data"]))], columns=["time"])
        self.df["Open"] = [self.dados["Data"]["Data"][n]["open"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["High"] = [self.dados["Data"]["Data"][n]["high"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Low"] = [self.dados["Data"]["Data"][n]["low"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Price"] = [self.dados["Data"]["Data"][n]["close"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Volume"] = [self.dados["Data"]["Data"][n]["volumeto"] for n in range(len(self.dados["Data"]["Data"]))]  
        self.df.time = self.df.time.astype(int)
        self.df["Data"] = pd.to_datetime(self.df.time)
        print(self.df)

        if self.time == "day":
            for n in range(len(self.df)):
                self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"]).date()
            self.df = self.df.drop(columns=["time"])
            self.df.set_index('Data', inplace=True)
            self.df = self.df.iloc[::-1]
            self.df = self.df.asfreq("D")
            if self.model == False:
                relative_path = "DataSets/solana_data.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df.to_csv(csv_path)
            elif self.model:
                relative_path = "modelDataSets/solana.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df.to_csv(csv_path)

        else:
            for n in range(len(self.df)):
                self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"])

            self.df = self.df.drop(columns=["time"])
            self.df.set_index('Data', inplace=True)

            relative_path = "DataSets_hour\solana_hour.csv"
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, relative_path)
            if os.path.exists(csv_path):
                self.df.to_csv(csv_path)        

    def corrige_os_dados_internos(self):
        if self.time == "day":    
            self.df.Data = pd.to_datetime(self.df.Data)
            self.df.set_index("Data", inplace= True)
            self.df = self.df.asfreq("D")
        else:
            self.df.Data = pd.to_datetime(self.df.Data)
            self.df.set_index("Data", inplace= True)

class Dolar_data(Dados):

    def __init__(self, n, atual):
        if atual == False:    
            try:
                self.requisicao = req.get(f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{n}")
                if self.requisicao.status_code == 200:
                    self.df = pd.DataFrame(self.requisicao.json())
                    self.corrige_os_dados_externos()
                    self.registra_os_dados("DataSets\dolar_data.csv")
                else:
                    self.get_dados_internos("DataSets\dolar_data.csv")
            except req.exceptions.RequestException:
                    self.get_dados_internos("DataSets\dolar_data.csv")
        else:
            self.get_cotacao_atual()
        

    def corrige_os_dados_externos(self):
        self.df = self.df.dropna(axis=1)
        self.df.timestamp = self.df.timestamp.astype(int)
        self.df["Data"] = self.df.timestamp
        for n in range(len(self.df)):
            self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "timestamp"]).date()

        self.df.set_index("Data", inplace=True)
        self.df["Compra"] = self.df.bid
        self.df["Venda"] = self.df.ask
        self.df["High"] = self.df.high
        self.df["Low"] = self.df.low
        self.df = self.df.drop(columns=["varBid", "pctChange", "timestamp", "bid", "ask", "high", "low"])
        self.df.High = self.df.High.astype(float)
        self.df.Low = self.df.Low.astype(float)
        self.df.Venda = self.df.Venda.astype(float)
        self.df.Compra = self.df.Compra.astype(float)

    def corrige_os_dados_internos(self):

        self.df.Data = pd.to_datetime(self.df.Data)
        self.df.set_index("Data", inplace= True)
        self.df = self.df.iloc[::-1]

    def registra_os_dados(self, locaDataSet):
        relative_path = locaDataSet
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, relative_path)
        if os.path.exists(csv_path):
            self.df.to_csv(csv_path)

    def get_dados_internos(self, localDaset):
            relative_path = localDaset
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, relative_path)
            if os.path.exists(csv_path):
                self.df = pd.read_csv(csv_path)
                self.corrige_os_dados_internos()
    
    def get_cotacao_atual(self):
            
            self.requisicao = req.get(f"https://economia.awesomeapi.com.br/json/last/USD-BRL")
            if self.requisicao.status_code == 200:
                self.dados =self.requisicao.json()
                self.df = pd.DataFrame([self.dados["USDBRL"]])
                print(self.df)
                self.corrige_os_dados_externos()
            else:
                self.df = f"Erro: {self.requisicao.status_code}"
            
class Criptomoedas_data(Dados):

    def __init__(self, n, moeda, time, atual):
        self.time = time
        self.atual = atual
        if atual == False:
            self.req = req.get(f"https://min-api.cryptocompare.com/data/v2/histo{time}?fsym={moeda}&tsym=BRL&limit={n}&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")
            try:
                if self.req.status_code == 200:
                    self.dados = self.req.json()
                    if self.dados["Response"] == "Success":
                        self.corrige_os_dados_externos()
                    else:
                        self.df = self.dados["Message"]
                else:
                    self.df = f"Erro: {self.req.status_code}"
            except req.exceptions.RequestException:
                    self.df = "Sem internet"
        else:
            self.req = req.get(f"https://min-api.cryptocompare.com/data/v2/histominute?fsym={moeda}&tsym=BRL&limit=1&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")
            try:
                if self.req.status_code == 200:
                    self.dados = self.req.json()
                    if self.dados["Response"] == "Success":
                        self.corrige_os_dados_externos()
                    else:
                        self.df = self.dados["Message"]
                else:
                    self.df = f"Erro: {self.req.status_code}"
            except req.exceptions.RequestException:
                    self.df = "Sem internet"           

    def corrige_os_dados_externos(self):
        self.df = pd.DataFrame([self.dados["Data"]["Data"][n]["time"] for n in range(len(self.dados["Data"]["Data"]))], columns=["time"])
        self.df["Open"] = [self.dados["Data"]["Data"][n]["open"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["High"] = [self.dados["Data"]["Data"][n]["high"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Low"] = [self.dados["Data"]["Data"][n]["low"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Price"] = [self.dados["Data"]["Data"][n]["close"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Volume"] = [self.dados["Data"]["Data"][n]["volumeto"] for n in range(len(self.dados["Data"]["Data"]))]       
        self.df.time = self.df.time.astype(int)
        self.df["Data"] = pd.to_datetime(self.df.time)
        if self.time == "day" and self.atual == False:
            for n in range(len(self.df)):
                    self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"]).date()
            self.df = self.df.drop(columns=["time"])
            self.df.set_index('Data', inplace=True)
            self.df = self.df.iloc[::-1]
        elif self.time == "hour" and self.atual == False:
            for n in range(len(self.df)):
                    self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"])
            self.df = self.df.drop(columns=["time"])
            self.df.set_index('Data', inplace=True)
            self.df = self.df.iloc[::-1]
        elif self.atual:
            for n in range(len(self.df)):
                    self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"]).time()
            self.df = self.df.drop(columns=["time"])
            self.df.set_index('Data', inplace=True)
            self.df = self.df.iloc[::-1]

    def corrige_os_dados_internos(self):
        pass