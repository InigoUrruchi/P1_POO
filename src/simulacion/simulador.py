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
object_name = 'ball'
object_name = 'ramp'
object_id = None
posiciones_iniciales = {}
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

        #Guardar las posiciones iniciales de las bolas
        mj.mj_step(self.model, self.data)
        self.guardar_posicion_inicial("ball1")
        self.guardar_posicion_inicial("ball2")
        
        # Configurar callbacks de mouse
        glfw.set_cursor_pos_callback(self.window, self.mouse_move)
        glfw.set_mouse_button_callback(self.window, self.mouse_button)
        glfw.set_scroll_callback(self.window, self.mouse_scroll)

        # Variables para el control de la cámara
        self.mouse_pressed_right = False
        self.prev_mouse_x = 0
        self.prev_mouse_y = 0
        self.zoom_factor = 1.0

    def mouse_scroll(self, window, xoffset, yoffset):
        #Acercar la camara si se hace scroll hacia adelante   
        if yoffset > 0 and self.cam.distance > 0.6:
            self.cam.distance -= 0.3
        #Acercar la camara si se hace scroll hacia atras
        elif yoffset < 0 and self.cam.distance < 20:
            self.cam.distance += 0.3 

    def mouse_move(self, window, xpos, ypos):
        global mouse_x, mouse_y

        # Calcular el desplazamiento en el movimiento del ratón
        dx = xpos - self.prev_mouse_x  # Diferencia en el eje X
        dy = ypos - self.prev_mouse_y  # Diferencia en el eje Y

        # Si el botón derecho está presionado, mover la cámara
        if self.mouse_pressed_right:
            # Ajustar azimuth (rotación horizontal) y elevation (rotación vertical)
            self.cam.azimuth += dx * 0.1 
            self.cam.elevation += dy * 0.1

        # Actualizar las posiciones anteriores del ratón
        self.prev_mouse_x = xpos
        self.prev_mouse_y = ypos

    def mouse_button(self, window, button, action, mods):
        global button_left, button_right
        #Definir las acciones al pusar los clicks
        if button == glfw.MOUSE_BUTTON_LEFT:
            button_left = (action == glfw.PRESS)
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            self.mouse_pressed_right = (action == glfw.PRESS)
    
    def run(self):
        while not glfw.window_should_close(self.window):
            mj.mj_step(self.model, self.data)
            mj.mj_forward(self.model, self.data)
            
            # Actualizar la escena y renderizar
            mj.mjv_updateScene(self.model, self.data, self.opt, None, self.cam, mj.mjtCatBit.mjCAT_ALL.value, self.scene)
            mj.mjr_render(mj.MjrRect(0, 0, 1200, 900), self.scene, self.context)
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()
    
    #Cambia la posicion de las bolas a la posicion inicial
    def reiniciar_bolas(self):
        global posiciones_iniciales
        nombres_objetos = list(posiciones_iniciales.keys())
        for n in range(len (posiciones_iniciales)):
            object_name = nombres_objetos[n]
            object_id = self.obtener_id_objeto(object_name)
            
            #Se obtiene el id del body atraves del id del geom
            body_id = self.model.geom_bodyid[object_id]
            posicion_inicial = posiciones_iniciales[object_name]

            #Calcula en que posicion de la lista va y actualiza el valor
            qpos_index_ball = self.model.jnt_qposadr[self.model.body_jntadr[body_id]]
            self.data.qpos[qpos_index_ball:qpos_index_ball+7] = posicion_inicial

            # Reinicia todas las velocidades del body
            vel_index_start = self.model.body_dofadr[body_id]
            vel_index_end = vel_index_start + self.model.body_dofnum[body_id]
            self.data.qvel[vel_index_start:vel_index_end] = 0

            # Reinicia aceleracion
            self.data.qacc[vel_index_start:vel_index_end] = 0

            # Reinicia las fuerzas residuales
            if hasattr(self.data, 'xfrc_applied'):
                self.data.xfrc_applied[body_id] = 0

        #Actualiza la simulacion una vez hechos los cambios
        mj.mj_forward(self.model, self.data)
    
    #Guarda la posicion inicial de las bolas
    def guardar_posicion_inicial(self, object_name):
        global posiciones_iniciales
        object_id = self.obtener_id_objeto(object_name)
        
        #Obtener la posicion inicial de la bola
        posicion_inicial = self.model.geom_pos[object_id]
        
        #Añadir el cuaternion a la posicion
        posicion_inicial = np.concatenate((posicion_inicial, [1, 0, 0, 0]))
        posiciones_iniciales[object_name] = posicion_inicial
        print(posiciones_iniciales)
        return posiciones_iniciales

    #obtiene el radio de la bola
    def obtener_radio(self,object_name):
        object_id = self.obtener_id_objeto(object_name)
        valor_radio = self.model.geom_size[object_id][0]
        return valor_radio
    
    #Actualiza el radio de la bola
    def actualizar_radio(self, nuevo_valor, object_name):
        object_id = self.obtener_id_objeto(object_name)
        self.model.geom_size[object_id][0] = nuevo_valor
        return nuevo_valor
    
    # Obtener el ID del objeto
    def obtener_id_objeto(self, object_name):
        object_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, object_name)
        return object_id

    #Obtener el angulo de rotacion mediante el cuaternion
    def calcular_angulo(self, valor_inclinacion):
        
        #Obtener la parte real del quaternion (w)
        w = valor_inclinacion[0]
        
        #Calcular el angulo en radianes
        angulo_rad = 2 * np.arccos(w)
        
        #Calcular el angulo en grados
        angulo_grados = np.degrees(angulo_rad)
        return angulo_grados
    
    #Calcula el cuaternion que corresponde al angulo
    def calcular_cuaternion(self, angulo_grados):
        
        #Calcula el angulo en radianes
        angulo_radianes = np.radians(angulo_grados)
        
        #Calcula la parte real del cuaternion
        w = np.cos(angulo_radianes/2)
        
        #Calcula las componentes del cuaternion (las componentes x,z son 0 porque la rotacion de la rampa es sobre el eje y)
        x = 0
        y = np.sin(angulo_radianes/2)
        z = 0
        
        #Crea el cuaternion
        cuaternion = (w,x,y,z)
        return cuaternion

    #Obtiene la inclinacion de la rampa
    def obtener_inclinacion(self,object_name):
        object_id = self.obtener_id_objeto(object_name)
        
        #Devuelve un quaternion con la informacion del angulo de la rampa
        valor_inclinacion = self.model.geom_quat[object_id]
        
        #Obtiene el angulo a partir de quaternion
        angulo_inclinacion = self.calcular_angulo(valor_inclinacion)
        return angulo_inclinacion
    
    #Actualiza la inclinacion de la rampa
    def actualizar_inclinacion(self, nuevo_valor, object_name):
        object_id = self.obtener_id_objeto(object_name)
        
        #Calcula el quaternion del angulo que se quiere añadir
        inclinacion =  self.calcular_cuaternion(nuevo_valor)
        self.model.geom_quat[object_id] = inclinacion
        return nuevo_valor