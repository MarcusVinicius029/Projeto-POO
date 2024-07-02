import tkinter as tk
from tkinter import ttk, messagebox
from .Dados.DataController import DataControler

class Interface:
    """
    Classe Interface para criar uma interface gráfica de usuário (GUI) utilizando Tkinter.
    Esta interface permite ao usuário selecionar uma criptomoeda, um período de tempo, 
    e optar por prever os dados ou visualizar a cotação do dólar.

    Atributos:
        criptomoeda (str): Nome da criptomoeda selecionada.
        momento (int): Número de dias, horas ou minutos selecionados.
        previsao (bool): Indicador se a previsão dos dados foi selecionada.
        periodo (str): Período de tempo selecionado (dia, minutos, horas).
        root (tk.Tk): Janela principal da GUI.
        cotacao (bool): Indicador se a cotação do dólar foi selecionada.
    """
    
    def __init__(self):
        """
        Inicializa a classe Interface com atributos padrão.
        """
        self.criptomoeda = None
        self.momento = None
        self.previsao = False
        self.periodo = None
        self.root = None
        self.cotacao = False

    def inicializar_interface(self):
        """
        Inicializa a interface gráfica do usuário com widgets Tkinter.
        """
        self.root = tk.Tk()  # Cria a janela principal
        self.root.title("Previsão de Criptomoedas")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        # Rótulo e combobox para seleção de criptomoeda
        label_cripto = tk.Label(self.root, text="Escolha uma criptomoeda:", font=("Arial", 14))
        label_cripto.pack(pady=10)
        self.combo_cripto = ttk.Combobox(self.root, values=["Bitcoin", "Ethereum", "Solana", "Dogecoin"], font=("Arial", 12))
        self.combo_cripto.pack(pady=5)

        # Rótulo e entry para entrada de momento (dias, horas ou minutos)
        label_momento = tk.Label(self.root, text="Número de (dias, horas ou minutos):", font=("Arial", 14))
        label_momento.pack(pady=10)
        self.entry_momento = tk.Entry(self.root, font=("Arial", 12))
        self.entry_momento.pack(pady=5)

        # Checkbox para previsão dos dados
        self.var_previsao = tk.BooleanVar()
        check_previsao = tk.Checkbutton(self.root, text="Previsão dos Dados", variable=self.var_previsao, font=("Arial", 12),
                                        command=self.on_previsao_check)
        check_previsao.pack(pady=10)

        # Checkbox para cotação do dólar
        self.var_cotacao = tk.BooleanVar()
        check_cotacao = tk.Checkbutton(self.root, text="Cotação do dólar", variable=self.var_cotacao, font=("Arial", 12),
                                        command=self.on_cotacao_check)
        check_cotacao.pack(pady=10)

        # Rótulo e radiobuttons para seleção de período
        label_periodo = tk.Label(self.root, text="Selecione o período:", font=("Arial", 14))
        label_periodo.pack(pady=10)

        self.var_periodo = tk.StringVar()
        periodos = [("Dia", "day"), ("Horas", "hour"), ("Minutos", "minute")]
        for texto, valor in periodos:
            radio = tk.Radiobutton(self.root, text=texto, variable=self.var_periodo, value=valor, font=("Arial", 12))
            radio.pack()  

        # Botão para confirmar a seleção
        btn_confirmar = tk.Button(self.root, text="Confirmar Seleção", command=self.confirmar_selecao, font=("Arial", 12))
        btn_confirmar.pack(pady=20)

        # Mantendo a janela aberta
        self.root.mainloop()

    def on_previsao_check(self):
        """
        Callback para o checkbox de previsão.
        Se selecionado, define o período como "dia".
        """
        if self.var_previsao.get():
            self.var_periodo.set("day")
    
    def on_cotacao_check(self):
        """
        Callback para o checkbox de cotação do dólar.
        Se selecionado, limpa a seleção de criptomoeda.
        """
        if self.var_cotacao.get():
            self.combo_cripto.set("")

    def criar_popup(self):
        """
        Cria e exibe um popup com a cotação atual do dólar.
        """
        def on_closing():
            popup.destroy()  # Fecha o popup

        root = tk.Tk()
        root.withdraw()  # Oculta a janela principal 

        popup = tk.Toplevel(root)  # Cria uma nova janela de popup
        popup.title("Popup")
        popup.geometry("300x150")

        # Obtém a cotação atual do dólar e exibe no popup
        cotacao_atual = round(DataControler.get_moeda_df(1, "dolar", time = "day", atual=True)["Compra"].values[0], 2)
        popup_label = tk.Label(popup, text=f"A cotação atual do dólar é {cotacao_atual} reais", font=("Arial", 12))
        popup_label.pack(pady=20)

        close_button = tk.Button(popup, text="Fechar", command=on_closing, font=("Arial", 12))
        close_button.pack(pady=10)

    def confirmar_selecao(self):
        """
        Callback para o botão de confirmação.
        Coleta os dados da interface e chama métodos apropriados do DataControler para
        gerar gráficos ou previsões com base na seleção do usuário.
        """
        self.criptomoeda = self.combo_cripto.get()  # Obtém a criptomoeda selecionada
        self.momento = self.entry_momento.get()  # Obtém o momento (dias, horas ou minutos) inserido
        self.previsao = self.var_previsao.get()  # Verifica se previsão foi selecionada
        self.periodo = self.var_periodo.get()  # Obtém o período selecionado
        self.cotacao = self.var_cotacao.get()  # Verifica se cotação do dólar foi selecionada

        if self.previsao:
            self.var_periodo.set("day")
            self.var_cotacao.set(False)

        # Ajusta o nome da criptomoeda para o formato esperado pelo DataControler
        if self.criptomoeda == "Bitcoin":
            self.criptomoeda = "BTC"
        elif self.criptomoeda == "Ethereum":
            self.criptomoeda = "ETH"
        elif self.criptomoeda == "Solana":
            self.criptomoeda = "SOL"
        elif self.criptomoeda == "Dogecoin":
            self.criptomoeda = "DOGE"

        # Se a cotação do dólar foi selecionada, exibe o popup e ajusta os parâmetros
        if self.cotacao:
            self.criar_popup()
            self.momento = 1
            self.criptomoeda = "dolar"

        # Validações das entradas do usuário
        if not self.criptomoeda:
            messagebox.showwarning("Aviso", "Por favor, insira o nome da criptomoeda.")
            return
        if int(self.momento) < 1:
            messagebox.showwarning("Aviso", "Por favor, insira um número válido.")
            return
        if self.previsao and self.criptomoeda not in ["BTC", "ETH", "SOL"]:
            messagebox.showwarning("Aviso", "A previsão de dados só funciona com Bitcoin, Ethereum ou Solana.")
            return
        
        # Gera o gráfico ou previsão de acordo com os parâmetros fornecidos
        try:
            n = int(self.momento)
            if self.previsao:
                DataControler.get_grafico_previsao(self.criptomoeda, n)
            else:
                time_period = self.periodo
                DataControler.get_grafico_df(self.criptomoeda, n, time_period)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        
        # Finaliza a aplicação
        self.root.mainloop()
        self.root.quit()
        self.root.destroy()
