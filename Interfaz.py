import customtkinter
from src.simulacion.simulador import simulador
import xml.etree.ElementTree as ET
from customtkinter import filedialog
import threading

filepath = None
simulation = None
radio_actual = None
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
    configurador = customtkinter.CTk()
    configurador.title("configurar")
    configurador.geometry("1000x1000")

    #Abre el buscador de archivos
    open_filedialog = customtkinter.CTkButton(configurador, command=abrir_archivo, text= "Abrir archivo")
    open_filedialog.grid(row=2, column=1, padx=19, pady=8, sticky="w")

    #Muestra el archivo que se esta usando en tiempo real
    archivo_actual = customtkinter.CTkLabel(configurador, text= filepath)
    archivo_actual.grid(row=2, column=0, padx=20, pady=20)

    #Actualiza el valor del radio de la bola
    radio = customtkinter.CTkSlider(configurador, from_=0.1, to=2, command=lambda valor: llamar_actualizar_radio(valor, radio_actual))
    radio.grid(row=0, column=7, padx=20, pady=20)

    #Muestra el valor del radio de la bola en tiempo real
    radio_actual = customtkinter.CTkLabel(configurador, text=f"Radio actual: {simulation.obtener_radio()}")
    radio_actual.grid(row=0, column=1, padx=20, pady=10)
    
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

def llamar_actualizar_radio(nuevo_valor, radio_actual):
        #Actualiza el radio de la esfera
        simulation.actualizar_radio(nuevo_valor)
        
        #Actualiza el valor en la etiqueta
        radio_actual.configure(text=f"Radio actual: {round(nuevo_valor, 2)}")

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

