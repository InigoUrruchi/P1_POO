import customtkinter
from src.simulacion.simulador import simulador
from customtkinter import filedialog
import threading

filepath = None
simulation = None
radio_actual = None
inclinacion_actual = None
nombre_bola = "ball1"
nombre_rampa = "ramp1"
i = 0
j = 0
old_x1 = 0
old_x2 = 0
old_y1 = 0
old_y2 = 0
customtkinter.set_appearance_mode("dark")

def cargar_configuracion():
    global simulation
    global radio_actual
    global inclinacion_actual
    global nombre_bola
    global nombre_rampa

    # Crear la ventana principal
    configurador = customtkinter.CTk()
    configurador.title("Configurar Simulación")
    configurador.geometry("800x600")
    configurador.grid_rowconfigure(0, weight=1)
    configurador.grid_columnconfigure(0, weight=1)
    background_color = configurador.cget("fg_color")

#FRAME PRINCIPAL

    frame_principal = customtkinter.CTkFrame(configurador, border_color = background_color, fg_color = background_color)
    frame_principal.grid(row = 0, column = 0,sticky = "nsew", columnspan = 4)
    frame_principal.grid_propagate(False)

#FRAME GRAFICA

    grafica = customtkinter.CTkFrame(frame_principal, border_color = background_color, fg_color = background_color)
    grafica.grid(row=1, column=2, rowspan=999, sticky="nsew", padx=20, pady=10)

    # configure grid layout (4x4)
    grafica.grid_columnconfigure(1, weight=1)
    grafica.grid_columnconfigure((2, 3), weight=0)
    grafica.grid_rowconfigure((0, 1, 2), weight=1)

    canvas, canvas_width, canvas_heigth = dibujar_ejes(grafica)
    representar_posiciones(canvas, canvas_width, canvas_heigth)
        
#/FRAME GRAFICA

#FRAME TITULO

    # Separador horizontal
    frame_titulo = customtkinter.CTkFrame(frame_principal, height = 0, border_width = 2, corner_radius = 0, fg_color = background_color)
    frame_titulo.grid(row=0, column=0, columnspan=9, sticky="new", pady=0)

    # Título centrado en la parte superior
    titulo = customtkinter.CTkLabel(frame_titulo, text="CONFIGURAR SIMULACIÓN", font=("Arial", 18, "bold"))
    titulo.pack(expand=True, pady= 5)

#/FRAME TITULO

#FRAME COLUMNA

    # Separador vertical
    columna = customtkinter.CTkFrame(frame_principal, width=20 ,border_width=2, corner_radius= 0, fg_color= background_color, border_color="grey")
    columna.grid(row=1, column=0, rowspan=999, sticky="ns", pady = 0)

    # Menú de opciones para seleccionar la bola
    menu_bola = customtkinter.CTkOptionMenu(columna, values=["ball1", "ball2"], command=lambda valor: print(f"Bola seleccionada: {valor}"))
    menu_bola.grid(row=2, column=1, padx=10, pady = 10)

    # Etiqueta para seleccionar el radio de la bola
    etiqueta_bola = customtkinter.CTkLabel(columna, text="Elige el radio de la bola", font=("Arial", 12))
    etiqueta_bola.grid(row=1, column=1, padx=10, pady=10)

    # Menú de opciones para seleccionar la rampa
    menu_rampa = customtkinter.CTkOptionMenu(columna, values=["ramp1", "ramp2"], command=lambda valor: print(f"Rampa seleccionada: {valor}"))
    menu_rampa.grid(row=5, column=1, padx=10, pady=10)

    # Etiqueta para seleccionar la inclinación de la rampa
    etiqueta_rampa = customtkinter.CTkLabel(columna, text="Elige la inclinación de la rampa", font=("Arial", 12))
    etiqueta_rampa.grid(row=4, column=1, padx=10, pady=10)

#/FRAME COLUMNA

#FRAME DERECHA

    frame_derecha = customtkinter.CTkFrame(frame_principal, width=20 ,border_width=2, corner_radius= 0, fg_color= background_color, border_color="grey")
    frame_derecha.grid(row=1, column=1, rowspan=999, sticky="ns")

    # Slider para elegir el radio de la bola
    elegir_radio = customtkinter.CTkSlider(frame_derecha, from_=0.1, to=2, command=lambda valor: llamar_actualizar_radio(valor, radio_actual, menu_bola.get()))
    elegir_radio.grid(row=1, column=0, padx=10, pady=10)

    # Mostrar el valor del radio actual
    radio_actual = customtkinter.CTkLabel(frame_derecha, text="Radio actual: 1.0", font=("Arial", 12))
    radio_actual.grid(row=0, column=0, padx=10, pady=10)

    # Slider para elegir la inclinación de la rampa
    elegir_inclinacion = customtkinter.CTkSlider(frame_derecha, from_=0.1, to=180, command=lambda valor: llamar_actualizar_inclinacion(valor, inclinacion_actual, menu_rampa.get()))
    elegir_inclinacion.grid(row=3, column=0, padx=10, pady=10)

    # Mostrar el valor de inclinación actual
    inclinacion_actual = customtkinter.CTkLabel(frame_derecha, text="Inclinación actual: 45.0", font=("Arial", 12))
    inclinacion_actual.grid(row=2, column=0, padx=10, pady=10)

    # Botón para reiniciar las posiciones de las bolas
    resetear_bolas = customtkinter.CTkButton(frame_derecha, text="Reiniciar las posiciones de las bolas", command=lambda: simulation.reiniciar_bolas(), fg_color="red")
    resetear_bolas.grid(row=4, column=0, columnspan=2, padx=15, pady=15)

#/FRAME DERECHA

#/FRAME PRINCIPAL

    configurador.mainloop()

#Iniciar la configuracion como un hilo
def configurar():
    hilo2 = threading.Thread(target = cargar_configuracion)
    hilo2.start()

#Iniciar el simulador
def simular():
    global filepath
    global simulation
    if filepath is not None:
        simulation = simulador(filepath)
        simulation.run()
    else:
        print("El archivo no existe")

#Inicia la simulacion dentro de un hilo
def iniciar_simulacion():
    hilo = threading.Thread(target = simular)
    hilo.start()

    #Activa el boton de configurar cuando se inicia la simulacion
    cargar.configure(state="enabled") 

#Selecciona el archivo XML y lo abre
def abrir_archivo():
    global filepath
    global simulation
    filepath = filedialog.askopenfilename(title="Abrir archivo configuración simulador", initialdir="./POO/Practica 1", filetypes=[("XML", "*.xml"),("Archivos .txt","*.txt")])
    open(filepath, 'r')

    #Activa el boton iniciar_simulacion cuando el filepath sea valido
    iniciar.configure(state = "enabled")
    return filepath

def dibujar_ejes(grafica):

    canvas_width = 650
    canvas_heigth = 650
    background_color = "#373F51"
    line2_color = "#4E5973"
    line_color = "#A9BCD0"

    centro_x = canvas_width/2
    centro_y = canvas_heigth/2

    canvas = customtkinter.CTkCanvas(grafica, width = canvas_width, height = canvas_heigth, bg = background_color )
    canvas.grid(row= 0, column=0, padx=20, pady=20)

    #Crear la cuadricula

    for x_grid in range(0, canvas_width, 25):
        canvas.create_line(x_grid, 0, x_grid, canvas_heigth, fill=line2_color, width=1)

    for y_grid in range(0, canvas_heigth, 25):
        canvas.create_line(0, y_grid, canvas_width, y_grid, fill=line2_color, width=1)
    
    #Dibujar eje y
    canvas.create_line(centro_x, canvas_heigth, centro_x, 0, fill=line_color, width=1)
    
    #Dibujar eje x
    canvas.create_line(0, centro_y, canvas_width, centro_y, fill=line_color, width=1)
    
    #Poner etiquetas eje x positivo
    for iX in range(0, canvas_width, 50):
        canvas.create_text(centro_x + iX, centro_y+10, text=str(iX), fill=line_color, anchor='e')
    
    #Poner etiquetas eje x negativo
    for iX in range(0, canvas_width, 50):
        canvas.create_text(centro_x - iX, centro_y + 10, text=str(-iX), fill=line_color, anchor='e')

    #Poner etiquetas eje y positivo
    for iY in range(0, canvas_heigth, 50):
        canvas.create_text(centro_x -5, centro_y - iY, text=str(iY), fill=line_color, anchor='e')
    
    #Poner etiquetas eje y negativo
    for iY in range(0, canvas_heigth, 50):
        canvas.create_text(centro_x -5, centro_y + iY, text=str(-iY), fill=line_color, anchor='e')

    
    return canvas, canvas_heigth, canvas_width

#Representar las funciones del movimiento de las bolas
def representar_posiciones(canvas, canvas_heigth, canvas_width):
        #Bola 1
        global i
        global j
        global old_y1
        global old_x1
        global old_x2
        global old_y2

        x1 = simulation.bola1_xpos*5
        y1 = simulation.bola1_zpos*5

        if i == 0:
             old_x1 = 0
             old_y1 = 5
        else:
             pass
        
        canvas.create_line( canvas_width/2 + old_x1, canvas_heigth/2 + old_y1, x1, y1, fill='red', width = 1)
        old_x1 = x1
        old_y1 = y1
        i+=1

        #Bola 2
        x2 = simulation.bola2_xpos*5
        y2 = simulation.bola2_zpos*5

        if j == 0:
             old_x2 = 2
             old_y2 = 4
        else:
            pass
        
        canvas.create_line( canvas_width/2 + old_x2, canvas_heigth/2 + old_y2, x2, y2, fill='blue', width = 1)
        old_x2 = x2
        old_y2 = y2
        j+=1
        canvas.after(1000, lambda: representar_posiciones(canvas, canvas_heigth, canvas_width))

def llamar_actualizar_radio(nuevo_valor, radio_actual, nombre_bola):
        #Actualiza el radio de la esfera
        simulation.actualizar_radio(nuevo_valor, nombre_bola)
        
        #Actualiza el valor en la etiqueta
        radio_actual.configure(text=f"Radio actual: {round(nuevo_valor, 2)}")

def llamar_actualizar_inclinacion(nuevo_valor, inclinacion_actual, nombre_rampa):
        #Actualiza la inclinacion de la rampa
        simulation.actualizar_inclinacion(nuevo_valor, nombre_rampa)

        #Actualiza el valor en la etiqueta
        inclinacion_actual.configure(text=f"Inclinacion actual: {round(nuevo_valor, 2)}")

def actualizar_datos_bola(nombre_bola, elegir_radio):
    global simulation
    #Obtener el valor del radio de la bola elegida
    valor_radio = simulation.obtener_radio(nombre_bola)

    #Cambia el valor que muestra la etiqueta por el de la bola elegid

    radio_actual.configure(text=f"Radio actual: {round(valor_radio, 2)}")

    #Cambia la posicion del slider a la correspondiente con la del radio de la bola elegida
    elegir_radio.set(valor_radio)
    print(f"Radio segunda bola: {elegir_radio.get()}")
    print("La posicion del slider se ha actualizado")

def actualizar_datos_rampa(nombre_rampa, elegir_inclinacion):
    global simulation
    print(f"Radio primera bola: {elegir_inclinacion.get()}")

    #Obtener el valor del radio de la bola elegida
    valor_inclinacion = simulation.obtener_inclinacion(nombre_rampa)

    #Cambia el valor que muestra la etiqueta por el de la bola elegid

    inclinacion_actual.configure(text=f"Inclinacion actual: {round(valor_inclinacion, 2)}")

    #Cambia la posicion del slider a la correspondiente con la del radio de la bola elegida
    elegir_inclinacion.set(valor_inclinacion)
    print(f"Radio segunda bola: {elegir_inclinacion.get()}")
    print("La posicion del slider se ha actualizado")

app = customtkinter.CTk()
app.title("My App")
app.geometry("600x300")

cargar = customtkinter.CTkButton(app, text="Cargar Configuracion", command=configurar, state = "disabled")
cargar.grid(row=0, column=1, padx=30, pady=100)

iniciar = customtkinter.CTkButton(app, text="Iniciar Simulacion", command=iniciar_simulacion, state="disabled")
iniciar.grid(row=0, column=2, padx=30, pady=100)

open_filedialog = customtkinter.CTkButton(app, command=abrir_archivo, text= "Abrir archivo")
open_filedialog.grid(row=0, column=3, padx=30, pady=100, sticky="w")

app.mainloop()

