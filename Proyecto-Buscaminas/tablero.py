from tkinter import *


import random
from casilla import Casilla

TAMANO_X = 10
TAMANO_Y = 10

ESTADO_POR_DEFECTO = 0
ESTADO_PULSADO = 1
ESTADO_MARCADO = 2

CLICK_BOTON = "<Button-1>"
MARCADO_BOTON = "<Button-3>"

ventana = None
class Tablero: # Tablero
    def __init__(self, tamano_x, tamano_y, marco, imagenes): # Constructor
        self.tamano_x = tamano_x # Tamaño en X
        self.tamano_y = tamano_y # Tamaño en Y
        self.casillas = [[Casilla(x, y, marco, imagenes) for y in range(tamano_y)] for x in range(tamano_x)] # Casillas
        self.distribuir_minas() # Distribuir minas
        self.calcular_minas_cercanas() # Calcular minas cercanas

    def distribuir_minas(self): # Distribuir minas
        minas_plantadas = 0 # Minas plantadas
        while minas_plantadas < (self.tamano_x * self.tamano_y * 0.1):  # Mientras minas plantadas sea menor que el tamaño en X por el tamaño en Y por 0.1
            x = random.randint(0, self.tamano_x - 1) # X
            y = random.randint(0, self.tamano_y - 1) # Y
            if not self.casillas[x][y].es_mina: 
                self.casillas[x][y].configurar_mina(True) # Configurar mina
                minas_plantadas += 1 # Minas plantadas

    def calcular_minas_cercanas(self): # Calcular minas cercanas
        for x in range(self.tamano_x): # Para X en el rango del tamaño en X
            for y in range(self.tamano_y): 
                if not self.casillas[x][y].es_mina: 
                    minas_cercanas = self.contar_minas_cercanas(x, y) # Minas cercanas
                    self.casillas[x][y].actualizar_minas_cercanas(minas_cercanas) # Actualizar minas cercanas

    def contar_minas_cercanas(self, x, y): # Contar minas cercanas
        minas_cercanas = 0 # Minas cercanas
        for dx in [-1, 0, 1]: # Para DX en -1, 0, 1
            for dy in [-1, 0, 1]: # Para DY en -1, 0, 1
                nx, ny = x + dx, y + dy # NX, NY
                if 0 <= nx < self.tamano_x and 0 <= ny < self.tamano_y: # Si 0 es menor o igual que NX y NX es menor que el tamaño en X y 0 es menor o igual que NY y NY es menor que el tamaño en Y
                    if self.casillas[nx][ny].es_mina: # Si las casillas de NX y NY son minas
                        minas_cercanas += 1    # Minas cercanas
        return minas_cercanas # Minas cercanas