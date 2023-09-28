import tkinter as tk

LARGE_FONT = ("CMU Serif", 16)
NORM_FONT = ("CMU Serif", 10)
SMALL_FONT = ("CMU Serif", 6)

class ButtonsAndEntries:
    def __init__(self,controller):
        self.controller=controller

class Switchs(ButtonsAndEntries):
    def __init__(self,canvas,parameter,text,button_width=50,button_height=20,label_width=50,label_height=30,y_button=20):
        super().__init__(canvas.controller)
        self.button=tk.Button(canvas.root, text="On", command=lambda: self.switch(parameter))
        canvas.create_window(canvas.posx, canvas.posy+y_button,width=button_width,height=button_height,
                                   window=self.button)
        canvas.create_window(canvas.posx, canvas.posy,width=label_width,height=label_height,
                                   window=tk.Label(canvas.root, text=text,font=NORM_FONT))
    def switch(self,parameter):
        if self.button.cget("text")=="On":
            self.button.configure(text="Off")
            self.controller.parameters[parameter]=False
        else:
            self.button.configure(text="On")
            self.controller.parameters[parameter]=True
class RadioButtons(ButtonsAndEntries):
    def __init__(self,canvas,parameter,possible_values,text,button_width=50,button_height=20,label_width=50,label_height=30,y_button=20):
        super().__init__(canvas.controller)
        self.parameter=parameter
        self.v = tk.StringVar(value=self.controller.parameters[parameter])
        self.button_list=[]
        for i in range(len(possible_values)):
            self.button_list.append(tk.Radiobutton(canvas.root,indicatoron=0,
                                                   text=possible_values[i], variable=self.v, value=possible_values[i],command=lambda: self.submit(parameter)))
            canvas.create_window(canvas.posx+i*button_width, canvas.posy+y_button,width=button_width,height=button_height,
                                      window=self.button_list[i])
        canvas.create_window(canvas.posx, canvas.posy,width=label_width,height=label_height,
                                   window=tk.Label(canvas.root, text=text,font=NORM_FONT))
    def submit(self):
        self.controller.parameters[self.parameter]=self.v.get()
class Entries(ButtonsAndEntries):
    def __init__(self,canvas,parameter_list,labels_list,type_list,button_width=50,button_height=30,label_width=50,label_height=30,y_button=20):
        super().__init__(canvas.controller)
        self.entry_list=[]
        self.parameter_list=parameter_list
        self.type_list=type_list
        for i in range(len(parameter_list)):
            self.entry_list.append(tk.Entry(canvas.root))
            canvas.create_window(canvas.posx+i*button_width, canvas.posy+y_button,width=button_width,height=button_height,window=self.entry_list[i])
            canvas.create_window(canvas.posx+i*button_width, canvas.posy,width=label_width,height=label_height,window=tk.Label(canvas.root, text=labels_list[i],font=NORM_FONT))
            try:
                self.entry_list[i].insert(0, self.controller.parameters[parameter_list[i]])
            except:
                self.entry_list[i].insert(0,"")

    def submit(self):
        for i in range(len(self.entry_list)):
            self.controller.parameters[self.parameter_list[i]]=self.type_list[i](self.entry_list[i].get())
class Navigator(ButtonsAndEntries):
    def __init__(self,canvas,parameter,possible_values,text,type=str,button_width=50,button_height=30,label_width=50,label_height=30,entry_width=50,entry_height=50,y_button=20):
        super().__init__(canvas.controller)
        self.parameter=parameter
        self.type=type
        self.entry=tk.Entry(canvas.root)
        canvas.create_window(canvas.posx, canvas.posy+y_button,width=entry_width,height=entry_height,window=self.entry)
        self.entry.insert(0, self.controller.parameters[parameter])

        #next and previous color in colormap_list buttons
        canvas.create_window(canvas.posx+entry_width*1.2, canvas.posy+y_button,width=button_width,height=button_height,
                                   window=tk.Button(canvas.root, text="<", command=lambda: self.previous(parameter,possible_values)))
        canvas.create_window(canvas.posx+entry_width*1.2+button_width, canvas.posy+y_button,width=button_width,height=button_height,
                                   window=tk.Button(canvas.root, text=">", command=lambda: self.next(parameter,possible_values)))
        canvas.create_window(canvas.posx, canvas.posy,width=label_width,height=label_height,
                                   window=tk.Label(canvas.root, text=text,font=NORM_FONT))
    def previous(self,parameter,possible_values):
        try:
            new_value=possible_values[possible_values.index(self.entry.get())-1]
        except:
            new_value=possible_values[-1]
        self.entry.delete(0,tk.END)
        self.entry.insert(0, new_value)
    def next(self,parameter,possible_values):
        
        try:
            new_value=possible_values[possible_values.index(self.entry.get())+1]
        except:
            new_value=possible_values[0]
        self.entry.delete(0,tk.END)
        self.entry.insert(0, new_value)
    def submit(self):
        self.controller.parameters[self.parameter]=self.type(self.entry.get())
class FunctionButtons(ButtonsAndEntries):
    def __init__(self,canvas,func,text,button_width=50,button_height=30):
        super().__init__(canvas.controller)
        canvas.create_window(canvas.posx, canvas.posy,width=button_width,height=button_height,
                                   window=tk.Button(canvas.root, text=text, command=func))