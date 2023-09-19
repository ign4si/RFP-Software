import tkinter as tk
from Sonnet.sonnet_fitting import Sonnet

# Crear una ventana de prueba
controller = tk.Tk()
controller.title("Prueba de SonnetFrame")
containter = tk.Frame(controller)

# Crear una instancia de SonnetFrame y agregarla a la ventana
sonnet_frame = Sonnet(containter,controller)
sonnet_frame.pack()

# Iniciar el bucle principal de tkinter
controller.mainloop()