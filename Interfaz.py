import customtkinter
from src.simulacion.simulador import simulador
import xml.etree.ElementTree as ET
from customtkinter import filedialog

filepath = None
simulation = None

def pulsar_boton():
    print("Boton pulsado")

def buscar_configuracion():
    buscador = customtkinter.CTk()
    buscador.title("configurar")
    buscador.geometry("1000x1000")

    open_filedialog = customtkinter.CTkButton(buscador, command=abrir_archivo, text= "Abrir archivo")
    open_filedialog.grid(row=2, column=0, padx=19, pady=8, sticky="w")
    buscador.mainloop()

def cargar_configuracion():
    global simulation
    configurador = customtkinter.CTk()
    configurador.title("configurar")
    configurador.geometry("1000x1000")

    open_filedialog = customtkinter.CTkButton(configurador, command=abrir_archivo, text= "Abrir archivo")
    open_filedialog.grid(row=2, column=7, padx=19, pady=8, sticky="w")

    archivo_actual = customtkinter.CTkLabel(configurador, text= filepath)
    archivo_actual.grid(row=2, column=0, padx=20, pady=20)

    radio = customtkinter.CTkEntry(configurador, placeholder_text="Radio de la bola", )
    radio.grid(row=0, column=1, padx=20, pady=20)
    
    #Muestra el valor del radio de la bola
    radio_actual = customtkinter.CTkLabel(configurador, text=simulation.obtener_radio())
    radio_actual.grid(row=0, column=0, padx=20, pady=20)

    #Actualizar el valor del radio de la bola 
    button3 = customtkinter.CTkButton(configurador, text="Aceptar", command =lambda: simulation.actualizar_radio(radio.get()))
    button3.grid(row=0, column=7, padx=20, pady=20)


    configurador.mainloop()

#Iniciar el simulador
def simular():
    global filepath
    global simulation
    if filepath is not None:
        simulation = simulador(filepath)
        simulation.run()
    else:
        print("El archivo no existe")
        
#Selecciona el archivo XML y lo abre
def abrir_archivo():
    global filepath
    global simulation
    filepath = filedialog.askopenfilename(title="Abrir archivo configuración simulador", initialdir="./POO/Practica 1", filetypes=[("XML", "*.xml"),("Archivos .txt","*.txt")])
    open(filepath, 'r')
    print ("la ruta del archivo es:",filepath,)
    simulation = simulador(filepath)
    return filepath, simulation

'''def actualizar_radio(simulador, nuevo_valor, radio_actual):
        #Actualiza el radio de la esfera
        simulador.model.geom_size[ball] = nuevo_valor

        #Actualiza el valor de la esfera en el texto de la etiqueta
        radio_actual.configure(text=f"Radio actual = {nuevo_valor}")'''

app = customtkinter.CTk()
app.title("my app")
app.geometry("1000x800")

button1 = customtkinter.CTkButton(app, text="Cargar Configuracion", command=cargar_configuracion)
button1.grid(row=0, column=0, padx=20, pady=20)

button2 = customtkinter.CTkButton(app, text="Iniciar Simulacion", command=simular)
button2.grid(row=1, column=0, padx=20, pady=20)

buscar = customtkinter.CTkButton(app, text="Buscar configuracion", command=buscar_configuracion)
buscar.grid(row=3, column=0, padx=20, pady=20)

app.mainloop()

