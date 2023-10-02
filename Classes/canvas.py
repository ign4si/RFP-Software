import tkinter as tk
from tkinter import ttk
MENU_COLOR="#1B252F"


class ControlCanvas(tk.Canvas):
    def __init__(self,root,controller,xini=100,yini=100):
        tk.Canvas.__init__(self,root,bg=MENU_COLOR)
        self.root=root
        self.controller=controller
        self.object_list=[]
        self.posx=xini
        self.posy=yini
    def move(self,x,y):
        self.posx+=x
        self.posy+=y
    def add_object(self,object):
        self.object_list.append(object)
    def clear(self):
        for widgets in self.winfo_children():
            widgets.destroy()
        self.posy=0
    def submit_all(self):
        autoscale=0
        for object in self.object_list:
            if object.check_change():
                object.submit()
                if object.autoscale:
                    autoscale=1
        self.controller.plot()
        if autoscale==1:
            self.controller.autoscale()

class InformationChart(tk.Canvas):
    def __init__(self,root,Df,controller):
        self.controller=controller
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
