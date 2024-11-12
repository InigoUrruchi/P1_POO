    # El siguiente Colab proporciona una explicación detallada sobre el funcionamiento de cada función, método y variable dentro del código de ejemplo de MuJoCo. A lo largo del notebook, se analizan en profundidad los elementos clave de la simulación, como la inicialización del entorno, la interacción con el ratón y el teclado, y el manejo de objetos en la escena simulada. Cada parte del código se desglosa para que puedas entender su propósito y cómo se utiliza en el contexto de las simulaciones físicas en tiempo real.

    # Explicación detallada:
    # 1. Funciones y métodos: Se explica cómo las funciones de inicialización, como `init_mujoco()`, configuran el entorno gráfico y cargan el modelo de MuJoCo. Se detallan los métodos que controlan la simulación, como `mj.mj_step()` y `mj.mj_forward()`, que avanzan la simulación en pasos discretos.
    
    # 2. Eventos de entrada: Se analizan las funciones de manejo del ratón (`mouse_move()` y `mouse_button()`), que permiten que el usuario interactúe con los objetos en la simulación, y cómo estos eventos se integran en el bucle principal del programa.

    # 3. Renderizado y visualización: Se examinan los métodos que actualizan y renderizan la escena, como `mj.mjr_render()`, mostrando cómo se dibuja el entorno físico en la ventana.

    # 4. Variables globales: Se explora el uso de variables globales, como las posiciones del ratón y los identificadores de objetos, para almacenar el estado de la simulación y permitir la interacción en tiempo real.

    # Puedes acceder al Colab en este enlace: https://colab.research.google.com/drive/1gm8F1l158Ul3IdeNbyrad75CIxx1pyW_?usp=sharing. 


import mujoco as mj
from mujoco.glfw import glfw
import numpy as np

# Variables globales para el estado del mouse y el objeto
mouse_x = 0
mouse_y = 0
button_left = False
button_right = False
ball_name = 'ball'  # Nombre del objeto a mover
ramp_name = 'ramp'
object_id = None



class simulador:

    # Inicialización de MuJoCo
    def __init__(self, path):
        #global model, data, scene, cam, window, context, opt, object_id
        #self.model = None
        # Inicialización de GLFW
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        # Crear ventana
        self.window = glfw.create_window(1200, 900, "MuJoCo Viewer", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        
        # Hacer que el contexto OpenGL sea actual
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  # Habilitar V-Sync
        
        # MuJoCo model y data
        self.model = mj.MjModel.from_xml_path(path)
        self.data = mj.MjData(self.model)
        self.cam = mj.MjvCamera()
        self.opt = mj.MjvOption()
        self.scene = mj.MjvScene(self.model, maxgeom=10000)
        self.context = mj.MjrContext(self.model, mj.mjtFontScale.mjFONTSCALE_150.value)

        mj.mjv_defaultCamera(self.cam)
        mj.mjv_defaultOption(self.opt)

        self.cam.lookat = [0,0,0.5]

        # Configurar callbacks de mouse
        glfw.set_cursor_pos_callback(self.window, self.mouse_move)
        glfw.set_mouse_button_callback(self.window, self.mouse_button)
        glfw.set_scroll_callback(self.window, self.mouse_scroll)

        # Obtener el ID del objeto para actualizar su posición
        self.ramp_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, ramp_name)
        self.ball_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, ball_name)

        # Variables para el control de la cámara
        self.mouse_pressed_right = False
        self.prev_mouse_x = 0
        self.prev_mouse_y = 0
        self.zoom_factor = 1.0 #Distancia de la camara "zoom"

    def keyboard(self, window, key, scancode, act, mods):
        # Resetea la simulación con la tecla BACKSPACE
        if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
            mj.mj_resetData(self.model, self.data)
            mj.mj_forward(self.model, self.data)
            for i in range(len(self.initial_joint_angles)):
                self.data.qpos[i] = self.initial_joint_angles[i]
            mj.mj_forward(self.model, self.data)
        
        # Activa la interacción con la tecla A o a
        if act == glfw.PRESS and (key == glfw.KEY_A or key == glfw.KEY_A):
            self.interact_with_object()

    def mouse_scroll(self, window, xoffset, yoffset):
        #Esta función es llamada cuando se usa la ruleta del ratón        
        if yoffset > 0 and self.cam.distance > 0.6:  # Hacia arriba (acercar)
            self.cam.distance -= 0.3  # Acercar la cámara
        elif yoffset < 0 and self.cam.distance < 7.5:  # Hacia abajo (alejar)
            self.cam.distance += 0.3 

    def mouse_move(self, window, xpos, ypos):
        global mouse_x, mouse_y

        # Calcular el desplazamiento en el movimiento del ratón
        dx = xpos - self.prev_mouse_x  # Diferencia en el eje X
        dy = ypos - self.prev_mouse_y  # Diferencia en el eje Y

        # Si el botón derecho está presionado, mover la cámara
        if self.mouse_pressed_right:
            # Ajustar azimuth (rotación horizontal) y elevation (rotación vertical)
            self.cam.azimuth += dx * 0.1  # Escala de rotación horizontal
            self.cam.elevation += dy * 0.1  # Escala de rotación vertical

        # Actualizar las posiciones anteriores del ratón
        self.prev_mouse_x = xpos
        self.prev_mouse_y = ypos

    def mouse_button(self, window, button, action, mods):
        global button_left, button_right
        if button == glfw.MOUSE_BUTTON_LEFT:
            button_left = (action == glfw.PRESS)
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            self.mouse_pressed_right = (action == glfw.PRESS)

    def update_object_position(self):
        if ball_id is not None:
            # Convertir las coordenadas del mouse a una posición en el mundo
            # Aquí se asume una conversión simple para demostrar el concepto.
            # En un caso real, deberías aplicar una transformación más precisa.
            scale_factor = 0.001  # Factor de escala para convertir el movimiento del mouse a unidades del mundo
            new_position = np.array([
                (mouse_x - 600) * scale_factor,  # Ajustar según el centro de la ventana
                (450 - mouse_y) * scale_factor,  # Ajustar según el centro de la ventana
                0.2  # Mantener la posición en Z constante, o ajustarla según sea necesario
            ])
            
            self.model.geom_pos[ball_id] = new_position

    def run(self):
        while not glfw.window_should_close(self.window):
            mj.mj_step(self.model, self.data)
            mj.mj_forward(self.model, self.data)
        
            # Actualizar la posición del objeto si el botón izquierdo está presionado
            if button_left:
                self.update_object_position()
            
            # Actualizar la escena y renderizar
            mj.mjv_updateScene(self.model, self.data, self.opt, None, self.cam, mj.mjtCatBit.mjCAT_ALL.value, self.scene)
            mj.mjr_render(mj.MjrRect(0, 0, 1200, 900), self.scene, self.context)
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()
    

    #obtiene el radio de la bola
    def obtener_radio(self,id):
        valor_radio = self.model.geom_size[id][0]
        print(f"radio = {valor_radio}")
        print("obtener_radio ejecutada")
        return valor_radio
    
    #Actualiza el radio de la bola
    def actualizar_radio(self, nuevo_valor, id):
        self.model.geom_size[id][0] = nuevo_valor
        print("actualizar_radio ejecutada")
        return nuevo_valor
        
    '''def obtener_id(self, object_name):
        self.object_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, object_name)
        print(f"el id de: {object_name} es : {self.object_id}")'''

    #Obtiene la inclinacion de la rampa
    '''def obtener_inclinacion(self,id):
        valor_inclinacion = self.model.geom_euler[id][1]
        print(f"inclinacion = {valor_inclinacion}")
        print("obtener_inclinacion ejecutada")
        return valor_inclinacion
    
    #Actualiza la inclinacion de la rampa
    def actualizar_inclinacion(self, nuevo_valor, id):
        self.model.geom_euler[id][1] = nuevo_valor
        print("actualizar_inclinacion ejecutada")
        return nuevo_valor'''
        
'''def main():
    simulation = simulador("escenario//escena.xml")
    simulation.run()
if __name__ == "__main__":
    main()'''