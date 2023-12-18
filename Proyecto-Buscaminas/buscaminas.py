from tkinter import *
from tkinter import messagebox as tkMessageBox
from tkinter import simpledialog
from tkinter import Tk, PhotoImage
from PIL import Image, ImageTk
from collections import deque
import random
from datetime import datetime
from tablero import Tablero

TAMANO_X = 10 # Tamaño en X
TAMANO_Y = 10 # Tamaño en Y

ESTADO_POR_DEFECTO = 0 # Estado por defecto
ESTADO_PULSADO = 1 # Estado pulsado
ESTADO_MARCADO = 2 # Estado marcado

CLICK_BOTON = "<Button-1>" # Click botón
MARCADO_BOTON = "<Button-3>" # Marcado botón

ventana = None # Ventana

class Buscaminas: # Buscaminas 
    def __init__(self, tk): # Constructor
        self.imagenes = { # Imágenes
            "simple": PhotoImage(file = "images/tile_plain.gif"),   
            "clickeado": PhotoImage(file = "images/tile_clicked.gif"),
            "mina": PhotoImage(file = "images/tile_mine.gif"),
            "bandera": PhotoImage(file = "images/tile_flag.gif"),
            "equivocado": PhotoImage(file = "images/tile_wrong.gif"),
            "numeros": [] # Números 
        }
        for i in range(1, 9): # Para I en el rango de 1 a 9
            self.imagenes["numeros"].append(PhotoImage(file = "images/tile_"+str(i)+".gif")) # Agregar a la lista de números la imagen de los números 
        try:
            image_path = "images/menu2.png" # Ruta de la imagen de fondo
            self.fondo_imagen = ImageTk.PhotoImage(Image.open(image_path)) # Imagen de fondo 
        except IOError:
            tkMessageBox.showerror("Error", "No se pudo cargar la imagen de fondo.") # Mostrar error
            return
        
        # configurar marco
        self.tk = tk # Tk 
        self.marco = Frame(self.tk) # Marco 
        self.marco.pack() # Pack 
        

        # configurar etiquetas/UI
        self.etiquetas = { # Etiquetas 
            "tiempo": Label(self.marco, text = "00:00:00"), # Tiempo 
            "minas": Label(self.marco, text = "Minas: 0"), # Minas 
            "banderas": Label(self.marco, text = "Banderas: 0") # Banderas
        }
        self.etiquetas["tiempo"].grid(row = 0, column = 0, columnspan = TAMANO_Y) # ancho completo arriba
        self.etiquetas["minas"].grid(row = TAMANO_X+1, column = 0, columnspan = int(TAMANO_Y/2)) # abajo izquierda
        self.etiquetas["banderas"].grid(row = TAMANO_X+1, column = int(TAMANO_Y/2)-1, columnspan = int(TAMANO_Y/2)) # abajo derecha

        self.reiniciar() # iniciar juego
        self.actualizarTemporizador() # iniciar temporizador


    def reiniciar(self): # Reiniciar
        self.juegoTerminado = False 
        # Primero, limpiar el marco actual y cualquier widget dentro de él
        self.marco.destroy() 
        
        # Crear un nuevo marco y configurar la interfaz del juego
        self.marco = Frame(self.tk)
        self.marco.pack()
        
        # Reconfigurar etiquetas/UI
        self.etiquetas = {
            "tiempo": Label(self.marco, text="00:00:00"),
            "minas": Label(self.marco, text="Minas: 0"),
            "banderas": Label(self.marco, text="Banderas: 0")
        }
        self.etiquetas["tiempo"].grid(row=0, column=0, columnspan=TAMANO_Y)
        self.etiquetas["minas"].grid(row=TAMANO_X+1, column=0, columnspan=int(TAMANO_Y/2))
        self.etiquetas["banderas"].grid(row=TAMANO_X+1, column=int(TAMANO_Y/2)-1, columnspan=int(TAMANO_Y/2))

        # Restablecer las variables del juego y reconstruir la cuadrícula de botones
        self.configurar()

        # Reiniciar el temporizador
        self.horaInicio = None  # Hora de inicio
        self.actualizarTemporizador() # Actualizar temporizador

    def actualizarTemporizador(self): # Actualizar temporizador
        if not self.juegoTerminado:
            tiempoTranscurrido = "00:00:00"
            if self.horaInicio != None: # Si la hora de inicio no es nula
                delta = datetime.now() - self.horaInicio # Delta
                tiempoTranscurrido = str(delta).split('.')[0] # eliminar ms
                if delta.total_seconds() < 36000: # Si el tiempo total es menor a 36000
                    tiempoTranscurrido = "0" + tiempoTranscurrido # agregar cero al inicio
            self.etiquetas["tiempo"].config(text = tiempoTranscurrido) # Configurar texto del tiempo
            self.marco.after(100, self.actualizarTemporizador) 


    def mostrarMenu(self):
    # Destruir el marco actual y cualquier widget dentro de él
        self.marco.destroy()    # Destruir marco
        self.marco = Frame(self.tk) # Marco
        self.marco.pack(fill=BOTH, expand=YES) # Pack

        # Cargar la imagen de fondo
        fondo_imagen = PhotoImage(file="images/menu2.png") # Imagen de fondo

        # Crear un Canvas o Label y poner la imagen de fondo
        fondo = Label(self.marco, image=fondo_imagen) 
        fondo.image = fondo_imagen  # Mantener una referencia para que no sea recolectada por el recolector de basura
        fondo.place(x=0, y=0, relwidth=1, relheight=1)

        # Crear un nuevo marco para el menú sobre el fondo
        
        #menu_marco = Frame(fondo, bg="white")
        parent_bg = fondo.cget('bg') # Color de fondo del padre
        menu_marco = Frame(fondo, bg=parent_bg) # Marco del menú

        menu_marco.pack(pady=50) # Pack

        # Agregar botón para iniciar un nuevo juego
        btn_nuevo_juego = Button(menu_marco, text="Nuevo Juego", command=self.reiniciar) # Botón de nuevo juego
        btn_nuevo_juego.pack(fill=X, padx=10, pady=5) # Pack  

        # Agregar botón para ver el top 10 de puntajes
        btn_top10 = Button(menu_marco, text="Ver Top 10", command=self.mostrarTop10) # Botón de ver top 10
        btn_top10.pack(fill=X, padx=10, pady=5) # Pack 

        # Agregar botón para salir del juego
        btn_salir = Button(menu_marco, text="Salir", command=self.tk.quit) # Botón de salir
        btn_salir.pack(fill=X, padx=10, pady=5) # Pack

    def mostrarTop10(self):
        # Mostrar una ventana con los mejores puntajes
        top10 = self.cargarTop10() # Cargar top 10
        mensaje = "\n".join(f"{puntaje['nombre']}: {puntaje['tiempo']}" for puntaje in top10) # Mensaje 
        tkMessageBox.showinfo("Top 10 Puntajes", mensaje) # Mostrar mensaje

    def guardarPuntaje(self, nombre, tiempo): # Guardar puntaje
        # Ruta del archivo dentro de la subcarpeta 'datos'
        ruta_archivo = "datos/puntajes.txt" # Ruta del archivo

        try:
            with open(ruta_archivo, "a") as archivo: # Abrir archivo
                archivo.write("{}: {}\n".format(nombre, tiempo)) # Escribir en el archivo
        except IOError: 
            tkMessageBox.showwarning("Advertencia", "No se pudo guardar el puntaje.") # Mostrar advertencia

    def cargarTop10(self): # Cargar top 10
        ruta_archivo = "datos/puntajes.txt" # Ruta del archivo
        try:    # Intentar abrir el archivo
            with open(ruta_archivo, "r") as archivo: # Abrir archivo
                lineas = archivo.readlines() # Leer líneas
            puntajes = [self.parsearPuntaje(linea) for linea in lineas] # Puntajes 
            return puntajes # Devolver puntajes
        except IOError:
            return [] # Devolver lista vacía

    @staticmethod
    def parsearPuntaje(linea): # Parsear puntaje
        partes = linea.strip().split(": ") # Partes 
        return {"nombre": partes[0], "tiempo": float(partes[1])} # Devolver nombre y tiempo

    def obtenerTiempoJuego(self): # Obtener tiempo de juego
        # Calcular y devolver el tiempo total de juego en segundos
        delta = datetime.now() - self.horaInicio # Delta 
        return delta.total_seconds() # Devolver tiempo total

    def configurar(self): # Configurar
        # crear variables para banderas y casillas pulsadas
        self.contadorBanderas = 0 # Contador de banderas
        self.contadorBanderasCorrectas = 0 # Contador de banderas correctas
        self.contadorPulsadas = 0 # Contador de pulsadas
        self.horaInicio = None # Hora de inicio

        # crear botones
        self.casillas = dict({}) # Casillas 
        self.minas = 0 # Minas
        for x in range(0, TAMANO_X): # Para X en el rango de 0 al tamaño en X
            for y in range(0, TAMANO_Y): # Para Y en el rango de 0 al tamaño en Y
                if y == 0: # Si Y es igual a 0
                    self.casillas[x] = {} # Agregar diccionario vacío

                identificador = str(x) + "_" + str(y) # Identificador
                esMina = False  # Esto se establecerá en el Tablero 

                # imagen del botón cambiable por razones de depuración:
                grafico = self.imagenes["simple"] # Gráfico

                # cantidad actualmente aleatoria de minas
                if random.uniform(0.0, 1.0) < 0.1: # Si un número aleatorio entre 0 y 1 es menor a 0.1
                    esMina = True # Es mina 
                    self.minas += 1 # Minas

                casilla = {
                    "id": identificador, # Identificador 
                    "esMina": esMina, # Es mina
                    "estado": ESTADO_POR_DEFECTO, # Estado por defecto
                    "coordenadas": {"x": x,"y": y}, # Coordenadas
                    "boton": Button(self.marco, image = grafico), # Botón
                    "minasCercanas": 0 # se calcula después de construir la cuadrícula
                }

                casilla["boton"].bind(CLICK_BOTON, self.envoltorioClick(x, y)) # Click botón
                casilla["boton"].bind(MARCADO_BOTON, self.envoltorioClickDerecho(x, y)) # Marcado botón
                casilla["boton"].grid( row = x+1, column = y ) # desplazado por 1 fila para el temporizador

                self.casillas[x][y] = casilla # Agregar casilla

        # bucle de nuevo para encontrar minas cercanas y mostrar número en la casilla
        for x in range(0, TAMANO_X): # Para X en el rango de 0 al tamaño en X
            for y in range(0, TAMANO_Y): # Para Y en el rango de 0 al tamaño en Y
                contadorMinasCercanas = 0 # Contador de minas cercanas
                for vecino in self.obtenerVecinos(x, y): # Para vecino en obtener vecinos de X y Y
                    contadorMinasCercanas += 1 if vecino["esMina"] else 0 # Contador de minas cercanas
                self.casillas[x][y]["minasCercanas"] = contadorMinasCercanas # Minas cercanas

    def finJuego(self, gano): # Fin de juego
        self.juegoTerminado = False # Juego terminado
        for x in range(0, TAMANO_X): # Para X en el rango de 0 al tamaño en X
            for y in range(0, TAMANO_Y): # Para Y en el rango de 0 al tamaño en Y
                if self.casillas[x][y]["esMina"] == False and self.casillas[x][y]["estado"] == ESTADO_MARCADO: # Si la casilla de X y Y no es mina y el estado es marcado
                    self.casillas[x][y]["boton"].config(image = self.imagenes["equivocado"]) # Configurar imagen equivocada
                if self.casillas[x][y]["esMina"] == True and self.casillas[x][y]["estado"] != ESTADO_MARCADO: # Si la casilla de X y Y es mina y el estado no es marcado
                    self.casillas[x][y]["boton"].config(image = self.imagenes["mina"]) # Configurar imagen de la mina

        self.tk.update() # Actualizar Tk

        if gano: # Si ganó
            self.juegoTerminado = True # Juego terminado
            tiempoActual = self.obtenerTiempoJuego() # Tiempo actual
            nombre = simpledialog.askstring("Ganaste", "Ingresa tu nombre:") # Nombre
            if nombre: # Si hay nombre
                self.guardarPuntaje(nombre, tiempoActual) # Guardar puntaje
            
            respuesta = tkMessageBox.askyesno("Ganaste", "¿Jugar de nuevo?")  # Preguntar si quiere jugar de nuevo
        else: # Si no
            respuesta = tkMessageBox.askyesno("Perdiste", "¿Jugar de nuevo?") # Preguntar si quiere jugar de nuevo
        
        if respuesta: # Si la respuesta es sí
            self.reiniciar() # Reiniciar
        else: # Si no
            self.mostrarMenu() # Mostrar menú 

    def actualizarEtiquetas(self): # Actualizar etiquetas
        self.etiquetas["banderas"].config(text = "Banderas: "+str(self.contadorBanderas)) # Configurar texto de las banderas
        self.etiquetas["minas"].config(text = "Minas: "+str(self.minas)) # Configurar texto de las minas


    def obtenerVecinos(self, x, y): # Obtener vecinos
        vecinos = [] # Vecinos
        coordenadas = [ # Coordenadas
            {"x": x-1,  "y": y-1},  # arriba derecha
            {"x": x-1,  "y": y},    # arriba centro
            {"x": x-1,  "y": y+1},  # arriba izquierda
            {"x": x,    "y": y-1},  # izquierda
            {"x": x,    "y": y+1},  # derecha
            {"x": x+1,  "y": y-1},  # abajo derecha
            {"x": x+1,  "y": y},    # abajo centro
            {"x": x+1,  "y": y+1},  # abajo izquierda
        ]
        for coordenada in coordenadas: # Para coordenada en coordenadas
            try: # Intentar
                vecinos.append(self.casillas[coordenada["x"]][coordenada["y"]]) # Agregar vecinos
            except KeyError: # Excepción
                pass # Pasar
        return vecinos # Devolver vecinos 

    def envoltorioClick(self, x, y): # Envoltorio click 
        return lambda Boton: self.alClick(self.casillas[x][y]) # Devolver lambda 

    def envoltorioClickDerecho(self, x, y):     # Envoltorio click derecho
        return lambda Boton: self.alClickDerecho(self.casillas[x][y]) # Devolver lambda 

    def alClick(self, casilla): # Al click 
        if self.horaInicio == None:     # Si la hora de inicio es nula
            self.horaInicio = datetime.now() # Hora de inicio
 
        if casilla["esMina"] == True: # Si la casilla es mina 
            # fin del juego
            self.finJuego(False) # Fin de juego
            return # Devolver 

        # cambiar imagen
        if casilla["minasCercanas"] == 0: # Si las minas cercanas son 0 
            casilla["boton"].config(image = self.imagenes["clickeado"]) # Configurar imagen clickeado
            self.despejarCasillasVecinas(casilla["id"]) # Despejar casillas vecinas
        else: # Si no
            casilla["boton"].config(image = self.imagenes["numeros"][casilla["minasCercanas"]-1]) # Configurar imagen de los números
        # si no estaba ya clickeado, cambiar estado y contar
        if casilla["estado"] != ESTADO_PULSADO: # Si el estado no es pulsado
            casilla["estado"] = ESTADO_PULSADO # Estado pulsado
            self.contadorPulsadas += 1 # Contador de pulsadas 
        if self.contadorPulsadas == (TAMANO_X * TAMANO_Y) - self.minas: # Si el contador de pulsadas es igual al tamaño en X por el tamaño en Y menos las minas
            self.finJuego(True) # Fin de juego

    def alClickDerecho(self, casilla): # Al click derecho
        if self.horaInicio == None: # Si la hora de inicio es nula
            self.horaInicio = datetime.now() # Hora de inicio

        # si no está clickeado
        if casilla["estado"] == ESTADO_POR_DEFECTO: # Si el estado es por defecto
            casilla["boton"].config(image = self.imagenes["bandera"]) # Configurar imagen de la bandera
            casilla["estado"] = ESTADO_MARCADO # Estado marcado
            casilla["boton"].unbind(CLICK_BOTON) # Desvincular click botón
            # si es una mina
            if casilla["esMina"] == True: # Si la casilla es mina
                self.contadorBanderasCorrectas += 1 # Contador de banderas correctas
            self.contadorBanderas += 1 # Contador de banderas
            self.actualizarEtiquetas() # Actualizar etiquetas
        # si estaba marcada, desmarcar
        elif casilla["estado"] == ESTADO_MARCADO: # Si el estado es marcado
            casilla["boton"].config(image = self.imagenes["simple"]) # Configurar imagen simple
            casilla["estado"] = ESTADO_POR_DEFECTO # Estado por defecto
            casilla["boton"].bind(CLICK_BOTON, self.envoltorioClick(casilla["coordenadas"]["x"], casilla["coordenadas"]["y"])) # Vincular click botón 
            # si es una mina
            if casilla["esMina"] == True: # Si la casilla es mina
                self.contadorBanderasCorrectas -= 1 # Contador de banderas correctas
            self.contadorBanderas -= 1 # Contador de banderas
            self.actualizarEtiquetas() # Actualizar etiquetas 

    def despejarCasillasVecinas(self, identificador): # Despejar casillas vecinas
        cola = deque([identificador]) # Cola 

        while len(cola) != 0: # Mientras la longitud de la cola sea diferente de 0
            clave = cola.popleft() # Clave
            partes = clave.split("_") # Partes
            x = int(partes[0]) # X
            y = int(partes[1]) # Y

            for casilla in self.obtenerVecinos(x, y): # Para casilla en obtener vecinos de X y Y
                self.despejarCasilla(casilla, cola) # Despejar casilla

    def despejarCasilla(self, casilla, cola): # Despejar casilla
        if casilla["estado"] != ESTADO_POR_DEFECTO:   # Si el estado no es por defecto
            return # Devolver

        if casilla["minasCercanas"] == 0: # Si las minas cercanas son 0 
            casilla["boton"].config(image = self.imagenes["clickeado"]) # Configurar imagen clickeado
            cola.append(casilla["id"]) # Agregar a la cola
        else:
            casilla["boton"].config(image = self.imagenes["numeros"][casilla["minasCercanas"]-1]) # Configurar imagen de los números

        casilla["estado"] = ESTADO_PULSADO # Estado pulsado
        self.contadorPulsadas += 1 # Contador de pulsadas


