from SRC.interfaceController import Interface

def main():
    """
    Função principal para iniciar a interface de usuário.

    Cria uma instância da classe Interface e chama o método inicializar_interface
    para configurar e exibir a interface gráfica do usuário.
    """
    teste = Interface()
    teste.inicializar_interface()

if __name__ == "__main__":
    main()
    """
    Executa a função principal se o script for executado diretamente.
    """
