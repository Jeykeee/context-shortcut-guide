#Recibe el nombre de una app y muestra la ventana flotante con sus atajos
import tkinter as tk #Para interfaces graficas
import json #Para leer archivos json
import os #para construir rutas de archivos

#Constantes del diseño
COLOR_FONDO          = "#1e1e2e"  # fondo oscuro de la ventana principal
COLOR_CATEGORIA      = "#313244"  # fondo de cada bloque de categoría
COLOR_TITULO_VENTANA = "#cdd6f4"  # color del título principal
COLOR_TITULO_CAT     = "#89b4fa"  # color del nombre de cada categoría
COLOR_TECLAS         = "#a6e3a1"  # color del texto de las teclas (verde)
COLOR_DESCRIPCION    = "#cdd6f4"  # color del texto de la descripción
FUENTE_TITULO        = ("Segoe UI", 14, "bold")  # fuente del título principal
FUENTE_CATEGORIA     = ("Segoe UI", 10, "bold")  # fuente del nombre categoría
FUENTE_ATAJO         = ("Segoe UI", 9)           # fuente de cada atajo

#Para cargar los datos

def cargar_datos_app(nombre_app):
    #Recibe el nombre de la app construye la ruta al archivo 
    #Lo abre y devuelve como diccionario de python 
    #Al devolver none si no existe se evita el crasheo
    #os.path.dirname(__file__) devuelve carpeta donde esta gui.py que es src/
    #Subimos un nivel y entramos a data/.
    
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_json = os.path.join(ruta_base,"..","data",f"{nombre_app}.json")
    
    #hacemos la verificacion
    if not os.path.exists(ruta_json):
        return None
    
    #Abrimos en modo lectura el archivo encoding utf-8
    #para que funcionen bien los caracteres especiales
    #con with cerramos el archivo al terminar automaticamente
    with open(ruta_json,"r",encoding="utf-8") as archivo:
        datos= json.load(archivo)

    return datos

#Construccion y despliegue ventana
def mostrar_ventana(nombre_app):
    #Recibe el nombre de la app carga los datos y construye la ventana flotante
    #Se llama desde el main cada que usuario utiliza el hotkey

    datos = cargar_datos_app(nombre_app) #Se cargan los datos del JSON
    #Si no encuentra muestra los de windows
    if datos is None:
        datos = cargar_datos_app("windows")
    #Si  no existe windows.json algo malo paso y salimos
    if datos is None:
        return
    
    #Crear ventana
    ventana = tk.Tk() #Tk() crea la ventana raiz
    ventana.title(f"ContextShortcut - {datos['aplicacion']}") #Titulo que aparece en la barra
    ventana.configure(bg=COLOR_FONDO) #Color fondo ventana principal
    ventana.overrideredirect(True) #overrideredirect(True) elimina barra de titulo y bordes del SO asi se ve como flotante
    ventana.attributes("-topmost",True) #mantiene la ventana siempre encima de las demas aunque hagamos clic en otram parte

    #Centrar ventana
    #Calculamos tamaño de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    #El tamaño que queremos para la ventana
    ancho_ventana = 600
    alto_ventana = 500

    #Calculamos la posicion x e y para que quede centrada
    #Formula :(tam_pantalla - tam_ventana) / 2
    posicion_x = (ancho_pantalla - ancho_ventana) // 2
    posicion_y = (ancho_pantalla - ancho_ventana) // 2

    #geometry definde tam y pos en formato ancho x alto + x + y
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

    #Titulo principal de la ventana
    titulo = tk.Label(
        ventana, #pertenece a la ventana principal
        text=datos["aplicacion"], #texto del titulo - nombre de la app
        font=FUENTE_TITULO,
        bg=COLOR_FONDO,
        fg=COLOR_TITULO_VENTANA,
        pady=12 #espacio vertical interno
    )
    titulo.pack() #pack coloca el widget en la venta de arriba hacia abajo

    #Scroll
    #Con canvas con scrollbar para si hay muchas se pueda hacer scroll sin que se corten

    #El canvas es lienzo donde podemos dibujar y poner widgets
    canvas =tk.Canvas(ventana, bg=COLOR_FONDO, highlightthickness=0)
    
    #Se conecta la scrollbar al canvas
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y") #Scrollbar va a la derecha
    canvas.pack(side="left", fill="both", expand=True) #El canvas llena el resto

    #Frame interior que vive dentro del canvas - aca va el contenido
    frame_contenido = tk.Frame(canvas, bg=COLOR_FONDO)

    #create_window pone frame_contendio dentro del canvas
    #anchor="nw" significa que se ancla desde esq sup izq
    canvas.create_window((0,0), window=frame_contenido, anchor="nw")

    #Construir seccion por categoria
    for categoria in datos["categorias"]:
        #Frame contenedor de esta categoria
        frame_categoria = tk.Frame(
            frame_contenido,
            bg=COLOR_CATEGORIA,
            padx=10, #espacio horizontal interno
            pady=8, #espacio vertical interno
        )
        #fill="x" hace que el frame ocupe todo el ancho disponible
        # padx y pady aca son espacio externo - separacion entre categorias.
        frame_categoria.pack(fill="x", padx=10, pady=5)

        #Titulo de la categoria
        tk.Label(
            frame_categoria,
            text=categoria["nombre"],
            font=FUENTE_CATEGORIA,
            bg=COLOR_CATEGORIA,
            fg=COLOR_TITULO_CAT,
            anchor="w" #alinea texto a izquierda (west)
        ).pack(fill="x")

        #Linea separadora entre titulo y los atajos
        tk.Frame(
            frame_categoria,
            bg=COLOR_TITULO_CAT,
            height=1 #1 pixel de alto - linea fina
        ).pack(fill="x", pady=(2,6))

        #Construir una fila por cada atajo dentro de esa categoria
        for atajo in categoria["atajos"]:
            
            #Frame de una sola fila - agrupa teclas y descripcion
            fila = tk.Frame(frame_categoria, bg=COLOR_CATEGORIA)
            fila.pack(fill="x",pady=1)

            #Columna izquierda - las teclas
            tk.Label(
                fila,
                text=atajo["teclado"],
                font=FUENTE_ATAJO,
                bg=COLOR_CATEGORIA,
                fg=COLOR_TECLAS,
                #ancho fijo para que descripcion siempre empiece misma posicion
                width=22,
                anchor="w" 
            ).pack(side="left")

            #Columna derecha-la descripcion
            tk.Label(
                fila,
                text=atajo["descripcion"],
                font=FUENTE_ATAJO,
                bg=COLOR_CATEGORIA,
                fg=COLOR_DESCRIPCION,
                anchor="w"
            ).pack(side="left")

    #Actualizar scroll y configurar su cierre
    #Despues de todo el contenido decimos al canvas cuanto espacio ocupa 
    #Asi la scrollbar sabe hasta donde
    frame_contenido.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    #Cerrar la ventana al presionar Esc - sin salir del programa principal
    #bind conecta un evento =tecla Esc con una funcion = cerrar ventana
    ventana.bind("<Escape>", lambda evento: ventana.destroy())

    #mainloop() inicia el bucle de eventos de tkinter
    #El programa se queda esperando acciones del usuario hasta que se cierre la ventana
    ventana.mainloop()