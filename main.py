import threading
import time
import tkinter as tk
from pynput import keyboard, mouse

from PIL import ImageGrab
import pyautogui
import pyperclip as clipboard


class WindowsPciker():
    # CONSTANTS
    # 130 50
    wp_width = 154
    wp_height = 52
    wp_offset_x = 15
    wp_offset_y = 15
    external_px = 5
    external_py = 5

    admn_width = 512
    admn_height = 487

    # instance variables of views
    pciekr = None  # float windows to pick color
    config = None  # float windows to config
    admin = None  # float windows to admin

    # threads
    wp_threads = []  # windows picker threads

    # Flag to thread
    flag_wp = False

    # thrd_wp_pos = None  # thread to move the position of picker

    # pciked color
    color_hex = None

    # constructor
    def __init__(self):
        pass

    # open admin thread
    def open_admin_tht(self):
        thr = threading.Thread(target=self.open_admin)
        thr.start()

    # open admin
    def open_admin(self):
        self.admin = tk.Tk()
        # self.admin.attributes('-topmost', True)
        # self.admin.overrideredirect(True)
        self.admin.geometry(f'{self.admn_width}x{self.admn_height}')

        self.admin.protocol("WM_DELETE_WINDOW", self.close_admin)

        self.admin.mainloop()

    # close admin
    def close_admin(self):
        if self.admin is not None:
            self.admin.destroy()

    # start picker thread
    def open_picker_thr(self):
        thrp = threading.Thread(target=self.open_picker)
        thrp.start()

    # start pciker
    def open_picker(self):
        self.pciekr = tk.Tk()
        self.pciekr.attributes('-topmost', True)
        self.pciekr.overrideredirect(True)
        self.pciekr.geometry(f'{self.wp_width}x{self.wp_height}')

        self.color_label = tk.Label(self.pciekr, width=6, height=3)
        self.color_label.pack(
            side=tk.LEFT,
            padx=self.external_px,
            pady=self.external_py
        )

        self.hex_label = tk.Label(
            self.pciekr,
            text="",
            width=10,
            height=3,
            font=("Arial", 12)
        )
        self.hex_label.pack(
            side=tk.RIGHT,
            padx=(0, self.external_px),
            pady=self.external_py
        )
        self.hex_label.configure(anchor="center")

        self.pciekr.protocol("WM_DELETE_WINDOW", self.close_picker)

        # Sync flags
        self.flag_wp = True

        # sync position
        self.move_wpciker(True)  # move the windows picker twhice

        # start thread
        _wp_pos = threading.Thread(target=self.move_wpciker)
        _wp_pos.start()
        _wp_color = threading.Thread(target=self.obtener_color_pixel)
        _wp_color.start()

        # add thread to list
        self.wp_threads.append(_wp_pos)
        self.wp_threads.append(_wp_color)

        def on_press(key):
            if key == keyboard.Key.esc:
                self.close_picker()

        def on_click(x, y, button, pressed):
            if pressed:
                copy_oc()

        def copy_oc():
            clipboard.copy(str(self.color_hex))
            self.close_picker()

        # listenesr
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        mouse_listener = mouse.Listener(on_click=on_click)
        mouse_listener.start()

        # mainloop
        self.pciekr.mainloop()

    # close picker
    def close_picker(self):
        # destroy pciker
        self.flag_wp = False

        for thrd in self.wp_threads:
            thrd.join()
        self.wp_threads = []
        if self.pciekr is not None:
            self.pciekr.destroy()
            self.pciekr = None

    # move the picker
    def move_wpciker(self, once=False):
        if self.pciekr is None:
            return
        while self.flag_wp:
            x, y = pyautogui.position()
            self.pciekr.geometry(f"+{x+self.wp_offset_x}+{y+self.wp_offset_y}")
            if once:
                break
            time.sleep(0.01)

    # get cursor position
    def obtener_color_pixel(self):
        global color_hex
        while self.flag_wp:
            x, y = pyautogui.position()
            imagen = ImageGrab.grab().load()
            r, g, b = imagen[int(x), int(y)]
            self.color_hex = f"#{r:02x}{g:02x}{b:02x}"
            self.color_label.configure(bg=self.color_hex)
            self.hex_label.configure(text=self.color_hex)
            # ventana.update()
            # print(f"Color del píxel en ({x}, {y}): R:{r}, G:{g}, B:{b}")
            time.sleep(0.01)


wp = WindowsPciker()
wp.open_admin_tht()
wp.open_picker_thr()
