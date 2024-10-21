import customtkinter
from src.simulacion.simulador import simulador


def pulsar_boton():
    print("Boton pulsado")

def cargar_configuracion():
    configurador = customtkinter.CTk()
    configurador.title("configurar")
    configurador.geometry("300x300")

    button3 = customtkinter.CTkButton(configurador, text="Cargar Configuracion", command=pulsar_boton)
    button3.grid(row=2, column=0, padx=20, pady=20)

    radio1 = customtkinter.CTkEntry(configurador, placeholder_text="Radio de la esfera 1")
    radio1.grid(row=0, column=0, padx=20, pady=20)

    radio_actual = customtkinter.CTkLabel(configurador, text = 'Radio actual = 2')
    radio1.grid(row=0, column=1, padx=20, pady=20)

    configurador.mainloop()

    

def simular():
    p = simulador("escenario//escena.xml")
    p.run()

app = customtkinter.CTk()
app.title("my app")
app.geometry("1000x800")

button1 = customtkinter.CTkButton(app, text="Cargar Configuracion", command=cargar_configuracion)
button1.grid(row=0, column=0, padx=20, pady=20)

button2 = customtkinter.CTkButton(app, text="Iniciar Simulacion", command=simular)
button2.grid(row=1, column=0, padx=20, pady=20)

app.mainloop()

