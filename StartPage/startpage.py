import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


import matplotlib
matplotlib.use("TkAgg")
from Classes.windows import Windows
from Sonnet.sonnet_fitting import Sonnet
from DC.DC import Compensation
from RF.RF import Workspace

LARGE_FONT = ("CMU Serif", 16)
NORM_FONT = ("CMU Serif", 10)
SMALL_FONT = ("CMU Serif", 6)

SIZE_Y=720
SIZE_X=1280

HOMEPAGEBG="#273746"
MENU_COLOR="#1B252F"

class StartPage(Windows):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent,bg=HOMEPAGEBG)
        self.controller = controller
        load = Image.open("tkinterstuff\logo.png")
        load.thumbnail((150,150))
        render = ImageTk.PhotoImage(load)
        img=ttk.Label(self,image=render,background=HOMEPAGEBG)
        img.image=render
        img.place(relx=0.5, rely=0.1, anchor=tk.N)
        button_style=ttk.Style()
        button_style.theme_use('alt')
        button_style.configure('TButton', background = HOMEPAGEBG, foreground = 'white', width = 40,borderwidth=1, focusthickness=3, focuscolor='none',font=LARGE_FONT)
        button_sonnet=ttk.Button(self,text="Sonnet",style='TButton',command=lambda:self.controller.show_frame(Sonnet))
        button_sonnet.place(relx=0.5, rely=0.4, anchor=tk.N)
        button = ttk.Button(self, text="RF Measurements",style='TButton',
                            command=lambda: self.controller.show_frame(Workspace))
        button.place(relx=0.5, rely=0.5, anchor="n")

        button_compensation=ttk.Button(self,text="DC Measurements",style='TButton',command=lambda: self.controller.show_frame(Compensation))
        button_compensation.place(relx=0.5, rely=0.6, anchor=tk.N)
