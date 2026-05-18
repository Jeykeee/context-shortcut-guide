# ContextShortcut Guide

Programa de escritorio para Windows que detecta la aplicación activa
y muestra una ventana flotante con sus atajos de teclado al presionar `Ctrl + Alt + H`.

## ¿Por qué existe este proyecto?

Cada aplicación tiene decenas de atajos que aceleran el trabajo pero es imposible
recordarlos todos. En vez de buscar en Google cada vez, este programa los muestra
en contexto, en el momento justo, sin interrumpir el flujo de trabajo.

## Aplicaciones soportadas

| Aplicación | Categorías de atajos |
|---|---|
| Brave Browser | Pestañas, navegación, ventanas, herramientas |
| Visual Studio Code | Edición, terminal, paneles, ventanas |
| Explorador de Archivos | Navegación, gestión de archivos, visualización |
| Windows (global) | Sistema, ventanas, escritorios virtuales, capturas |

## Controles

| Acción | Cómo |
|---|---|
| Abrir ventana de atajos | `Ctrl + Alt + H` desde cualquier app |
| Cerrar ventana | `Escape` o botón `✕` |
| Scroll | Mouse, touchpad o teclas ↑ ↓ |
| Scroll rápido | `Re Pág` y `Av Pág` |
| Cerrar el programa | `Ctrl + C` en la terminal |

## Estructura del proyecto
context-shortcut-guide/
├── src/
│   ├── main.py          # Punto de entrada — conecta detección con GUI
│   ├── detector.py      # Detecta ventana activa y escucha el hotkey
│   └── gui.py           # Ventana flotante con tabla de atajos
├── data/
│   ├── brave.json       # Atajos de Brave Browser
│   ├── vscode.json      # Atajos de Visual Studio Code
│   ├── explorer.json    # Atajos del Explorador de Archivos
│   └── windows.json     # Atajos globales del sistema Windows
├── tests/               # Pruebas unitarias
├── requerimientos.txt   # Dependencias del proyecto
└── README.md            # Este archivo

## Instalación y uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/Jeykeee/context-shortcut-guide.git
cd context-shortcut-guide
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requerimientos.txt
```

### 3. Ejecutar el programa
```bash
python src/main.py
```

Presioná `Ctrl + Alt + H` con cualquier aplicación en foco.

## Tecnologías usadas

- **Python 3.11+**
- **pywin32** — detección de ventana activa via Win32 API
- **keyboard** — captura del hotkey global
- **psutil** — lectura de procesos del sistema
- **tkinter** — interfaz gráfica incluida en Python

## Sprints de desarrollo

- [x] Sprint 1 — Estructura del proyecto y configuración
- [x] Sprint 2 — Detección de ventana activa, hotkey y GUI flotante
- [ ] Sprint 3 — Mejoras de UX, autoarranque y bandeja del sistema

## Autor

Jeyke — [@Jeykeee](https://github.com/Jeykeee)