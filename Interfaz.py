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

def pulsar_boton():
    print("Boton pulsado")

def buscar_configuracion():
    buscador = customtkinter.CTk()
    buscador.title("configurar")
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


    configurador = customtkinter.CTk()
    configurador.title("configurar")
    configurador.geometry("1000x1000")

    #Abre el buscador de archivos
    '''open_filedialog = customtkinter.CTkButton(configurador, command=abrir_archivo, text= "Abrir archivo")
    open_filedialog.grid(row=3, column=2, padx=19, pady=8, sticky="w")

    #Muestra el archivo que se esta usando en tiempo real
    archivo_actual = customtkinter.CTkLabel(configurador, text= filepath)
    archivo_actual.grid(row=3, column=1, padx=20, pady=20)'''
    #Actualiza el valor del radio de la bola
    elegir_radio = customtkinter.CTkSlider(configurador, from_=0.1, to=2, command=lambda valor: llamar_actualizar_radio(valor, radio_actual, menu_bola.get()))
    elegir_radio.grid(row=1, column=2, padx=20, pady=20)

    #Muestra el valor del radio de la bola en tiempo real
    radio_actual = customtkinter.CTkLabel(configurador, text=f"Radio actual: {simulation.obtener_radio(nombre_bola)}")
    radio_actual.grid(row=1, column=1, padx=10, pady=10)

    menu_bola = customtkinter.CTkOptionMenu(configurador, values=["ball1", "ball2"], command=lambda valor: actualizar_datos_bola(valor, elegir_radio))
    menu_bola.grid(row=0, column=2, padx=20, pady=20)

    menu_rampa = customtkinter.CTkOptionMenu(configurador, values=["ramp1", "ramp2"], command= lambda valor : actualizar_datos_rampa(valor, elegir_inclinacion))
    menu_rampa.grid(row=0, column=4, padx=20, pady=20)

    etiqueta_bola = customtkinter.CTkLabel(configurador, text = "Elige la bola")
    etiqueta_bola.grid(row=0, column=1, padx=10, pady=20)

    etiqueta_rampa = customtkinter.CTkLabel(configurador, text = "Elige la rampa")
    etiqueta_rampa.grid(row=0, column=3, padx=10, pady=20)

    elegir_inclinacion = customtkinter.CTkSlider(configurador, from_=0.1, to=180, command=lambda valor: llamar_actualizar_inclinacion(valor, inclinacion_actual, menu_rampa.get()))
    elegir_inclinacion.grid(row=2, column=2, padx=20, pady=20)

    inclinacion_actual = customtkinter.CTkLabel(configurador, text=f"Inclinacion actual: {simulation.obtener_inclinacion(nombre_rampa)}")
    inclinacion_actual.grid(row=2, column=1, padx=10, pady=10)

    resetear_bolas = customtkinter.CTkButton(configurador, text="Reiniciar las posiciones de las bolas", command=lambda: simulation.reiniciar_bolas(), fg_color= 'red')
    resetear_bolas.grid(row=3, column=0, padx=20, pady=20)

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
    print ("la ruta del archivo es:",filepath,)

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
    
    print(f"Radio primera bola: {elegir_radio.get()}")

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


'''def elegir_id(valor, elegir_radio):
    print(valor)
    global id_rampa
    global id_bola

    if valor == "ramp1":
         id_rampa = 1
    elif valor == "ramp2":
         id_rampa = 2
    elif valor == "ball1":
         id_bola = 3
    elif valor == "ball2":
         id_bola = 4
    else:
         print("El objeto no existe")
    
    actualizar_datos_bola(id_bola, elegir_radio)

    print("rampa: ",id_rampa)
    print("bola: ",id_bola)
    return id_bola, id_rampa'''
         

'''def id_objeto():
    global simulation
    simulation.obtener_id("ramp1")
    simulation.obtener_id("ramp2")
    simulation.obtener_id("ball1")
    simulation.obtener_id("ball2")'''

app = customtkinter.CTk()
app.title("my app")
app.geometry("1000x800")

cargar = customtkinter.CTkButton(app, text="Cargar Configuracion", command=configurar, state = "disabled")
cargar.grid(row=0, column=0, padx=20, pady=20)

iniciar = customtkinter.CTkButton(app, text="Iniciar Simulacion", command=iniciar_simulacion, state="disabled")
iniciar.grid(row=1, column=0, padx=20, pady=20)

buscar = customtkinter.CTkButton(app, text="Buscar Archivo", command=buscar_configuracion_hilo)
buscar.grid(row=3, column=0, padx=20, pady=20)

app.mainloop()

