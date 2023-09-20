import tkinter as tk

LARGE_FONT = ("CMU Serif", 16)
NORM_FONT = ("CMU Serif", 10)
SMALL_FONT = ("CMU Serif", 6)

class ButtonsAndEntries:
    def __init__(self,controller):
        self.controller=controller
    def submit(self,plot=True,load_baseline=False):
        if self.type=="int":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=int(self.entry_list[i].get())
        if self.type=="float":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=float(self.entry_list[i].get())
        if self.type=="str":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=str(self.entry_list[i].get())
        if self.type=="bool":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=bool(self.entry_list[i].get())
        if self.type=="np.array":
            self.globalparams_list[0]=np.linspace(float(self.entry_list[0].get()),float(self.entry_list[1].get()),int(self.entry_list[2].get()))
        if self.type=="radiobutton":
            self.globalparams_list[0]=self.v.get()
        if load_baseline==True:
            self.canvas.root.master.load_data(reset=False)
            self.canvas.root.master.load_baseline()
            self.canvas.root.master.smooth_data()
        if plot==True:
            self.canvas.root.master.plot()
    def submit_fitwindow(self):
        if self.type=="int":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=int(self.entry_list[i].get())
        if self.type=="float":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=float(self.entry_list[i].get())
        if self.type=="str":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=str(self.entry_list[i].get())
        if self.type=="bool":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=bool(self.entry_list[i].get())
        if self.type=="radiobutton":
            self.globalparams_list[0]=self.v.get()
        self.canvas.root.update_plot()
    def submit_onepointfitwindow(self):
        if self.type=="int":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=int(self.entry_list[i].get())
        if self.type=="float":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=float(self.entry_list[i].get())
        if self.type=="str":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=str(self.entry_list[i].get())
        if self.type=="bool":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=bool(self.entry_list[i].get())
        if self.type=="radiobutton":
            self.globalparams_list[0]=self.v.get()
        self.onepointfit()
    def submit_colorplot(self):
        if self.type=="int":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=int(self.entry_list[i].get())
        if self.type=="float":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=float(self.entry_list[i].get())
        if self.type=="str":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=str(self.entry_list[i].get())
        if self.type=="bool":
            for i in range(len(self.entry_list)):
                self.globalparams_list[i]=bool(self.entry_list[i].get())
        if self.type=="radiobutton":
            self.globalparams_list[0]=self.v.get()
        self.canvas.root.update_plot()
    # def switch(self,plot=True):
    #     if self.globalparams_list[0]==True:
    #         self.globalparams_list[0]=False
    #         self.entry_list[0].configure(text="Off")
    #     else:
    #         self.globalparams_list[0]=True
    #         self.entry_list[0].configure(text="On")
    #     if plot==True:
    #         self.canvas.root.master.plot()
    
    def fit(self):
        self.canvas.root.master.fit()
    def onepointfit(self):
        axis=(self.canvas.root.master.ax1,self.canvas.root.master.ax2,self.canvas.root.master.ax3)
        index=self.canvas.root.master.index
        index_crop=self.canvas.root.master.index_crop
        draw_canvas=self.canvas.root.master.canvas
        self.canvas.root.master.port=self.canvas.root.master.master.master.onepointfit(index,index_crop,axis,draw_canvas)
        self.canvas.root.master.fr_min=self.canvas.root.master.master.master.frmin
        self.canvas.root.master.parameterschart.update()
    def customize_plot(self):
        self.canvas.root.master.customize_plot() 
    def color_plot(self):
        self.canvas.root.master.color_plot()

class Switchs(ButtonsAndEntries):
    def __init__(self,canvas,controller,parameter,text,button_width=50,button_height=50,label_width=50,label_height=80,y_button=20):
        super().__init__(controller)
        self.button=tk.Button(canvas.root, text="On", command=lambda: self.switch(parameter))
        canvas.create_window(canvas.posx, canvas.posy+y_button,width=button_width,height=button_height,
                                   window=self.button)
        canvas.create_window(canvas.posx, canvas.posy,width=label_width,height=label_height,
                                   window=tk.Label(canvas.root, text=text,font=NORM_FONT))
    def switch(self,parameter):
        if self.button.cget("text")=="On":
            self.button.configure(text="Off")
            self.controller.parameters[parameter]=True
        else:
            self.button.configure(text="On")
            self.controller.parameters[parameter]=False
class RadioButtons(ButtonsAndEntries):
    def __init__(self,canvas,controller,parameter,possible_values,text,button_width=50,button_height=50,label_width=50,label_height=80,y_button=20):
        super().__init__(controller)
        self.v = tk.StringVar(value=self.controller.parameters[parameter])
        self.button_list=[]
        for i in range(len(possible_values)):
            self.button_list.append(tk.Radiobutton(canvas.root,indicatoron=0,
                                                   text=possible_values[i], variable=self.v, value=possible_values[i],command=lambda: self.submit(parameter)))
            canvas.create_window(canvas.posx+i*button_width, canvas.posy+y_button,width=button_width,height=button_height,
                                      window=self.button_list[i])
        canvas.create_window(canvas.posx, canvas.posy,width=label_width,height=label_height,
                                   window=tk.Label(canvas.root, text=text,font=NORM_FONT))
    def submit(self,parameter):
        self.controller.parameters[parameter]=self.v.get()
class Entries(ButtonsAndEntries):
    def __init__(self,canvas,controller,parameter_list,labels_list,type_list,button_width=50,button_height=50,label_width=50,label_height=80,y_button=20):
        super().__init__(controller)
        self.entry_list=[]
        for i in range(len(parameter_list)):
            self.entry_list.append(tk.Entry(canvas.root))
            canvas.create_window(canvas.posx+i*button_width, canvas.posy+y_button,width=button_width,height=button_height,window=self.entry_list[i])
            canvas.create_window(canvas.posx+i*button_width, canvas.posy,width=label_width,height=label_height,window=tk.Label(canvas.root, text=labels_list[i],font=NORM_FONT))
            self.entry_list[i].insert(0, self.controller.parameters[parameter_list[i]])
        canvas.create_window(canvas.posx+(len(parameter_list)+1)*button_width, canvas.posy+y_button,width=button_width,height=button_height,window=tk.Button(canvas.root, text="Submit", command=lambda: self.submit(parameter_list,type_list)))
    def submit(self,parameter_list,type_list):
        for i in range(len(self.entry_list)):
            self.controller.parameters[parameter_list[i]]=type_list[i](self.entry_list[i].get())
class Navigator(ButtonsAndEntries):
    def __init__(self,canvas,controller,parameter,possible_values,text,type=str,button_width=50,button_height=50,label_width=50,label_height=80,entry_width=50,entry_height=50,y_button=20):
        super().__init__(controller)
        self.entry=tk.Entry(canvas.root)
        canvas.create_window(canvas.posx, canvas.posy+y_button,width=entry_width,height=entry_height,window=self.entry)
        self.entry.insert(0, self.controller.parameters[parameter])

        #next and previous color in colormap_list buttons
        canvas.create_window(canvas.posx+entry_width*1.2, canvas.posy+y_button,width=button_width,height=button_height,
                                   window=tk.Button(canvas.root, text="<", command=lambda: self.previous(parameter,possible_values)))
        canvas.create_window(canvas.posx+entry_width*1.2+button_width, canvas.posy+y_button,width=button_width,height=button_height,
                                   window=tk.Button(canvas.root, text=">", command=lambda: self.next(parameter,possible_values)))
        canvas.create_window(canvas.posx+entry_width*1.2+2*button_width, canvas.posy+y_button,width=button_width,height=button_height,
                                   window=tk.Button(canvas.root, text="Submit", command=lambda: self.submit(parameter,type)))
        canvas.create_window(canvas.posx, canvas.posy,width=label_width,height=label_height,
                                   window=tk.Label(canvas.root, text=text,font=NORM_FONT))
    def previous(self,parameter,possible_values):
        try:
            new_value=possible_values[possible_values.index(self.controller.parameters[parameter])-1]
        except:
            new_value=possible_values[-1]
        self.entry.delete(0,tk.END)
        self.entry.insert(0, new_value)
    def next(self,parameter,possible_values):
        try:
            new_value=possible_values[possible_values.index(self.controller.parameters[parameter])+1]
        except:
            new_value=possible_values[0]
        self.entry.delete(0,tk.END)
        self.entry.insert(0, new_value)
    def submit(self,parameter,type):
        self.controller.parameters[parameter]=type(self.entry.get())
class FunctionButtons(ButtonsAndEntries):
    def __init__(self,canvas,controller,func,text,button_width=50,button_height=50):
        super().__init__(controller)
        canvas.create_window(canvas.posx, canvas.posy,width=button_width,height=button_height,
                                   window=tk.Button(canvas.root, text=text, command=lambda: func))


        
       

class SweepFile(ButtonsAndEntries):
    def __init__(self,canvas):
        global file
        #parameters for this button
        self.type="int"
        self.globalparams_list=file
        self.entry_list=[]
        self.canvas=canvas

        label_width=60
        button_width=50
        entry_width=50
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160+i*entry_width, self.canvas.posy+140,width=entry_width,height=entry_height, window=self.entry_list[i])
            self.entry_list[i].insert(0, self.globalparams_list[i])
        
        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+240, self.canvas.posy+140,width=button_width,height=button_height,window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.nextdata()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height,
                                   window=tk.Label(self.canvas.root, text="File",font=NORM_FONT))
    def nextdata(self):
        global file
        self.entry_list[0].delete(0,tk.END)
        self.entry_list[0].insert(0, file[0])
        self.canvas.root.load_data()
        self.canvas.root.load_baseline()
        self.canvas.root.smooth_data()
        self.canvas.root.master.plot()


class SweepButtons(ButtonsAndEntries):
    def __init__(self,canvas):
        global sweep_list
        #parameters for this button
        self.type="int"
        self.globalparams_list=sweep_list
        self.entry_list=[]
        self.canvas=canvas

        label_width=70
        button_width=50
        entry_width=50
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160+i*70, self.canvas.posy+140,width=entry_width,height=entry_height, window=self.entry_list[i])
            self.entry_list[i].insert(0, self.globalparams_list[i])

        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+370, self.canvas.posy+140,width=button_width,height=button_height, window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height, window=tk.Label(self.canvas.root, text="Initial",font=NORM_FONT))
        self.canvas.create_window(self.canvas.posx+230, self.canvas.posy+120,width=label_width,height=label_height, window=tk.Label(self.canvas.root, text="End",font=NORM_FONT))
        self.canvas.create_window(self.canvas.posx+300, self.canvas.posy+120,width=label_width,height=label_height, window=tk.Label(self.canvas.root, text="Step",font=NORM_FONT))

class Shift(ButtonsAndEntries):
    def __init__(self,canvas):
        global shift

        #parameters for this button
        self.type="float"
        self.globalparams_list=shift
        self.entry_list=[]
        self.canvas=canvas

        label_width=60
        button_width=50
        entry_width=50
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160+i*40, self.canvas.posy+140,width=entry_width,height=entry_height,window=self.entry_list[i])
            self.entry_list[i].insert(0, self.globalparams_list[i])

        #draw the submit button and the labels  
        self.canvas.create_window(self.canvas.posx+240, self.canvas.posy+140,width=button_width,height=button_height,
                                   window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height,
                                   window=tk.Label(self.canvas.root, text="Shift",font=NORM_FONT))

class Colour(ButtonsAndEntries):
    def __init__(self,canvas):
        global colormap
        #parameters for this button
        self.type="str"
        self.globalparams_list=colormap
        self.entry_list=[]
        self.canvas=canvas

        label_width=60
        button_width=50
        entry_width=50
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160+i*40, self.canvas.posy+140,width=entry_width,height=entry_height,window=self.entry_list[i])
            self.entry_list[i].insert(0, self.globalparams_list[i])

        #draw the submit button and the labels  
        self.canvas.create_window(self.canvas.posx+320, self.canvas.posy+140,width=button_width,height=button_height,
                                   window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height,
                                   window=tk.Label(self.canvas.root, text="Colormap",font=NORM_FONT))

        #next and previous color in colormap_list buttons
        self.canvas.create_window(self.canvas.posx+220, self.canvas.posy+140,width=button_width,height=button_height,
                                   window=tk.Button(self.canvas.root, text="<", command=lambda: self.previous()))
        self.canvas.create_window(self.canvas.posx+270, self.canvas.posy+140,width=button_width,height=button_height,
                                   window=tk.Button(self.canvas.root, text=">", command=lambda: self.next()))
    def previous(self):
        global colormap
        if colormap[0] in colormap_list:
            colormap[0]=colormap_list[colormap_list.index(colormap[0])-1]
        self.entry_list[0].delete(0,tk.END)
        self.entry_list[0].insert(0, colormap[0])
    def next(self):
        global colormap
        if colormap[0] in colormap_list:
            colormap[0]=colormap_list[colormap_list.index(colormap[0])+1]
        self.entry_list[0].delete(0,tk.END)
        self.entry_list[0].insert(0, colormap[0])
class Cbar(ButtonsAndEntries):
    def __init__(self,canvas):
        global cbarbool
        #parameters for this button
        self.type="bool"
        self.globalparams_list=cbarbool
        self.entry_list=[]
        self.canvas=canvas

        label_width=60
        button_width=50
        label_height=20
        button_height=60
        #create an on/off switch button
        self.entry_list.append(tk.Button(self.canvas.root, text="On", command=lambda: self.switch()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=button_width,height=button_height,
                                  window=self.entry_list[0])
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height,
                                   window=tk.Label(self.canvas.root, text="Colorbar",font=NORM_FONT))

class CbarSweep(ButtonsAndEntries):
    def __init__(self,canvas):
        global cbarsweep

        #parameters for this button
        self.type="radiobutton"
        self.globalparams_list=cbarsweep
        self.entry_list=[]
        self.canvas=canvas
        #create the buttons and the entries
        possible_values=["T","P","B","Bx","By","Bz"]
        self.v = tk.StringVar(value=cbarsweep[0])

        button_width=50
        button_height=60

        #create a radio button for each possible value
        for i in range(len(possible_values)):
            self.entry_list.append(tk.Radiobutton(self.canvas.root,indicatoron=0,
                                                   text=possible_values[i], variable=self.v, value=possible_values[i],command=lambda: self.submit()))
            self.canvas.create_window(self.canvas.posx+160+i*50, self.canvas.posy+140,width=button_width,height=button_height,
                                      window=self.entry_list[i])
class Fit(ButtonsAndEntries):
    def __init__(self,canvas):
        #parameters for this button
        self.canvas=canvas
        button_width=50
        button_height=60
        #create a button that opens a new window called Fit
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=button_width,height=button_height,
                                   window=tk.Button(self.canvas.root, text="Fit", command=lambda: self.fit()))
class GuessDelay(ButtonsAndEntries):
    def __init__(self,canvas):
        global guessdelay
        #parameters for this button
        self.type="bool"
        self.globalparams_list=guessdelay
        self.entry_list=[]
        self.canvas=canvas
        label_width=100
        button_width=50
        label_height=20
        button_height=60

        #create an on/off switch button
        self.entry_list.append(tk.Button(self.canvas.root, text="Off", command=lambda: self.switch(plot=False)))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=button_width,height=button_height,
                                   window=self.entry_list[0])
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height,
                                   window=tk.Label(self.canvas.root, text="Guess delay",font=NORM_FONT))
class PlotParameters(ButtonsAndEntries):
    def __init__(self,canvas):
        button_width=120
        button_height=60
        self.canvas=canvas
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=button_width,height=button_height,
                                      window=tk.Button(self.canvas.root, text="Customize plot", command=lambda: self.customize_plot()))
class ColorPlotButton(ButtonsAndEntries):
    def __init__(self,canvas):
        button_width=120
        button_height=60
        self.canvas=canvas
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=button_width,height=button_height,
                                      window=tk.Button(self.canvas.root, text="Color plot", command=lambda: self.color_plot()))
class Fontsize(ButtonsAndEntries):
    def __init__(self,canvas):
        global fontsize
        #parameters for this button
        self.type="float"
        self.globalparams_list=fontsize
        self.entry_list=[]
        self.canvas=canvas
        label_width=60
        button_width=50
        entry_width=50
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160+i*40, self.canvas.posy+140,width=entry_width,height=entry_height,
                                      window=self.entry_list[i])
            self.entry_list[i].insert(0, self.globalparams_list[i])
        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+160+6*40, self.canvas.posy+140,width=button_width,height=button_height,
                                      window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height,
                                      window=tk.Label(self.canvas.root, text="Fontsize",font=NORM_FONT))
class ColorPlotFontsize(ButtonsAndEntries):
    def __init__(self,canvas):
        global colorplotfontsize
        #parameters for this button
        self.type="float"
        self.globalparams_list=colorplotfontsize
        self.entry_list=[]
        self.canvas=canvas
        label_width=60
        button_width=50
        entry_width=50
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160+i*40, self.canvas.posy+140,width=entry_width,height=entry_height,
                                      window=self.entry_list[i])
            self.entry_list[i].insert(0, self.globalparams_list[i])
        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+160+6*40, self.canvas.posy+140,width=button_width,height=button_height,
                                      window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit_colorplot()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height,
                                      window=tk.Label(self.canvas.root, text="Fontsize",font=NORM_FONT))
class PlotLabels(ButtonsAndEntries):
    def __init__(self,canvas):
        global plotlabels
        #parameters for this button
        self.type="str"
        self.globalparams_list=plotlabels
        self.entry_list=[]
        self.canvas=canvas
        label_width=60
        button_width=50
        entry_width=180
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140+i*entry_height,width=entry_width,height=entry_height,
                                      window=self.entry_list[i])
            self.entry_list[i].insert(0, self.globalparams_list[i])
        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+140+entry_width, self.canvas.posy+170,width=button_width,height=button_height,
                                      window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+105,width=label_width,height=label_height,
                                      window=tk.Label(self.canvas.root, text="Labels",font=NORM_FONT))
class ColorPlotLabels(ButtonsAndEntries):
    def __init__(self,canvas):
        global colorplotlabels
        #parameters for this button
        self.type="str"
        self.globalparams_list=colorplotlabels
        self.entry_list=[]
        self.canvas=canvas
        label_width=60
        button_width=50
        entry_width=180
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140+i*entry_height,width=entry_width,height=entry_height,
                                        window=self.entry_list[i])
            self.entry_list[i].insert(0, self.globalparams_list[i])
        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+140+entry_width, self.canvas.posy+170,width=button_width,height=button_height,
                                        window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit_colorplot()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+105,width=label_width,height=label_height,
                                        window=tk.Label(self.canvas.root, text="Labels",font=NORM_FONT))
class ColorPlotColormap(ButtonsAndEntries):
    def __init__(self,canvas):
        global colorplotcolormap
        #parameters for this button
        self.type="str"
        self.globalparams_list=colorplotcolormap
        self.entry_list=[]
        self.canvas=canvas

        label_width=60
        button_width=50
        entry_width=50
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160+i*40, self.canvas.posy+140,width=entry_width,height=entry_height,window=self.entry_list[i])
            self.entry_list[i].insert(0, self.globalparams_list[i])

        #draw the submit button and the labels  
        self.canvas.create_window(self.canvas.posx+320, self.canvas.posy+140,width=button_width,height=button_height,
                                   window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit_colorplot()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height,
                                   window=tk.Label(self.canvas.root, text="Colormap",font=NORM_FONT))

        #next and previous color in colormap_list buttons
        self.canvas.create_window(self.canvas.posx+220, self.canvas.posy+140,width=button_width,height=button_height,
                                   window=tk.Button(self.canvas.root, text="<", command=lambda: self.previous()))
        self.canvas.create_window(self.canvas.posx+270, self.canvas.posy+140,width=button_width,height=button_height,
                                   window=tk.Button(self.canvas.root, text=">", command=lambda: self.next()))
    def previous(self):
        global colorplotcolormap
        if colorplotcolormap[0] in colormap_list:
            colorplotcolormap[0]=colormap_list[colormap_list.index(colorplotcolormap[0])-1]
        self.entry_list[0].delete(0,tk.END)
        self.entry_list[0].insert(0, colorplotcolormap[0])
    def next(self):
        global colorplotcolormap
        if colorplotcolormap[0] in colormap_list:
            colorplotcolormap[0]=colormap_list[colormap_list.index(colorplotcolormap[0])+1]
        self.entry_list[0].delete(0,tk.END)
        self.entry_list[0].insert(0, colorplotcolormap[0])

class GridBool(ButtonsAndEntries):
    def __init__(self,canvas):
        global grid_bool
        #parameters for this button
        self.type="bool"
        self.globalparams_list=grid_bool
        self.entry_list=[]
        self.canvas=canvas
        label_width=100
        button_width=50
        label_height=20
        button_height=60

        #create an on/off switch button
        self.entry_list.append(tk.Button(self.canvas.root, text="On", command=lambda: self.switch()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=button_width,height=button_height,
                                   window=self.entry_list[0])
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height,
                                   window=tk.Label(self.canvas.root, text="Grid",font=NORM_FONT))
class XTicks(ButtonsAndEntries):
    def __init__(self,canvas):
        global xticks
        #parameters for this button
        self.type="np.array"
        self.globalparams_list=xticks
        self.entry_list=[]
        self.canvas=canvas

        label_width=70
        button_width=50
        entry_width=50
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(3):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160+i*70, self.canvas.posy+140,width=entry_width,height=entry_height, window=self.entry_list[i])

        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+370, self.canvas.posy+140,width=button_width,height=button_height, window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height, window=tk.Label(self.canvas.root, text="Initial",font=NORM_FONT))
        self.canvas.create_window(self.canvas.posx+230, self.canvas.posy+120,width=label_width,height=label_height, window=tk.Label(self.canvas.root, text="End",font=NORM_FONT))
        self.canvas.create_window(self.canvas.posx+300, self.canvas.posy+120,width=label_width,height=label_height, window=tk.Label(self.canvas.root, text="Interval number",font=NORM_FONT))
class YTicks(ButtonsAndEntries):
    def __init__(self,canvas):
        global yticks
        #parameters for this button
        self.type="np.array"
        self.globalparams_list=yticks
        self.entry_list=[]
        self.canvas=canvas

        label_width=70
        button_width=50
        entry_width=50
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(3):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160+i*70, self.canvas.posy+140,width=entry_width,height=entry_height, window=self.entry_list[i])

        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+370, self.canvas.posy+140,width=button_width,height=button_height, window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height, window=tk.Label(self.canvas.root, text="Initial",font=NORM_FONT))
        self.canvas.create_window(self.canvas.posx+230, self.canvas.posy+120,width=label_width,height=label_height, window=tk.Label(self.canvas.root, text="End",font=NORM_FONT))
        self.canvas.create_window(self.canvas.posx+300, self.canvas.posy+120,width=label_width,height=label_height, window=tk.Label(self.canvas.root, text="Interval number",font=NORM_FONT))


class Linestyle(ButtonsAndEntries):
    def __init__(self,canvas):
        global linestyle
        #parameters for this button
        self.type="str"
        self.globalparams_list=linestyle
        self.entry_list=[]
        self.canvas=canvas

        label_width=60
        button_width=50
        entry_width=50
        label_height=20
        button_height=60
        entry_height=20
        
        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.entry_list[i].insert(0, self.globalparams_list[i])
            self.canvas.create_window(self.canvas.posx+160+i*40, self.canvas.posy+140,width=entry_width,height=entry_height,window=self.entry_list[i])
        
        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+240, self.canvas.posy+140,width=button_width,height=button_height,
                                      window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height,
                                        window=tk.Label(self.canvas.root, text="Linestyle",font=NORM_FONT)) 

class Linewidth(ButtonsAndEntries):
    def __init__(self,canvas):
        global linewidth
        #parameters for this button
        self.type="float"
        self.globalparams_list=linewidth
        self.entry_list=[]
        self.canvas=canvas

        label_width=60
        button_width=50
        entry_width=50
        label_height=20
        button_height=60
        entry_height=20
        
        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.entry_list[i].insert(0, self.globalparams_list[i])
            self.canvas.create_window(self.canvas.posx+160+i*40, self.canvas.posy+140,width=entry_width,height=entry_height,window=self.entry_list[i])
        
        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+240, self.canvas.posy+140,width=button_width,height=button_height,
                                      window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height,
                                        window=tk.Label(self.canvas.root, text="Linewidth",font=NORM_FONT))
class TicksIn(ButtonsAndEntries):
    def __init__(self,canvas):
        global ticksin
        #parameters for this button
        self.type="bool"
        self.globalparams_list=ticksin
        self.entry_list=[]
        self.canvas=canvas
        label_width=100
        button_width=50
        label_height=20
        button_height=60

        #create an on/off switch button
        self.entry_list.append(tk.Button(self.canvas.root, text="On", command=lambda: self.switch()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=button_width,height=button_height,
                                   window=self.entry_list[0])
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height,
                                   window=tk.Label(self.canvas.root, text="Ticks in",font=NORM_FONT))
class FitWindowLabelsX(ButtonsAndEntries):
    def __init__(self,canvas):
        global xlabel_fitwindow
        #parameters for this button
        self.type="str"
        self.globalparams_list=xlabel_fitwindow
        self.entry_list=[]
        self.canvas=canvas
        label_width=60
        button_width=50
        entry_width=180
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140+i*entry_height,width=entry_width,height=entry_height,
                                      window=self.entry_list[i])
            self.entry_list[i].insert(0, self.globalparams_list[i])
        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+140+entry_width, self.canvas.posy+170,width=button_width,height=button_height,
                                      window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit_fitwindow()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+105,width=label_width,height=label_height,
                                      window=tk.Label(self.canvas.root, text="X Label",font=NORM_FONT))
class FitWindowLabelsY(ButtonsAndEntries):
    def __init__(self,canvas):
        global ylabel_fitwindow
        #parameters for this button
        self.type="str"
        self.globalparams_list=ylabel_fitwindow
        self.entry_list=[]
        self.canvas=canvas
        label_width=60
        button_width=50
        entry_width=180
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140+i*entry_height,width=entry_width,height=entry_height,
                                      window=self.entry_list[i])
            self.entry_list[i].insert(0, self.globalparams_list[i])
        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+140+entry_width, self.canvas.posy+170,width=button_width,height=button_height,
                                      window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit_fitwindow()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+105,width=label_width,height=label_height,
                                      window=tk.Label(self.canvas.root, text="Y Label",font=NORM_FONT)) 
class FitWindowSuptitle(ButtonsAndEntries):
    def __init__(self,canvas):
        global suptitle_fitwindow
        #parameters for this button
        self.type="str"
        self.globalparams_list=suptitle_fitwindow
        self.entry_list=[]
        self.canvas=canvas
        label_width=60
        button_width=50
        entry_width=180
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140+i*entry_height,width=entry_width,height=entry_height,
                                      window=self.entry_list[i])
            self.entry_list[i].insert(0, self.globalparams_list[i])
        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+140+entry_width, self.canvas.posy+170,width=button_width,height=button_height,
                                      window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit_fitwindow()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+105,width=label_width,height=label_height,
                                      window=tk.Label(self.canvas.root, text="Suptitle",font=NORM_FONT))
class FitWindowSave(ButtonsAndEntries):
    def __init__(self,canvas):
        #ask for a place to save the data in the figs
        self.canvas=canvas
        button_width=50
        button_height=60
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=button_width,height=button_height,
                                        window=tk.Button(self.canvas.root, text="Save", command=lambda: self.save()))
    def save(self):
        self.canvas.root.save()


class PlotY(ButtonsAndEntries):
    def __init__(self,canvas):
        global yplot
        global yplot_list
        #parameters for this button
        self.type="radiobutton"
        self.globalparams_list=yplot
        self.entry_list=[]
        self.canvas=canvas
        #create the buttons and the entries
        possible_values=yplot_list
        self.v = tk.StringVar(value=yplot[0])

        button_width=50
        button_height=60

        #create a radio button for each possible value
        for i in range(len(possible_values)):
            self.entry_list.append(tk.Radiobutton(self.canvas.root,indicatoron=0,
                                                   text=possible_values[i], variable=self.v, value=possible_values[i],command=lambda: self.submit()))
            self.canvas.create_window(self.canvas.posx+160+i*50, self.canvas.posy+140,width=button_width,height=button_height,
                                      window=self.entry_list[i])

class Baseline(ButtonsAndEntries):
    def __init__(self,canvas):
        global baseline_folder
        #parameters for this button
        self.type="str"
        self.globalparams_list=baseline_folder
        self.entry_list=[]
        self.canvas=canvas
        label_width=100
        button_width=50
        label_height=20
        button_height=60

        #create an on/off switch button
        self.entry_list.append(tk.Button(self.canvas.root, text="Off", command=lambda: self.switch_baseline()))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=button_width,height=button_height,
                                   window=self.entry_list[0])
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height,
                                   window=tk.Label(self.canvas.root, text="Baseline",font=NORM_FONT))
class BaselineSweep(ButtonsAndEntries):
    def __init__(self,canvas):
        global baseline_sweep

        #parameters for this button
        self.type="int"
        self.globalparams_list=baseline_sweep
        self.entry_list=[]
        self.canvas=canvas

        label_width=70
        button_width=50
        entry_width=50
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        for i in range(len(self.globalparams_list)):
            self.entry_list.append(tk.Entry(self.canvas.root))
            self.canvas.create_window(self.canvas.posx+160+i*70, self.canvas.posy+140,width=entry_width,height=entry_height, window=self.entry_list[i])
            self.entry_list[i].insert(0, self.globalparams_list[i])
        
        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+370, self.canvas.posy+140,width=button_width,height=button_height,window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit(load_baseline=True)))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height, window=tk.Label(self.canvas.root, text="File",font=NORM_FONT))
        self.canvas.create_window(self.canvas.posx+230, self.canvas.posy+120,width=label_width,height=label_height, window=tk.Label(self.canvas.root, text="Sweep",font=NORM_FONT))
        self.canvas.create_window(self.canvas.posx+300, self.canvas.posy+120,width=label_width,height=label_height, window=tk.Label(self.canvas.root, text="Shift (+)",font=NORM_FONT))
class Smooth(ButtonsAndEntries):
    def __init__(self,canvas):
        global smoothlist
        #parameters for this button
        self.type="int"
        self.globalparams_list=smoothlist
        self.entry_list=[]
        self.canvas=canvas

        label_width=60
        button_width=50
        entry_width=50
        label_height=20
        button_height=60
        entry_height=20

        #create the buttons and the entries
        self.entry_list.append(tk.Entry(self.canvas.root))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=entry_width,height=entry_height, window=self.entry_list[0])
        self.entry_list[0].insert(0, self.globalparams_list[0])

        #draw the submit button and the labels
        self.canvas.create_window(self.canvas.posx+240, self.canvas.posy+140,width=button_width,height=button_height,window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit(load_baseline=True)))
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+120,width=label_width,height=label_height, window=tk.Label(self.canvas.root, text="Smooth",font=NORM_FONT))



class OnePointFit(ButtonsAndEntries):
    def __init__(self,canvas):
        #parameters for this button
        self.canvas=canvas
        button_width=50
        button_height=60
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=button_width,height=button_height,
                                   window=tk.Button(self.canvas.root, text="Fit", command=lambda: self.onepointfit()))

class OnePointFitLabelsX(ButtonsAndEntries):
    def __init__(self,canvas):
            global xlabel_onepointfitwindow
            #parameters for this button
            self.type="str"
            self.globalparams_list=xlabel_onepointfitwindow
            self.entry_list=[]
            self.canvas=canvas
            label_width=60
            button_width=50
            entry_width=180
            label_height=20
            button_height=60
            entry_height=20

            #create the buttons and the entries
            for i in range(len(self.globalparams_list)):
                self.entry_list.append(tk.Entry(self.canvas.root))
                self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140+i*entry_height,width=entry_width,height=entry_height,
                                        window=self.entry_list[i])
                self.entry_list[i].insert(0, self.globalparams_list[i])
            #draw the submit button and the labels
            self.canvas.create_window(self.canvas.posx+140+entry_width, self.canvas.posy+170,width=button_width,height=button_height,
                                        window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit_onepointfitwindow()))
            self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+105,width=label_width,height=label_height,
                                        window=tk.Label(self.canvas.root, text="X Label",font=NORM_FONT))
class OnePointFitLabelsY(ButtonsAndEntries):
    def __init__(self,canvas):
            global ylabel_onepointfitwindow
            #parameters for this button
            self.type="str"
            self.globalparams_list=ylabel_onepointfitwindow
            self.entry_list=[]
            self.canvas=canvas
            label_width=60
            button_width=50
            entry_width=180
            label_height=20
            button_height=60
            entry_height=20

            #create the buttons and the entries
            for i in range(len(self.globalparams_list)):
                self.entry_list.append(tk.Entry(self.canvas.root))
                self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140+i*entry_height,width=entry_width,height=entry_height,
                                        window=self.entry_list[i])
                self.entry_list[i].insert(0, self.globalparams_list[i])
            #draw the submit button and the labels
            self.canvas.create_window(self.canvas.posx+140+entry_width, self.canvas.posy+170,width=button_width,height=button_height,
                                        window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit_onepointfitwindow()))
            self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+105,width=label_width,height=label_height,
                                        window=tk.Label(self.canvas.root, text="Y Label",font=NORM_FONT))
class OnePointFitSuptitle(ButtonsAndEntries):
    def __init__(self,canvas):
            global suptitle_onepointfitwindow
            #parameters for this button
            self.type="str"
            self.globalparams_list=suptitle_onepointfitwindow
            self.entry_list=[]
            self.canvas=canvas
            label_width=60
            button_width=50
            entry_width=180
            label_height=20
            button_height=60
            entry_height=20

            #create the buttons and the entries
            for i in range(len(self.globalparams_list)):
                self.entry_list.append(tk.Entry(self.canvas.root))
                self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140+i*entry_height,width=entry_width,height=entry_height,
                                        window=self.entry_list[i])
                self.entry_list[i].insert(0, self.globalparams_list[i])
            #draw the submit button and the labels
            self.canvas.create_window(self.canvas.posx+140+entry_width, self.canvas.posy+170,width=button_width,height=button_height,
                                        window=tk.Button(self.canvas.root, text="Submit", command=lambda: self.submit_onepointfitwindow()))
            self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+105,width=label_width,height=label_height,
                                        window=tk.Label(self.canvas.root, text="Suptitle",font=NORM_FONT))
class OnePointFitSave(ButtonsAndEntries):
    def __init__(self,canvas):
        #ask for a place to save the data in the figs
        self.canvas=canvas
        button_width=50
        button_height=60
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=button_width,height=button_height,
                                      window=tk.Button(self.canvas.root, text="Save plot", command=lambda: self.save()))
    def save(self):
        self.canvas.root.master.save()

class OnePointFitSaveChart(ButtonsAndEntries):
    def __init__(self,canvas):
        #ask for a place to save the data in the figs
        self.canvas=canvas
        button_width=50
        button_height=60
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=button_width,height=button_height,
                                      window=tk.Button(self.canvas.root, text="Save chart", command=lambda: self.save_chart()))
    def save_chart(self):
        self.canvas.root.master.save_chart()