#Detecta la app activa y escucha el hotkey
import win32gui #Para interactuar con ventanas
import win32process #Para info del proceso
import psutil #Para leer informacion de procesos
import keyboard #Para escuchar combinaciones de teclas globales
#Clave --> Valor
APLICACIONES_RECONOCIDAS = {
    "brave.exe": "brave",
    "code.exe": "vscode",
    "explorer.exe": "explorer",
}
APP_POR_DEFECTO= "windows"   #Devuelve por defecto atajos de windows
#El atajo elegido
HOTKEY="ctrl+alt+h"
"""
DETECCION
"""
def obtener_ventana_activa():
    #Para obtener la ventana activa devolviendo el handle
    handle= win32gui.GetForegroundWindow()#Pregunta al sistema la ventana activa
    return handle #Devuelve el numero entero

def obtener_pid(handle):
    #Dado el handle devolver el PID
    #Devuelve dos valores a la vez el id del hilo que creo la ventana y el id del proceso dueño de la ventana
    #handle 0 significa que no hay ventana activa
    if not handle:
        return None
    _, pid=win32process.GetWindowThreadProcessId(handle) #Con el _, descartamos el primer valor solo importa el PID
    return pid

def obtener_nombre_ejecutable(pid):
    #Verficamos que PID sea valido
    if not pid:
        return None
    try:
        #El try/except atrapa el caso en que el proceso desaparecio entre que obtuvimos pid y esa linea
        proceso = psutil.Process(pid)
        nombre = proceso.name().lower()
        return nombre
    except psutil.NoSuchProcess:
        return None

def traducir_a_nombre_app(nombre_ejecutable):
    #Traduce el nombre del ejecutable al que usamos 
    #Si no esta en el diccionario devuelve la app por defecto
    #con get busca la clave en diccionario si la encuentra devuelve valor sino la app por defecto
    #sin get el programa crashea con apps desconocidas
    return APLICACIONES_RECONOCIDAS.get(nombre_ejecutable, APP_POR_DEFECTO)

def detectar_app_activa():
    #Combina los pasos
    handle = obtener_ventana_activa() #El handle de la ventana activa
    pid = obtener_pid(handle) #PID del dueño de la ventana
    nombre_ejecutable = obtener_nombre_ejecutable(pid) #nombre del ejecutable
    # Debug temporal — muestra el ejecutable real detectado
    print(f"[Debug] Ejecutable detectado: {nombre_ejecutable}")
    #Si cualquier paso devolvio none usamos fallback
    if not nombre_ejecutable:
        return APP_POR_DEFECTO
    nombre_app = traducir_a_nombre_app(nombre_ejecutable) #traduce a la del programa
    return nombre_app

"""
HOTKEY
"""

def iniciar_escucha(funcion_callback):
    #Registra el hotkey y empieza a escuchar
    #con add_hotkey registra la combinacion en el SO
    #Windows monitorea y cuando detecta llama a la funcion_callback
    keyboard.add_hotkey(HOTKEY, funcion_callback)
    print(f"[ContextShortcut] Escuchando {HOTKEY} - presionalo en cualquier app")
    #mantiene el programa vivo indefinidamente esperando eventos del teclado termina despues del hotkey
    keyboard.wait()