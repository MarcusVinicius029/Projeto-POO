import matplotlib.pyplot as plt
from SRC.Dados.DataController import DataControler

locais = ["Caminho local do arquivo de dataset do Bitcoin",
           "Caminho local do arquivo de dataset do Ehtereum",
           "Caminho local do arquivo de dataset da Solana"]
DataControler.start(locais)
df = DataControler.solana_df
y_pred = DataControler.previsao_solana(5)
print(y_pred)
df.close.plot(color="black")
y_pred.plot(color="Orange")
plt.show()

