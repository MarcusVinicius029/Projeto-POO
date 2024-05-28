import pandas as pd
from datetime import datetime
import abc
import matplotlib.pyplot as plt
import requests as req


class Dados(abc.ABC):
    """
    Classe abstrata para a manipulação e preparação de dados.
    """
    
    @abc.abstractmethod
    def corrige_os_dados(self):
        """
        Corrige os dados carregados, ajustando valores e removendo dados desnecessários.
        """
        pass

class Bitcoin_data(Dados):
    """
    Classe para manipulação de dados da criptomoeda Bitcoin.

    Atributos:
    df (pd.DataFrame): DataFrame contendo os dados do Bitcoin.
    """

    def __init__(self, localDataset):
        """
        Inicializa a classe Bitcoin_data carregando um dataset local.

        Parâmetros:
        localDataset (str): Caminho para o arquivo CSV contendo os dados do Bitcoin.
        """
        self.df = pd.read_csv(localDataset, delimiter=";")
        self.corrige_os_dados()

    def corrige_os_dados(self):
        """
        Corrige e formata os dados do Bitcoin no DataFrame.

        Ações:
        - Converte a coluna 'timeOpen' para datetime.
        - Define 'timeOpen' como índice.
        - Converte o índice para apenas a data.
        - Remove colunas desnecessárias.
        - Converte e arredonda os valores das colunas 'open', 'high', 'low', 'close' e 'volume' para float.
        - Remove linhas com valores NaN.
        - Define a frequência do índice como diária.
        - Renomeia a coluna 'close' para 'Price'.
        """
        self.df["timeOpen"] = pd.to_datetime(self.df["timeOpen"])
        self.df.set_index("timeOpen", inplace=True)
        self.df.index = self.df.index.date
        self.df.drop(columns=["timeHigh", "timeClose", "timeLow", "name", "marketCap", "timestamp"], inplace=True, axis=1)
        self.df.open = self.df.open.astype(float).round(2)
        self.df.high = self.df.high.astype(float).round(2)
        self.df.low = self.df.low.astype(float).round(2)
        self.df.close = self.df.close.astype(float).round(2)
        self.df.volume = self.df.volume.astype(float).round(2)
        self.df.dropna(inplace=True, axis=0)
        self.df = self.df.asfreq("D")
        self.df["Price"] = self.df.close
        self.df = self.df.drop(columns="close")
        
class Ethereum_data(Dados):

    """
    Classe para manipulação de dados da criptomoeda Ethereum.

    Atributos:
    df (pd.DataFrame): DataFrame contendo os dados do Ethereum.
    """

    def __init__(self, localDataset):
        """
        Inicializa a classe Ethereum_data carregando um dataset local.

        Parâmetros:
        localDataset (str): Caminho para o arquivo CSV contendo os dados do Ethereum.
        """
        self.df = pd.read_csv(localDataset, delimiter=";")
        self.corrige_os_dados()

    def corrige_os_dados(self):
        """
        Corrige e formata os dados do Ethereum no DataFrame.

        Ações:
        - Converte a coluna 'timeOpen' para datetime.
        - Define 'timeOpen' como índice.
        - Converte o índice para apenas a data.
        - Remove colunas desnecessárias.
        - Converte e arredonda os valores das colunas 'open', 'high', 'low', 'close' e 'volume' para float.
        - Remove linhas com valores NaN.
        - Define a frequência do índice como diária.
        """
        self.df["timeOpen"] = pd.to_datetime(self.df["timeOpen"])
        self.df.set_index("timeOpen", inplace=True)
        self.df.index = self.df.index.date
        self.df.drop(columns=["timeHigh", "timeClose", "timeLow", "name", "marketCap", "timestamp"], inplace=True, axis=1)
        self.df.open = self.df.open.astype(float).round(2)
        self.df.high = self.df.high.astype(float).round(2)
        self.df.low = self.df.low.astype(float).round(2)
        self.df.close = self.df.close.astype(float).round(2)
        self.df.volume = self.df.volume.astype(float).round(2)
        self.df.dropna(inplace=True, axis=0)
        self.df = self.df.asfreq("D")

class Solana_data(Dados):
    """
    Classe para manipulação de dados da criptomoeda Solana.

    Atributos:
    df (pd.DataFrame): DataFrame contendo os dados da Solana.
    """

    def __init__(self, localDataset):
        """
        Inicializa a classe Solana_data carregando um dataset local.

        Parâmetros:
        localDataset (str): Caminho para o arquivo CSV contendo os dados da Solana.
        """
        self.df = pd.read_csv(localDataset, delimiter=";")
        self.corrige_os_dados()

    def corrige_os_dados(self):
        """
        Corrige e formata os dados da Solana no DataFrame.

        Ações:
        - Converte a coluna 'timeOpen' para datetime.
        - Define 'timeOpen' como índice.
        - Converte o índice para apenas a data.
        - Remove colunas desnecessárias.
        - Converte e arredonda os valores das colunas 'open', 'high', 'low', 'close' e 'volume' para float.
        - Remove linhas com valores NaN.
        - Define a frequência do índice como diária.
        """
        self.df["timeOpen"] = pd.to_datetime(self.df["timeOpen"])
        self.df.set_index("timeOpen", inplace=True)
        self.df.index = self.df.index.date
        self.df.drop(columns=["timeHigh", "timeClose", "timeLow", "name", "marketCap", "timestamp"], inplace=True, axis=1)
        self.df.open = self.df.open.astype(float).round(2)
        self.df.high = self.df.high.astype(float).round(2)
        self.df.low = self.df.low.astype(float).round(2)
        self.df.close = self.df.close.astype(float).round(2)
        self.df.volume = self.df.volume.astype(float).round(2)
        self.df.dropna(inplace=True, axis=0)
        self.df = self.df.asfreq("D")

class Dolar_data(Dados):
    """
    Classe para manipulação de dados do dólar.

    Atributos:
    df (pd.DataFrame): DataFrame contendo os dados do dólar.
    req (requests.models.Response): Objeto de resposta da requisição HTTP.
    """

    def get_cotacao(self, n):
        """
        Obtém a cotação do dólar dos últimos 'n' dias.

        Parâmetros:
        n (int): Número de dias para obter a cotação.

        Retorna:
        pd.DataFrame: DataFrame contendo as cotações do dólar se a requisição for bem-sucedida.
        str: Mensagem de erro se a requisição falhar.
        """
        self.req = req.get(f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{n}")
        if self.req.status_code == 200:
            self.df = pd.DataFrame(self.req.json())
            self.corrige_os_dados()
            return self.df
        else:
            return f"Foi obtido o seguinte erro durante a requisição: {self.req.status_code}"

    def corrige_os_dados(self):
        """
        Corrige e formata os dados da cotação do dólar no DataFrame.

        Ações:
        - Remove colunas com valores NaN.
        - Converte a coluna 'timestamp' para int.
        - Cria e formata a coluna 'Data' a partir do 'timestamp'.
        - Define 'Data' como índice.
        - Renomeia colunas para 'Compra', 'Venda', 'High' e 'Low'.
        - Remove colunas desnecessárias.
        - Converte colunas para float.
        """
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