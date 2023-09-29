from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


import matplotlib
import expdatafunc as edf
matplotlib.use("TkAgg")
import numpy as np
import pandas as pd
from resonator_tools import circuit

matplotlib.rcParams['text.usetex'] = True   #Change to false if u dont have latex <3
from StartPage.startpage import StartPage

LARGE_FONT = ("CMU Serif", 16)
NORM_FONT = ("CMU Serif", 10)
SMALL_FONT = ("CMU Serif", 6)

SIZE_Y=720
SIZE_X=1280

HOMEPAGEBG="#273746"
MENU_COLOR="#1B252F"


class MainContainer(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="tkinterstuff\logo.ico")
        tk.Tk.wm_title(self, "RFP")
        tk.Tk.wm_geometry(self, self.geometry())
        self.state('zoomed')


        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)    
        style = ttk.Style(self)
        style.configure('TLabel', background='black', foreground='white')
        style.configure('TFrame', background='black')
        self.frames = {}

        for F in ([StartPage]):

            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Creating the menu
        menubar = tk.Menu(self.container)  # toolbar

        # creating the file section

        filemenu = tk.Menu(menubar, tearoff=0,bg=MENU_COLOR,fg="white")

        filemenu.add_command(label="Load File", command=lambda: self.frames[StartPage].select_folder(self))
        filemenu.add_command(label="Exit", command=quit)
        filemenu.add_separator()
        filemenu.add_command(label="Pop Up", command=lambda: tk.messagebox.showinfo(title="Pop up",message="This is a pop up!"))
        # adding the file section to the menu
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu=tk.Menu(menubar,tearoff=0,bg=MENU_COLOR,fg="white")

        # helpmenu.add_command(label="How to read Sonnet files",command=lambda: self.read_pdf("tkinterstuff\SonnetFiles.pdf"))
        # helpmenu.add_command(label= "How Sonnet data is fitted",command=lambda: self.read_pdf("tkinterstuff\SonnetFitted.pdf"))
        # helpmenu.add_separator()
        # helpmenu.add_command(label="How to read real data files",command=lambda: self.read_pdf("tkinterstuff\RealDataFiles.pdf"))
        # helpmenu.add_command(label="How real data is fitted",command=lambda: self.read_pdf("tkinterstuff\RealDataFitted.pdf"))
        # helpmenu.add_separator()
        helpmenu.add_command(label="Contact",command=lambda: tk.messagebox.showinfo(title="Contact",message="Beta 1.0.5\nMSc. I. Lobato \nlobato31415@gmail.com"))
        
        menubar.add_cascade(label="Help",menu=helpmenu)
        # telling the program: hey, this is the menu
        tk.Tk.config(self, menu=menubar)
        
        
        # show the start page
        self.show_frame(StartPage)
    def geometry(self):
        global SIZE_X
        global SIZE_Y

        SIZE_X=self.winfo_screenwidth()
        SIZE_Y=self.winfo_screenheight()
        return "%dx%d" % (SIZE_X, SIZE_Y)
    def show_frame(self, cont):
        if self.frames.get(cont)==None:
            frame=cont(self.container,self)
            self.frames[cont]=frame
            frame.grid(row=0, column=0, sticky="nsew")
        frame=self.frames[cont]
        frame.tkraise()
        # if cont==Workspace:
            # frame.title.text=folder
    def destroy_frames(self):
        for frame in self.frames.values():
            frame.grid_remove()
    def back_to_start(self):
        self.destroy_frames()
        self.destroy()
        app=MainContainer()
        app.mainloop()
app = MainContainer()
app.mainloop()
