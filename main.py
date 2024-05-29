import matplotlib.pyplot as plt
import tkinter
from SRC.Dados.DataController import DataControler

locais = ["C:/Users/THIAGO/Desktop/POO/TrabalhoFinal/Projeto-POO/SRC/Dados/Data/DataSets/Bitcoin_26_03_2024-27_05_2024_historical_data_coinmarketcap.csv",
           "C:/Users/THIAGO/Desktop/POO/TrabalhoFinal/Projeto-POO/SRC/Dados/Data/DataSets/Ethereum_26_03_2024-27_05_2024_historical_data_coinmarketcap.csv",
           "C:/Users/THIAGO/Desktop/POO/TrabalhoFinal/Projeto-POO/SRC/Dados/Data/DataSets/Solana_29_05_2023-28_05_2024_historical_data_coinmarketcap.csv"]

DataControler.start(locais)
df = DataControler.solana_df
y_pred = DataControler.previsao_solana(5)
print(y_pred)
df.close.plot(color="black")
y_pred.plot(color="Orange")
plt.show()

