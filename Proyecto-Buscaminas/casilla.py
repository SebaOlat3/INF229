from tkinter import *
from tkinter import messagebox as tkMessageBox


TAMANO_X = 10 # Tamaño en X
TAMANO_Y = 10 # Tamaño en Y

ESTADO_POR_DEFECTO = 0 # Estado por defecto
ESTADO_PULSADO = 1 # Estado pulsado
ESTADO_MARCADO = 2 # Estado marcado

CLICK_BOTON = "<Button-1>"  # Click botón
MARCADO_BOTON = "<Button-3>" # Marcado botón

ventana = None # Ventana

class Casilla: # Casilla
    def __init__(self, x, y, marco, imagenes): # Constructor
        self.x = x # X
        self.y = y # Y
        self.estado = ESTADO_POR_DEFECTO # Estado
        self.es_mina = False  # Esto se establecerá en el Tablero
        self.minas_cercanas = 0 # Minas cercanas
        self.boton = Button(marco, image=imagenes["simple"]) # Botón
        self.boton.grid(row=x+1, column=y) # Grid
        self.imagenes = imagenes # Imágenes

    def configurar_mina(self, es_mina): # Configurar mina
        self.es_mina = es_mina # Es mina

    def actualizar_minas_cercanas(self, minas_cercanas): # Actualizar minas cercanas 
        self.minas_cercanas = minas_cercanas # Minas cercanas  

    def revelar(self): # Revelar
        if self.es_mina: # Si es mina
            self.boton.config(image=self.imagenes["mina"]) # Configurar imagen de la mina
        else: # Si no
            self.boton.config(image=self.imagenes["numeros"][self.minas_cercanas]) # Configurar imagen de los números
        self.estado = ESTADO_PULSADO # Estado pulsado 

    def marcar(self): # Marcar 
        if self.estado == ESTADO_POR_DEFECTO: # Si el estado es por defecto
            self.boton.config(image=self.imagenes["bandera"]) # Configurar imagen de la bandera
            self.estado = ESTADO_MARCADO # Estado marcado
        elif self.estado == ESTADO_MARCADO: # Si el estado es marcado
            self.boton.config(image=self.imagenes["simple"]) # Configurar imagen simple
            self.estado = ESTADO_POR_DEFECTO # Estado por defecto

    def esquivocado(self): # Esquivocado
        if self.estado == ESTADO_MARCADO and not self.es_mina: # Si el estado es marcado y no es mina
            self.boton.config(image=self.imagenes["equivocado"]) # Configurar imagen equivocada