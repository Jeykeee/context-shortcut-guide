#Conecta deteccion con gui
import detector
import gui

def al_presionar_hotkey():
    #El puente la funcion callback
    #Detector llama cada vez que usuario presiona el atajo
    
    #Detecta
    nombre_app = detector.detectar_app_activa()

    #Para comprobar
    print(f"[ContextShortcut] App detectada: {nombre_app}")

    #Muestra la ventana
    gui.mostrar_ventana(nombre_app)

def iniciar_programa():
    print("=" * 45)
    print(" ContextShortcut Guide - Iniciado")
    print(" Presiona Ctrl+Alt+H en cualquier app")
    print(" para ver sus atajos de teclado")
    print("=" * 45)
    #Aqui bloqueamos el programa manteniendo en espera indefinidamente
    detector.iniciar_escucha(al_presionar_hotkey)

#Bloque para que arranque cuando lo ejecuto proteccion importante
if __name__=="__main__" :
    iniciar_programa()
