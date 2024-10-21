import xml.etree.ElementTree as ET

def buscar_size_ball1():
    # Cargar el archivo XML
    tree = ET.parse("escenario/escena.xml")  # Asegúrate de que la ruta sea correcta
    root = tree.getroot()

    # Buscar el elemento geom con name='ball1'
    for geom in root.findall(".//geom"):  # Busca todos los elementos geom en el árbol
        if geom.get('name') == 'ball1':
            size = geom.get('size')  # Obtiene el atributo size
            print(f"El tamaño actual de 'ball1' es: {size}")
            return size

    print("No se encontró el objeto 'ball1'.")
    return None  # Devuelve None si no se encuentra

# Llamar a la función
buscar_size_ball1()