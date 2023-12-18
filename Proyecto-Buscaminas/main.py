from buscaminas import Buscaminas
from tkinter import Tk

def main():
    # crear instancia de Tk
    ventana = Tk()
    ventana.geometry("300x300")

    # establecer título del programa
    ventana.title("Buscaminas")
    # crear instancia del juego
    buscaminas = Buscaminas(ventana)
    # Mostrar el menú antes de iniciar el bucle principal
    buscaminas.mostrarMenu()
    # ejecutar bucle de eventos
    ventana.mainloop()

if __name__ == "__main__":
    main()

