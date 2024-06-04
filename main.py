import matplotlib.pyplot as plt
from SRC.Dados.DataController import DataControler
df = DataControler.get_moeda_df(moeda="bitcoin", model=True)
y_pred = DataControler.get_previsao(df, 10, "bitcoin")

df.Price.plot(color="black")
y_pred.plot(color="blue")
plt.show()