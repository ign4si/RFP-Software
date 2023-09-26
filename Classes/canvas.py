import tkinter as tk
from tkinter import ttk
MENU_COLOR="#1B252F"


class ControlCanvas(tk.Canvas):
    def __init__(self,root):
        tk.Canvas.__init__(self,root,bg=MENU_COLOR)
        self.controller=self.root.controller
        self.object_list=[]
        self.posx=0
        self.posy=0
    def add_object(self,object,x=0,y=0):
        self.posx+=x
        self.posy+=y
        self.object_list.append(object)
    def clear(self):
        for widgets in self.winfo_children():
            widgets.destroy()
        self.posy=0

class InformationChart(tk.Canvas):
    def __init__(self,root,Df):
        global sweep_list
        self.root=root
        self.Df=Df
        self.df=Df.df
        s=ttk.Style()
        s.theme_use('clam')
        # Add the rowheight
        s.configure('Treeview', rowheight=20)
        self.treeview = ttk.Treeview(self.root,columns=list(self.df.columns), show='headings',height=self.df.shape[0])
        for column in self.df.columns:
            self.treeview.heading(column, text=column)
            self.treeview.column(column, width=100)
        for row in self.df.iterrows():
            self.treeview.insert('', 'end', values=list(row[1]))
    def update(self):
        self.Df.update()
        self.df=self.Df.df
        self.treeview.delete(*self.treeview.get_children())
        for row in self.df.iterrows():
            self.treeview.insert('', 'end', values=list(row[1]))
    def say(self):
        print(self.Df.df)
