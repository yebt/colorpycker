import tkinter as tk
from pynput import keyboard
import pyautogui
from PIL import ImageGrab

def seguir_mouse(evento):
    ventana.geometry(f"+{evento.x_root}+{evento.y_root}")

def cerrar_ventana():
    ventana.destroy()

# Crear la ventana flotante
ventana = tk.Tk()
ventana.overrideredirect(True)  # Elimina las barras de título y bordes de la ventana
ventana.attributes("-alpha", 0.7)  # Establece la opacidad de la ventana

# Configurar el tamaño de la ventana
ventana_width = 170
ventana_height = 60
x_offset = 15
y_offset = 15
ventana.geometry(f"{ventana_width}x{ventana_height}")

# Obtener el tamaño de la pantalla
pantalla_width = ventana.winfo_screenwidth()
pantalla_height = ventana.winfo_screenheight()

# Hacer que la ventana flotante siga el mouse
def actualizar_posicion():
    x, y = ventana.winfo_pointerxy()
    if 0 <= x <= pantalla_width and 0 <= y <= pantalla_height:
        ventana.geometry(f"+{x+x_offset}+{y+y_offset}")
    ventana.after(10, actualizar_posicion)

# Configurar el evento para cerrar la ventana con la tecla Esc
def on_press(key):
    if key == keyboard.Key.esc:
        cerrar_ventana()

def obtener_color_pixel():
    while True:
        x, y = pyautogui.position()
        imagen = ImageGrab.grab().load()
        r, g, b = imagen[x, y]
        color_hex = f"#{r:02x}{g:02x}{b:02x}"
        ventana.configure(bg=color_hex)
        ventana.update()
        #print(f"Color del píxel en ({x}, {y}): R:{r}, G:{g}, B:{b}")

listener = keyboard.Listener(on_press=on_press)
listener.start()

# Iniciar la función para obtener el color del píxel
import threading
color_thread = threading.Thread(target=obtener_color_pixel)
color_thread.daemon = True
color_thread.start()

actualizar_posicion()

# Iniciar el bucle de eventos
ventana.mainloop()

