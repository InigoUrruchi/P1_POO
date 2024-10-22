import customtkinter
from src.simulacion.simulador import simulador
import xml.etree.ElementTree as ET

def pulsar_boton():
    print("Boton pulsado")

def cargar_configuracion():
    configurador = customtkinter.CTk()
    configurador.title("configurar")
    configurador.geometry("1000x1000")

    radio1 = customtkinter.CTkEntry(configurador, placeholder_text="Radio de la bola 1", )
    radio1.grid(row=0, column=1, padx=20, pady=20)
    
    #Obtener el nuevo valor del radio de bola 1
    radio_actual = customtkinter.CTkLabel(configurador, text=f"Radio actual = {buscar_atributo('geom', 'ball1', 'size')}")
    radio_actual.grid(row=0, column=0, padx=20, pady=20)

    #Actualizar el valor del radio de la bola 1 
    button3 = customtkinter.CTkButton(configurador, text="Aceptar", command=lambda: actualizar_atributo('geom', 'ball1', 'size', radio1.get()))
    button3.grid(row=0, column=7, padx=20, pady=20)

    configurador.mainloop()

#Iniciar el simulador
def simular():
    inicializador = simulador("escenario//escena.xml")
    inicializador.run()

#Busca el valor del atributo del objeto que se quiera y lo devuelve como str
def buscar_atributo(objeto, nombre, atributo,):
    tree= ET.parse("escenario//escena.xml")
    root = tree.getroot()
    for elem in root.findall(f".//{objeto}"):
        if elem.get('name') == nombre:
            valor_atributo = elem.get(atributo)
            return str(valor_atributo)


#Actualiza en el xml el valor del atributo del objeto que se quiera 
def actualizar_atributo(objeto, nombre, atributo, valor_atributo):
    tree= ET.parse("escenario//escena.xml")
    root = tree.getroot()
    print(f"El nuebo valor del atributo es {valor_atributo}")
    for elem in root.findall(f".//{objeto}"):
        if elem.get('name') == nombre:
            elem.set(atributo, valor_atributo)
    tree.write("escenario//escena.xml")
    print(f"El nuevo valor de {atributo} es {valor_atributo}")


app = customtkinter.CTk()
app.title("my app")
app.geometry("1000x800")

button1 = customtkinter.CTkButton(app, text="Cargar Configuracion", command=cargar_configuracion)
button1.grid(row=0, column=0, padx=20, pady=20)

button2 = customtkinter.CTkButton(app, text="Iniciar Simulacion", command=simular)
button2.grid(row=1, column=0, padx=20, pady=20)

app.mainloop()

