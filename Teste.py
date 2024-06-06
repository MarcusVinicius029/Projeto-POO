"""
Arquivo para criar e testar pequenos códigos
Obs: Todo código de teste ou que não será incluido no projeto deve ser armazenado nesse arquivo!
"""
import requests as req
import pandas as pd
from datetime import datetime
import os

class Criptomoedas():

    def get_dados_atuais(self):
        
    def corrige_os_dados_externos(self):
        self.df = pd.DataFrame([self.dados["Data"]["Data"][n]["time"] for n in range(len(self.dados["Data"]["Data"]))], columns=["time"])
        self.df["Open"] = [self.dados["Data"]["Data"][n]["open"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["High"] = [self.dados["Data"]["Data"][n]["high"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Low"] = [self.dados["Data"]["Data"][n]["low"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Price"] = [self.dados["Data"]["Data"][n]["close"] for n in range(len(self.dados["Data"]["Data"]))]
        self.df["Volume"] = [self.dados["Data"]["Data"][n]["volumeto"] for n in range(len(self.dados["Data"]["Data"]))]       
        self.df.time = self.df.time.astype(int)
        self.df["Data"] = pd.to_datetime(self.df.time)
        if self.time == "day":
            for n in range(len(self.df)):
                    self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"]).date()
            self.df = self.df.drop(columns=["time"])
            self.df.set_index('Data', inplace=True)
            self.df = self.df.iloc[::-1]
        elif self.time == "hour":
            for n in range(len(self.df)):
                    self.df.loc[n, "Data"] = datetime.fromtimestamp(self.df.loc[n, "time"])
            self.df = self.df.drop(columns=["time"])
            self.df.set_index('Data', inplace=True)
            self.df = self.df.iloc[::-1]            

    

teste = Criptomoedas(10, "SOL", "hour")
print(teste.df)