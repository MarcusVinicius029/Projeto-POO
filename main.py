import matplotlib.pyplot as plt
from SRC.Dados.DataController import DataControler
df = DataControler.get_moeda_df(moeda = "dolar", atual=True)

print(df)