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
    """
    Classe para manipulação de dados do Bitcoin.
    Esta classe herda da classe Dados e é responsável por obter e corrigir os dados do Bitcoin.
    """

    def __init__(self, n, model = False):
        """
        Inicializa a classe Bitcoin_data.

        Parameters:
        - n (int): O número de dias de dados do Bitcoin a serem obtidos.
        - model(bool): Define se o DataFrame deve ser formatado para previsão(True) ou exibição(False)
        """
        self.model = model

        try:
            # Faz uma requisição para obter os dados do Bitcoin
            if model:
                self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=BRL&allData=true&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")
            else:
                self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=BRL&limit={n}&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")

            # Verifica se a requisição foi bem-sucedida
            if self.requisicao.status_code == 200:
                self.dados = self.requisicao.json()
                self.corrige_os_dados_externos()
            else:
                # Se a requisição falhar, tenta carregar os dados internos
                if model:
                    relative_path = "modelDataSets/bitcoin.csv"
                else:
                    relative_path = "DataSets/bitcoin.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df = pd.read_csv(csv_path)
                    self.corrige_os_dados_internos()
        except req.exceptions.RequestException:
            # Em caso de erro na requisição, tenta carregar os dados internos
            if model:
                relative_path = "modelDataSets/bitcoin.csv"
            else:
                relative_path = "DataSets/bitcoin_data.csv"
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, relative_path)
            print(csv_path)
            if os.path.exists(csv_path):
                self.df = pd.read_csv(csv_path)
                self.corrige_os_dados_internos()

    def corrige_os_dados_externos(self):
        """
        Corrige os dados externos do Bitcoin.

        Esta função é responsável por corrigir os dados externos obtidos da API, formatando-os em um DataFrame do Pandas.
        """
        # Cria um DataFrame com os dados externos do Bitcoin
        self.df = pd.DataFrame([self.dados["Data"]["Data"][n]["time"] for n in range(len(self.dados["Data"]["Data"]))], columns=["time"])
        self.df["Open"] = [self.dados["Data"]["Data"][n]["open"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["High"] = [self.dados["Data"]["Data"][n]["high"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Low"] = [self.dados["Data"]["Data"][n]["low"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Price"] = [self.dados["Data"]["Data"][n]["close"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Volume"] = [self.dados["Data"]["Data"][n]["volumeto"] for n in range(len(self.dados["Data"]["Data"]))]       

        # Formata as colunas de data e hora
        self.df.time = self.df.time.astype(int)
        self.df["Data"] = pd.to_datetime(self.df.time)
        for n in range(len(self.df)):
            self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"]).date()

        # Limpa e formata o DataFrame
        self.df = self.df.drop(columns=["time"])
        self.df.set_index('Data', inplace=True)
        self.df = self.df.iloc[::-1]
        self.df = self.df.asfreq("D")


        # Salva os dados corrigidos em um arquivo CSV
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

    def corrige_os_dados_internos(self):
        """
        Corrige os dados internos do Bitcoin.

        Esta função é responsável por corrigir os dados internos do Bitcoin, se necessário.
        """
        self.df.Data = pd.to_datetime(self.df.Data)
        self.df.set_index("Data", inplace= True)
        self.df = self.df.loc[::-1]
        self.df = self.df.asfreq("D")
       
class Ethereum_data(Dados):
    """
    Classe para manipulação de dados do Ethereum.
    Esta classe herda da classe Dados e é responsável por obter e corrigir os dados do Ethereum.
    """

    def __init__(self, n, model):
        """
        Inicializa a classe Ethereum_data.

        Parameters:
        - n (int): O número de dias de dados do Ethereum a serem obtidos.
        - model(bool): Define se o DataFrame deve ser formatado para previsão(True) ou exibição(False)
        """
        self.model = model
        try:
            # Faz uma requisição para obter os dados do Ethereum
            if model:
                self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=ETH&tsym=BRL&allData=true&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")
            else:
                self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=ETH&tsym=BRL&limit={n}&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")

            # Verifica se a requisição foi bem-sucedida
            if self.requisicao.status_code == 200:
                self.dados = self.requisicao.json()
                self.corrige_os_dados_externos()
            else:
                # Se a requisição falhar, tenta carregar os dados internos
                relative_path = "DataSets\ethereum_data.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df = pd.read_csv(csv_path)
                    self.corrige_os_dados_internos()
        except req.exceptions.RequestException:
            # Em caso de erro na requisição, tenta carregar os dados internos
            if model == False:
                relative_path = "DataSets/ethereum_data.csv"
            elif model:
                relative_path = "modelDataSets/ethereum.csv"
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
        # Cria um DataFrame com os dados externos do Ethereum
        self.df = pd.DataFrame([self.dados["Data"]["Data"][n]["time"] for n in range(len(self.dados["Data"]["Data"]))], columns=["time"])
        self.df["Open"] = [self.dados["Data"]["Data"][n]["open"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["High"] = [self.dados["Data"]["Data"][n]["high"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Low"] = [self.dados["Data"]["Data"][n]["low"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Price"] = [self.dados["Data"]["Data"][n]["close"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Volume"] = [self.dados["Data"]["Data"][n]["volumeto"] for n in range(len(self.dados["Data"]["Data"]))]  

        # Formata as colunas de data e hora
        self.df.time = self.df.time.astype(int)
        self.df["Data"] = pd.to_datetime(self.df.time)
        for n in range(len(self.df)):
            self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"]).date()

        # Limpa e formata o DataFrame
        self.df = self.df.drop(columns=["time"])
        self.df.set_index('Data', inplace=True)
        self.df = self.df.iloc[::-1]
        self.df = self.df.asfreq("D")

        # Salva os dados corrigidos em um arquivo CSV
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

    def corrige_os_dados_internos(self):
        """
        Corrige os dados internos do Ethereum.

        Esta função é responsável por corrigir os dados internos do Ethereum, se necessário.
        """
        self.df.Data = pd.to_datetime(self.df.Data)
        self.df.set_index("Data", inplace= True)
        self.df = self.df.asfreq("D")

class Solana_data(Dados):
    """
    Classe para manipulação de dados do Solana.
    Esta classe herda da classe Dados e é responsável por obter e corrigir os dados do Solana.
    """

    def __init__(self, n, model):
        """
        Inicializa a classe Solana_data.

        Parameters:
        - n (int): O número de dias de dados do Solana a serem obtidos.
        - model(bool): Define se o DataFrame deve ser formatado para previsão(True) ou exibição(False)
        """
        self.model = model
        try:
            # Faz uma requisição para obter os dados do Solana
            if model:
                self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=SOL&tsym=BRL&allData=true&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")
            else:
                self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=SOL&tsym=BRL&limit={n}&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")

            # Verifica se a requisição foi bem-sucedida
            if self.requisicao.status_code == 200:
                self.dados = self.requisicao.json()
                self.corrige_os_dados_externos()
            else:
                # Se a requisição falhar, tenta carregar os dados internos
                relative_path = "DataSets\solana_data.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df = pd.read_csv(csv_path)
                    self.corrige_os_dados_internos()
        except req.exceptions.RequestException:
            # Em caso de erro na requisição, tenta carregar os dados internos
            if self.model == False:
                relative_path = "DataSets/solana_data.csv"
            elif self.model:
                relative_path = "modelDataSets/solana.csv"
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, relative_path)
            if os.path.exists(csv_path):
                self.df = pd.read_csv(csv_path)
                self.corrige_os_dados_internos()

    def corrige_os_dados_externos(self):
        """
        Corrige os dados externos do Solana.

        Esta função é responsável por corrigir os dados externos obtidos da API, formatando-os em um DataFrame do Pandas.
        """
        # Cria um DataFrame com os dados externos do Solana
        self.df = pd.DataFrame([self.dados["Data"]["Data"][n]["time"] for n in range(len(self.dados["Data"]["Data"]))], columns=["time"])
        self.df["Open"] = [self.dados["Data"]["Data"][n]["open"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["High"] = [self.dados["Data"]["Data"][n]["high"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Low"] = [self.dados["Data"]["Data"][n]["low"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Price"] = [self.dados["Data"]["Data"][n]["close"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Volume"] = [self.dados["Data"]["Data"][n]["volumeto"] for n in range(len(self.dados["Data"]["Data"]))]  
        # Formata as colunas de data e hora
        self.df.time = self.df.time.astype(int)
        self.df["Data"] = pd.to_datetime(self.df.time)
        for n in range(len(self.df)):
            self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"]).date()

        # Limpa e formata o DataFrame
        self.df = self.df.drop(columns=["time"])
        self.df.set_index('Data', inplace=True)
        self.df = self.df.iloc[::-1]
        self.df = self.df.asfreq("D")

        # Salva os dados corrigidos em um arquivo CSV
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

    def corrige_os_dados_internos(self):
        """
        Corrige os dados internos do Solana.

        Esta função é responsável por corrigir os dados internos do Solana, se necessário.
        """
        self.df.Data = pd.to_datetime(self.df.Data)
        self.df.set_index("Data", inplace= True)
        self.df = self.df.asfreq("D")

class Dolar_data(Dados):
    """
    Classe para manipulação de dados do Dólar.
    Esta classe herda da classe Dados e é responsável por obter e corrigir os dados do Dólar.
    """

    def __init__(self, n):
        """
        Inicializa a classe Dolar_data.

        Parameters:
        - n (int): O número de dias de dados do Dólar a serem obtidos.
        """
        try:
            # Faz uma requisição para obter os dados do Dólar
            self.requisicao = req.get(f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{n}")

            # Verifica se a requisição foi bem-sucedida
            if self.requisicao.status_code == 200:
                self.df = pd.DataFrame(self.requisicao.json())
                self.corrige_os_dados_externos()
            else:
                # Se a requisição falhar, tenta carregar os dados internos
                relative_path = "DataSets/dolar_data.csv"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, relative_path)
                if os.path.exists(csv_path):
                    self.df = pd.read_csv(csv_path)
                    self.corrige_os_dados_internos()
        except req.exceptions.RequestException:
            # Em caso de erro na requisição, tenta carregar os dados internos
            relative_path = "DataSets/dolar_data.csv"
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, relative_path)
            if os.path.exists(csv_path):
                self.df = pd.read_csv(csv_path)
                self.corrige_os_dados_internos()

    def corrige_os_dados_externos(self):
        """
        Corrige os dados externos do Dólar.

        Esta função é responsável por corrigir os dados externos obtidos da API, formatando-os em um DataFrame do Pandas.
        """
        # Limpa o DataFrame e formata as colunas necessárias
        self.df = self.df.dropna(axis=1)
        self.df.timestamp = self.df.timestamp.astype(int)
        self.df["Data"] = self.df.timestamp
        for n in range(len(self.df)):
            self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "timestamp"]).date()

        # Define a coluna 'Data' como índice e renomeia as colunas
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

        # Salva os dados corrigidos em um arquivo CSV
        relative_path = "DataSets/dolar_data.csv"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, relative_path)
        if os.path.exists(csv_path):
            self.df.to_csv(csv_path)

    def corrige_os_dados_internos(self):
        """
        Corrige os dados internos do Dólar.

        Esta função é responsável por corrigir os dados internos do Dólar, se necessário.
        """
        self.df.Data = pd.to_datetime(self.df.Data)
        self.df.set_index("Data", inplace= True)
        self.df = self.df.iloc[::-1]