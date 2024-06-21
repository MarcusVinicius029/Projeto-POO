from SRC.interfaceController import Interface

class main:
    def __init__(self):
        """
        Classe para iniciar a interface de usuário.

        Cria uma instância da classe Interface e chama o método inicializar_interface
        para configurar e exibir a interface gráfica do usuário.
        """
        teste = Interface()
        teste.inicializar_interface()

if __name__ == "__main__":
    start = main()
    """
    Instacia a classe main e inica o seu construtor se o script for executado diretamente.
    """
