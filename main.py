import tkinter as tk
from pynput import keyboard, mouse
import pyautogui
from PIL import ImageGrab
import pyperclip as clipboard
import threading
import time

color_hex = ""
ventana = None

def seguir_mouse(evento):
    ventana.geometry(f"+{evento.x_root}+{evento.y_root}")

def cerrar_ventana():
    ventana.destroy()

def copy_oc():
    clipboard.copy(str(color_hex))
    ventana.destroy()

def on_press(key):
    if key == keyboard.Key.esc:
        cerrar_ventana()

def on_click(x, y, button, pressed):
    if pressed:
        copy_oc()

def obtener_color_pixel():
    global color_hex
    while True:
        x, y = pyautogui.position()
        imagen = ImageGrab.grab().load()
        r, g, b = imagen[x, y]
        color_hex = f"#{r:02x}{g:02x}{b:02x}"
        color_label.configure(bg=color_hex)
        hex_label.configure(text=color_hex)
        ventana.update()
        #print(f"Color del píxel en ({x}, {y}): R:{r}, G:{g}, B:{b}")
        time.sleep(0.001)

def actualizar_posicion():
    x, y = ventana.winfo_pointerxy()
    if 0 <= x <= pantalla_width and 0 <= y <= pantalla_height:
        ventana.geometry(f"+{x+x_offset}+{y+y_offset}")
    ventana.after(10, actualizar_posicion)

def sync_actualizar_posicion(cond=True):
    while True:
        x, y = ventana.winfo_pointerxy()
        if 0 <= x <= pantalla_width and 0 <= y <= pantalla_height:
            ventana.geometry(f"+{x+x_offset}+{y+y_offset}")

        time.sleep(0.001)
        if not cond:
            break
        #ventana.after(10, actualizar_posicion)



def iniciar():
    global ventana, color_label, hex_label, pantalla_width, pantalla_height, x_offset, y_offset

    ventana = tk.Tk()
    ventana.overrideredirect(True)
    ventana_width = 150
    ventana_height = 60
    x_offset = 15
    y_offset = 15
    external_px = 6
    external_py = 6
    ventana.geometry(f"{ventana_width}x{ventana_height}")

    pantalla_width = ventana.winfo_screenwidth()
    pantalla_height = ventana.winfo_screenheight()

    color_label = tk.Label(ventana, width=6, height=3)
    color_label.pack(side=tk.LEFT, padx=external_px, pady=external_py)

    hex_label = tk.Label(ventana, text="", width=10, height=3, font=("Arial", 12))
    hex_label.pack(side=tk.RIGHT, padx=(0, external_px), pady=external_py)
    hex_label.configure(anchor="center")

    # listenesr
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    # threads
    color_thread = threading.Thread(target=obtener_color_pixel)
    color_thread.daemon = True
    color_thread.start()

    position_thread = threading.Thread(target=sync_actualizar_posicion)
    position_thread.daemon = True
    position_thread.start()

    #actualizar_posicion()
    sync_actualizar_posicion(False)

    ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)
    ventana.mainloop()

iniciar()

