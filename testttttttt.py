import customtkinter as ctk

# Crear la ventana principal
root = ctk.CTk()

# Lista de opciones para el OptionMenu
opciones = ["Opción 1", "Opción 2", "Opción 3"]

# Crear el OptionMenu con la lista de opciones
opcion_menu = ctk.CTkOptionMenu(root, values=opciones)
opcion_menu.pack()

# Imprimir el valor inicial del OptionMenu
print(opcion_menu.get())  # Esto debería imprimir "Opción 1" al no haber interacción

# Iniciar el bucle principal
root.mainloop()