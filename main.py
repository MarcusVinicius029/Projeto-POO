import matplotlib.pyplot as plt
from SRC.Dados.DataController import DataControler
df = DataControler.get_moeda_df(moeda = "bitcoin", atual=False, n=10)

print(df)