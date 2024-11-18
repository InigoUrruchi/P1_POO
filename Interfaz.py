import customtkinter
from src.simulacion.simulador import simulador
import xml.etree.ElementTree as ET
from customtkinter import filedialog
import threading

filepath = None
simulation = None
radio_actual = None
inclinacion_actual = None
nombre_bola = "ball1"
nombre_rampa = "ramp1"

def buscar_configuracion():
    buscador = customtkinter.CTk()
    buscador.title("Abrir Archivo")
    buscador.geometry("1000x1000")

    open_filedialog = customtkinter.CTkButton(buscador, command=abrir_archivo, text= "Abrir archivo")
    open_filedialog.grid(row=2, column=0, padx=19, pady=8, sticky="w")
    
    #Espera a que se elija un archivo, cuando se elije un archivo cierra la ventana
    while filepath is None:
        buscador.update()
    
    buscador.destroy()

def buscar_configuracion_hilo():
     hilo3 = threading.Thread(target = buscar_configuracion)
     hilo3.start()

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
    frame_principal.grid(row = 0, column = 0,sticky = "nsew")

#FRAME TITULO

    # Separador horizontal
    frame_titulo = customtkinter.CTkFrame(frame_principal, height = 10, border_width = 2, corner_radius = 0, fg_color = background_color)
    frame_titulo.grid(row=0, column=0, columnspan=2, sticky="ew", pady=0)

    # Título centrado en la parte superior
    titulo = customtkinter.CTkLabel(frame_titulo, text="CONFIGURAR SIMULACIÓN", font=("Arial", 18, "bold"))
    titulo.pack(expand=True, pady= 5)

#/FRAME TITULO

#FRAME COLUMNA

    # Separador vertical
    columna = customtkinter.CTkFrame(frame_principal, width=20 ,border_width=2, corner_radius= 0, fg_color= background_color, border_color="grey")
    columna.grid(row=1, column=0, rowspan=30, sticky="ns", pady = 0)

    # Menú de opciones para seleccionar la bola
    menu_bola = customtkinter.CTkOptionMenu(columna, values=["ball1", "ball2"], command=lambda valor: print(f"Bola seleccionada: {valor}"))
    menu_bola.grid(row=2, column=1, padx=10, pady = 5)

    # Etiqueta para seleccionar el radio de la bola
    etiqueta_bola = customtkinter.CTkLabel(columna, text="Elige el radio de la bola", font=("Arial", 12))
    etiqueta_bola.grid(row=1, column=1, padx=10, pady=5)

    # Menú de opciones para seleccionar la rampa
    menu_rampa = customtkinter.CTkOptionMenu(columna, values=["ramp1", "ramp2"], command=lambda valor: print(f"Rampa seleccionada: {valor}"))
    menu_rampa.grid(row=5, column=1, padx=10, pady=0)

    # Etiqueta para seleccionar la inclinación de la rampa
    etiqueta_rampa = customtkinter.CTkLabel(columna, text="Elige la inclinación de la rampa", font=("Arial", 12))
    etiqueta_rampa.grid(row=4, column=1, padx=10, pady=10)

#/FRAME COLUMNA

#FRAME DERECHA

    frame_derecha = customtkinter.CTkFrame(frame_principal, width=20 ,border_width=2, corner_radius= 0, fg_color= background_color, border_color="grey")
    frame_derecha.grid(row=1, column=1, rowspan=30, sticky="ns")

    # Slider para elegir el radio de la bola
    elegir_radio = customtkinter.CTkSlider(frame_derecha, from_=0.1, to=2, command=lambda valor: print(f"Radio: {valor}"))
    elegir_radio.grid(row=0, column=0, padx=10, pady=10)

    # Mostrar el valor del radio actual
    radio_actual = customtkinter.CTkLabel(frame_derecha, text="Radio actual: 1.0", font=("Arial", 12))
    radio_actual.grid(row=0, column=1, padx=10, pady=10)

    # Slider para elegir la inclinación de la rampa
    elegir_inclinacion = customtkinter.CTkSlider(frame_derecha, from_=0.1, to=180, command=lambda valor: print(f"Inclinación: {valor}"))
    elegir_inclinacion.grid(row=2, column=0, padx=10, pady=20)

    # Mostrar el valor de inclinación actual
    inclinacion_actual = customtkinter.CTkLabel(frame_derecha, text="Inclinación actual: 45.0", font=("Arial", 12))
    inclinacion_actual.grid(row=2, column=1, padx=10, pady=20)

    # Botón para reiniciar las posiciones de las bolas
    resetear_bolas = customtkinter.CTkButton(frame_derecha, text="Reiniciar las posiciones de las bolas", command=lambda: print("Bolas reiniciadas"), fg_color="red")
    resetear_bolas.grid(row=3, column=0, columnspan=2, padx=15, pady=15)

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
app.geometry("1000x800")

cargar = customtkinter.CTkButton(app, text="Cargar Configuracion", command=configurar, state = "disabled")
cargar.grid(row=0, column=0, padx=20, pady=20)

iniciar = customtkinter.CTkButton(app, text="Iniciar Simulacion", command=iniciar_simulacion, state="disabled")
iniciar.grid(row=1, column=0, padx=20, pady=20)

buscar = customtkinter.CTkButton(app, text="Buscar Archivo", command=buscar_configuracion_hilo)
buscar.grid(row=3, column=0, padx=20, pady=20)

app.mainloop()

