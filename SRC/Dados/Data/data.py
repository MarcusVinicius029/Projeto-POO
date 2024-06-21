import pandas as pd
from datetime import datetime
import abc
import matplotlib.pyplot as plt
import requests as req
import os


class Dados(abc.ABC):
    """
    Classe abstrata para manipulação de dados.

    Define métodos abstratos que devem ser implementados por subclasses concretas para correção,
    salvamento e obtenção de dados externos e internos.

    Attributes:
        Não possui atributos definidos na classe base.
    """

    def __inti__(self):
        """
        Construtor da classe Dados.

        Este construtor está vazio, pois não é necessário inicializar atributos específicos na classe base.
        """
        pass

    @abc.abstractmethod
    def corrige_os_dados_externos(self):
        """
        Método abstrato para correção dos dados externos.

        Cada implementação concreta deve definir como corrigir os dados obtidos externamente.
        """
        pass

    @abc.abstractmethod
    def corrige_os_dados_internos(self):
        """
        Método abstrato para correção dos dados internos.

        Cada implementação concreta deve definir como corrigir os dados carregados de um arquivo interno.
        """
        pass

    @abc.abstractmethod
    def salva_os_dados_externos(self):
        """
        Método abstrato para salvar os dados corrigidos externos.

        Cada implementação concreta deve definir como salvar os dados corrigidos externos em um arquivo.
        """
        pass

    @abc.abstractmethod
    def get_dados_internos(self):
        """
        Método abstrato para obter os dados internos.

        Cada implementação concreta deve definir como carregar os dados de um arquivo interno.
        """
        pass

    @abc.abstractmethod
    def corrige_os_dados_internos(self):
        """
        Método abstrato para correção dos dados internos.

        Cada implementação concreta deve definir como corrigir os dados carregados de um arquivo interno.
        """
        pass

class Criptomoedas_data(Dados):
    """
    Classe para obtenção, correção e salvamento de dados de criptomoedas.

    Esta classe herda da classe Dados.

    Args:
        n (int): Número de (minutos, horas ou dias) anteriores ao período atual.
        criptomoeda (str): Nome da criptomoeda (por exemplo, "BTC", "ETH", "SOL"), as criptomedas devem ser passadas pela sua sigla.
        time (str): Unidade de tempo dos dados ("day", "hour" ou "minute").

    Attributes:
        time (str): Unidade de tempo dos dados.
        criptomoeda (str): Nome da criptomoeda.
        n (int): Número de registros a serem obtidos.
        requisicao (requests.Response): Resposta da requisição HTTP.
        dados (dict): Dados obtidos da API.
        df (pandas.DataFrame): DataFrame para armazenamento e manipulação dos dados.
    """

    def __init__(self, n: int, criptomoeda: str, time: str):
        """
        Inicializa a classe Criptomoedas_data.

        Faz uma requisição à API para obter os dados da criptomoeda especificada.
        Se a requisição for bem-sucedida, corrige os dados, salva-os externamente se for o caso,
        ou recupera dados internos se houver falha na conexão.
        Lança exceções se houver problemas na conexão ou se os dados estiverem incorretos.

        Args:
            n (int): Número de registros a serem obtidos.
            criptomoeda (str): Nome da criptomoeda (por exemplo, "BTC", "ETH", "SOL").
            time (str): Unidade de tempo dos dados ("day", "hour" ou "minute").

        Raises:
            ValueError: Se houver problemas na conexão ou se os dados estiverem incorretos.
        """
        self.time = time
        self.criptomoeda = criptomoeda
        self.n = n
        try:
            self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histo{self.time}?fsym={self.criptomoeda}&tsym=BRL&limit={self.n}&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")
            if self.requisicao.status_code == 200:
                self.dados = self.requisicao.json()
                if self.dados["Response"] == "Success":
                    self.corrige_os_dados_externos()
                    if self.criptomoeda == "BTC" and self.time == "day" and self.n >= 10:
                        self.salva_os_dados_externos("DataSets/bitcoin_data.csv")
                    elif self.criptomoeda == "ETH" and self.time == "day" and self.n >= 10:
                        self.salva_os_dados_externos("DataSets/ethereum_data.csv")
                    elif self.criptomoeda == "SOL" and self.time == "day" and self.n >= 10:
                        self.salva_os_dados_externos("DataSets/solana_data.csv")
                else:
                    raise ValueError("Dados incorretos!")
            else:
                raise ValueError("Problemas na conexão!")
        except req.exceptions.RequestException:
            if self.time == "day":
                if self.criptomoeda == "BTC":
                    self.get_dados_internos("DataSets/bitcoin_data.csv")
                elif self.criptomoeda == "ETH":
                    self.get_dados_internos("DataSets/ethereum_data.csv")
                elif self.criptomoeda == "SOL":
                    self.get_dados_internos("DataSets/solana_data.csv")
                else:
                    raise ValueError("Problemas na conexão!")
            else: 
                raise ValueError("Problemas na conexão!")
    
    def corrige_os_dados_externos(self):
        """
        Corrige os dados externos obtidos da API.

        Converte os dados em um DataFrame Pandas, ajusta os tipos de dados e define a coluna 'Data' como índice.
        """
        self.df = pd.DataFrame([self.dados["Data"]["Data"][n]["time"] for n in range(len(self.dados["Data"]["Data"]))], columns=["time"])
        self.df["Open"] = [self.dados["Data"]["Data"][n]["open"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["High"] = [self.dados["Data"]["Data"][n]["high"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Low"] = [self.dados["Data"]["Data"][n]["low"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Price"] = [self.dados["Data"]["Data"][n]["close"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Volume"] = [self.dados["Data"]["Data"][n]["volumeto"] for n in range(len(self.dados["Data"]["Data"]))]       
        self.df.time = self.df.time.astype(int)

        if self.time == "day":
            for i in range(len(self.df)):
                    self.df.loc[i, "Data"] = datetime.fromtimestamp(self.df.loc[i, "time"]).date()
            self.df.Data = pd.to_datetime(self.df.Data)
        elif self.time == "hour":
            for i in range(len(self.df)):
                    self.df.loc[i, "Data"] = datetime.fromtimestamp(self.df.loc[i, "time"]).time()
        elif self.time == "minute":
            for i in range(len(self.df)):
                self.df.loc[i, "Data"] = datetime.fromtimestamp(self.df.loc[i, "time"]).time()
        
        if self.n == 1:
            last_index = self.df.index[-1]
            self.df = pd.DataFrame(self.df.loc[last_index]).T
        self.df.set_index('Data', inplace=True)
        self.df = self.df.drop(columns=["time"])

    def salva_os_dados_externos(self, caminho: str):
        """
        Salva os dados corrigidos externos em um arquivo CSV.

        Args:
            caminho (str): Caminho relativo do arquivo CSV onde os dados serão salvos.

        Raises:
            ValueError: Se o caminho passado estiver incorreto.
        """
        relative_path = caminho
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, relative_path)
        if os.path.exists(csv_path):
            self.df.to_csv(csv_path)
        else:
            raise ValueError("O caminho passado está errado!")

    def get_dados_internos(self, caminho: str):
        """
        Obtém dados internos de um arquivo CSV.

        Args:
            caminho (str): Caminho relativo do arquivo CSV de onde os dados serão obtidos.

        Raises:
            ValueError: Se o arquivo especificado não for encontrado.
        """
        relative_path = caminho
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, relative_path)
        if os.path.exists(csv_path):
            self.df = pd.read_csv(csv_path, delimiter=",")
            self.corrige_os_dados_internos()
        else:
            raise ValueError("Arquivo não encontrado!")

    def corrige_os_dados_internos(self):
        """
        Corrige os dados internos obtidos de um arquivo CSV.

        Converte a coluna 'Data' para o tipo datetime e define-a como índice do DataFrame.
        """
        self.df.Data = pd.to_datetime(self.df.Data)
        self.df.set_index("Data", inplace=True)

class Previsao_data(Dados):
    """
    Classe para obtenção, correção e salvamento de dados históricos para previsão de criptomoedas.

    Esta classe herda da classe Dados.

    Args:
        criptomoeda (str): Nome da criptomoeda ("BTC", "ETH" ou "SOL").

    Attributes:
        criptomoeda (str): Nome da criptomoeda.
        requisicao (requests.Response): Resposta da requisição HTTP.
        dados (dict): Dados obtidos da API ou internamente.
        df (pandas.DataFrame): DataFrame para armazenamento e manipulação dos dados.
    """

    def __init__(self, criptomoeda: str):
        """
        Inicializa a classe Previsao_data.

        Faz uma requisição à API para obter os dados históricos da criptomoeda especificada.
        Se a requisição for bem-sucedida, corrige os dados, salva-os externamente se for o caso,
        ou recupera dados internos se houver falha na conexão.
        Lança exceções se houver problemas na conexão, se a criptomoeda não for suportada
        ou se os dados estiverem incorretos.

        Args:
            criptomoeda (str): Nome da criptomoeda ("BTC", "ETH" ou "SOL").

        Raises:
            ValueError: Se houver problemas na conexão, se a criptomoeda não for suportada
                        ou se os dados estiverem incorretos.
        """
        self.criptomoeda = criptomoeda
        if self.criptomoeda in ["BTC", "ETH", "SOL"]:
            try:
                self.requisicao = req.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={self.criptomoeda}&tsym=BRL&allData=true&api_key=53d41b3b5d49f3b5dba9daa9cb4f60848f537f53de8284c2e169324dca23bc9c")
                if self.requisicao.status_code == 200:
                    self.dados = self.requisicao.json()
                    if self.dados["Response"] == "Success":
                        self.corrige_os_dados_externos()
                        if self.criptomoeda == "BTC":
                            self.salva_os_dados_externos("modelDataSets/bitcoin.csv")
                        elif self.criptomoeda == "ETH":
                            self.salva_os_dados_externos("modelDataSets/ethereum.csv")
                        elif self.criptomoeda == "SOL":
                            self.salva_os_dados_externos("modelDataSets/solana.csv")
                    else:
                        raise ValueError("Dados incorretos!")
                else:
                    raise ValueError("Problema na conexão!")
            except req.exceptions.RequestException:
                if self.criptomoeda == "BTC":
                    self.get_dados_internos("DataSets/bitcoin_data.csv")
                elif self.criptomoeda == "ETH":
                    self.get_dados_internos("DataSets/ethereum_data.csv")
                elif self.criptomoeda == "SOL":
                    self.get_dados_internos("modelDataSets/solana.csv")
        else:
            raise ValueError("Essa função não está disponível para essa criptomoeda!")
            
    def corrige_os_dados_externos(self):
        """
        Corrige os dados externos obtidos da API.

        Converte os dados em um DataFrame Pandas, ajusta os tipos de dados,
        define a coluna 'Data' como índice e filtra os dados após a linha 2482.
        """
        self.df = pd.DataFrame([self.dados["Data"]["Data"][n]["time"] for n in range(len(self.dados["Data"]["Data"]))], columns=["time"])
        self.df["Open"] = [self.dados["Data"]["Data"][n]["open"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["High"] = [self.dados["Data"]["Data"][n]["high"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Low"] = [self.dados["Data"]["Data"][n]["low"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Price"] = [self.dados["Data"]["Data"][n]["close"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Volume"] = [self.dados["Data"]["Data"][n]["volumeto"] for n in range(len(self.dados["Data"]["Data"]))]       
        self.df.time = self.df.time.astype(int)
        for i in range(len(self.df)):
            self.df.loc[i, "Data"] = datetime.fromtimestamp(self.df.loc[i, "time"]).date()
        self.df = self.df.loc[2482:, :]
        self.df.Data = pd.to_datetime(self.df.Data)      
        self.df.set_index('Data', inplace=True)
        self.df = self.df.drop(columns=["time"])
                
    def salva_os_dados_externos(self, caminho: str):
        """
        Salva os dados corrigidos externos em um arquivo CSV.

        Args:
            caminho (str): Caminho relativo do arquivo CSV onde os dados serão salvos.

        Raises:
            ValueError: Se o caminho passado não existir.
        """
        relative_path = caminho
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, relative_path)
        if os.path.exists(csv_path):
            self.df.to_csv(csv_path)
        else:
            raise ValueError("O caminho passado não existe!")

    def get_dados_internos(self, caminho: str):
        """
        Obtém dados internos de um arquivo CSV.

        Args:
            caminho (str): Caminho relativo do arquivo CSV de onde os dados serão obtidos.

        Raises:
            ValueError: Se o arquivo especificado não for encontrado.
        """
        relative_path = caminho
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, relative_path)
        if os.path.exists(csv_path):
            self.df = pd.read_csv(csv_path, delimiter=",")
            self.corrige_os_dados_internos()
        else:
            raise ValueError("Arquivo não encontrado!")

    def corrige_os_dados_internos(self):
        """
        Corrige os dados internos obtidos de um arquivo CSV.

        Converte a coluna 'Data' para o tipo datetime e define-a como índice do DataFrame.
        """
        self.df.Data = pd.to_datetime(self.df.Data)
        self.df.set_index("Data", inplace=True)

class Dolar_data(Dados):
    """
    Classe para obtenção, correção e salvamento de dados históricos ou atuais da cotação do dólar.

    Esta classe herda da classe Dados.

    Args:
        n (int): Número de dias de histórico a serem obtidos.
        atual (str): Se 'atual' for True, busca a cotação atual do dólar; caso contrário,
                     busca o histórico de n dias.

    Attributes:
        requisicao (requests.Response): Resposta da requisição HTTP.
        df (pandas.DataFrame): DataFrame para armazenamento e manipulação dos dados.
    """

    def __init__(self, n: int, atual: str):
        """
        Inicializa a classe Dolar_data.

        Realiza uma requisição à API para obter os dados de histórico ou cotação atual do dólar.
        Se a requisição for bem-sucedida, corrige os dados, salva-os externamente se for o caso,
        ou recupera dados internos se houver falha na conexão.
        Lança exceções se houver problemas na conexão ou se o arquivo especificado não for encontrado.

        Args:
            n (int): Número de dias de histórico a serem obtidos.
            atual (str): Se 'atual' for True, busca a cotação atual do dólar; caso contrário,
                         busca o histórico de n dias.

        Raises:
            ValueError: Se o caminho passado não existir.
        """
        if atual:    
            try:
                self.requisicao = req.get(f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{n}")
                if self.requisicao.status_code == 200:
                    self.df = pd.DataFrame(self.requisicao.json())
                    self.corrige_os_dados_externos()
                    self.salva_os_dados_externos("DataSets/dolar_data.csv")
                else:
                    self.get_dados_internos("DataSets/dolar_data.csv")
            except req.exceptions.RequestException:
                self.get_dados_internos("DataSets/dolar_data.csv")
        else:
            self.get_cotacao_atual()
        
    def corrige_os_dados_externos(self):
        """
        Corrige os dados externos obtidos da API.

        Realiza ajustes nos tipos de dados, renomeia colunas e define a coluna 'Data' como índice.
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

    def corrige_os_dados_internos(self):
        """
        Corrige os dados internos obtidos de um arquivo CSV.

        Converte a coluna 'Data' para o tipo datetime e reordena o DataFrame em ordem crescente de datas.
        """
        self.df.Data = pd.to_datetime(self.df.Data)
        self.df.set_index("Data", inplace=True)
        self.df = self.df.iloc[::-1]

    def salva_os_dados_externos(self, locaDataSet: str):
        """
        Salva os dados corrigidos externos em um arquivo CSV.

        Args:
            locaDataSet (str): Caminho relativo do arquivo CSV onde os dados serão salvos.

        Raises:
            ValueError: Se o caminho passado não existir.
        """
        relative_path = locaDataSet
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, relative_path)
        if os.path.exists(csv_path):
            self.df.to_csv(csv_path)
        else:
            raise ValueError("O caminho passado não está correto!")

    def get_dados_internos(self, localDaset: str):
        """
        Obtém dados internos de um arquivo CSV.

        Args:
            localDaset (str): Caminho relativo do arquivo CSV de onde os dados serão obtidos.

        Raises:
            ValueError: Se o arquivo especificado não for encontrado.
        """
        relative_path = localDaset
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, relative_path)
        if os.path.exists(csv_path):
            self.df = pd.read_csv(csv_path)
            self.corrige_os_dados_internos()
        else:
            raise ValueError("Arquivo não encontrado!")
    
    def get_cotacao_atual(self):
        """
        Obtém a cotação atual do dólar.

        Realiza uma requisição à API para obter a cotação atual do dólar em tempo real.
        Se a requisição for bem-sucedida, corrige os dados e os armazena no DataFrame.
        Lança uma exceção se houver problemas na conexão.
        """
        try:
            self.requisicao = req.get(f"https://economia.awesomeapi.com.br/json/last/USD-BRL")
            if self.requisicao.status_code == 200:
                self.dados = self.requisicao.json()
                self.df = pd.DataFrame([self.dados["USDBRL"]])
                self.corrige_os_dados_externos()
            else:
                raise ValueError("Problemas na conexão!")
        except req.exceptions.RequestException:
            raise ValueError("Problemas na conexão!")
