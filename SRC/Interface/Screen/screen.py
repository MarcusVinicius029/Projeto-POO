import tkinter as tk
from tkinter import ttk, messagebox

def coletar_dados():
    # Função interna que será chamada quando o botão for clicado
    def confirmar_selecao():
        global criptomoeda, semanas, previsao
        criptomoeda = combo_cripto.get()
        semanas = entry_semanas.get()
        previsao = var_previsao.get()

        # Validação dos campos de entrada
        if not criptomoeda:
            messagebox.showwarning("Aviso", "Por favor, insira o nome da criptomoeda.")
            return
        if not semanas.isdigit() or int(semanas) < 1:
            messagebox.showwarning("Aviso", "Por favor, insira um número válido de semanas.")
            return
        if previsao and criptomoeda not in ["Bitcoin", "Ethereum", "Solana"]:
            messagebox.showwarning("Aviso", "A previsão de dados só funciona com Bitcoin, Ethereum ou Solana.")
            return
        
        # Fechar a janela e retornar os dados
        root.quit()
        root.destroy()
        

    # Criação da janela principal
    root = tk.Tk()
    root.title("Previsão de Criptomoedas")
    root.geometry("300x320")
    root.resizable(False, False)
    



    # Rótulo e combobox para seleção de criptomoeda
    label_cripto = tk.Label(root, text="Escolha uma criptomoeda:", font=("Arial", 14))
    label_cripto.pack(pady=10)
    combo_cripto = ttk.Combobox(root, values=["Bitcoin", "Ethereum", "Solana"], font=("Arial", 12))
    combo_cripto.pack(pady=5)

    # Rótulo e campo de entrada para o número de semanas
    label_semanas = tk.Label(root, text="Número de semanas no gráfico:", font=("Arial", 14))
    label_semanas.pack(pady=10)
    entry_semanas = tk.Entry(root, font=("Arial", 12))
    entry_semanas.pack(pady=5)

    # Checkbox para previsão dos dados
    var_previsao = tk.BooleanVar()
    check_previsao = tk.Checkbutton(root, text="Previsão dos Dados", variable=var_previsao, font=("Arial", 12))
    check_previsao.pack(pady=10)

    # Botão para confirmar a seleção
    btn_confirmar = tk.Button(root, text="Confirmar Seleção", command=confirmar_selecao, font=("Arial", 12))
    btn_confirmar.pack(pady=20)

    # Inicialização da janela principal
    root.mainloop()

    return criptomoeda, semanas, previsao


# Testando a função
print(coletar_dados())
print(criptomoeda, semanas, previsao)
