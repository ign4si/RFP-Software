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
import Sonnet.Sliders as Sliders 
import os
from scipy.optimize import fsolve
from scipy.optimize import curve_fit
from lmfit import minimize, Parameters, fit_report
import sys



LARGE_FONT = ("CMU Serif", 16)
NORM_FONT = ("CMU Serif", 10)
SMALL_FONT = ("CMU Serif", 6)

SIZE_Y=720
SIZE_X=1280

HOMEPAGEBG="#273746"
MENU_COLOR="#1B252F"

folder="hola"
sonnet_file="hola"
compensation_file="hola"

i=0
sweep_list=[0,-1,1]
file=[0]
shift=[0]
colormap=["coolwarm"]
colorplotcolormap=["coolwarm"]
compensationcolormap=["coolwarm"]
colormap_list=['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 
'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']
cbarbool=[True]
cbarsweep=["T"]
guessdelay=[False]

yplot=["S21"]
yplot_list=["S21","S21dB","Phase"]
xlabel_fitwindow=["$\mathrm{T}$ $\mathrm{(K)}$"]
ylabel_fitwindow=["$\mathrm{f}_\mathrm{r}$","$\mathrm{Q}_\mathrm{i}$","$\mathrm{Q}_\mathrm{i}$"]
suptitle_fitwindow=["$\mathrm{Fitted}$ $\mathrm{parameters}$"]
xlabel_onepointfitwindow=["$\mathrm{Re}\mathrm{(S}_{21}\mathrm{)}$","$\mathrm{Frequency}$ $\mathrm{(GHz)}$","$\mathrm{Frequency}$ $\mathrm{(GHz)}$"]
ylabel_onepointfitwindow=["$\mathrm{Im}\mathrm{(S}_{21}\mathrm{)}$","$\mathrm{S}_{21}$","$\mathrm{Phase}$"]
suptitle_onepointfitwindow=["$\mathrm{Fit}$"]
colorplotfontsize=[15,15,15,15,15]
colorplotlabels=["$\mathrm{Frequency}$ $\mathrm{(GHz)}$","$\mathrm{T} \mathrm{(K)}$","$\mathrm{Color} \mathrm{Plot}$","$\mathrm{S_{21}}$"]
baseline_folder=[""]
baseline_sweep=[0,0,0]
smoothlist=[0]
window_size=[10]


fontsize=[15,15,15,15,15]
plotlabels=["$\mathrm{Frequency}$ $\mathrm{(GHz)}$","$\mathrm{S}_{21}$","$\mathrm{Frequency}$ $\mathrm{sweep}$","$\mathrm{T (K)}$"]
grid_bool=[True]
xticks=[None]
yticks=[None]
marker_size=[1]
linewidth=[1]
linestyle=["solid"]
ticksin=[True]

init_phi0= -50
init_Qc = 0
init_Qi = 0
init_fr =0#Estimation of the resonante frequency 

deltaphi=10
deltafr=0.001
deltaQc=40e3
deltaQi=0.05e6
f=[]
amp=[]
angle=[]

#function that smooths a y array, simple
def smoothfunc(y, box_pts):
    if box_pts==0:
        return y
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def find_min(x,y,window_size=10):
            min_index=np.argmin(y)
            #make a second order polynomial fit around the minimum and find the minimum of the fit
            x=x[min_index-window_size:min_index+window_size]
            y=y[min_index-window_size:min_index+window_size]
            fit=np.polyfit(x,y,2)
            xmin=-fit[1]/(2*fit[0])
            ymin=fit[0]*xmin**2+fit[1]*xmin+fit[2]
            return xmin,ymin

class MainContainer(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="tkinterstuff\logo.ico")
        tk.Tk.wm_title(self, "RFP")
        tk.Tk.wm_geometry(self, self.geometry())
        self.state('zoomed')


        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
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
        global sweep_list
        global baseline_folder
        global baseline_sweep
        frame = self.frames[cont]
        frame.tkraise()
        if cont==Workspace:
            frame.title.text=folder
        if cont==StartPage:
            sweep_list=[0,-1,1]
            baseline_folder=[""]
            baseline_sweep=[0,0,0]
class StartPage(Windows):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent,bg=HOMEPAGEBG)
        
        load = Image.open("tkinterstuff\logo.png")
        load.thumbnail((150,150))
        render = ImageTk.PhotoImage(load)
        img=ttk.Label(self,image=render,background=HOMEPAGEBG)
        img.image=render
        img.place(relx=0.5, rely=0.1, anchor=tk.N)
        button_style=ttk.Style()
        button_style.theme_use('alt')
        button_style.configure('TButton', background = HOMEPAGEBG, foreground = 'white', width = 40,borderwidth=1, focusthickness=3, focuscolor='none',font=LARGE_FONT)
        button_sonnet=ttk.Button(self,text="Sonnet",style='TButton',command=lambda: self.select_sonnet_file(controller))
        button_sonnet.place(relx=0.5, rely=0.4, anchor=tk.N)
        button = ttk.Button(self, text="RF Measurements",style='TButton',
                            command=lambda: self.select_folder(controller))
        button.place(relx=0.5, rely=0.5, anchor="n")

        button_compensation=ttk.Button(self,text="DC Measurements",style='TButton',command=lambda: self.select_compensation(controller))
        button_compensation.place(relx=0.5, rely=0.6, anchor=tk.N)



class Workspace(Windows):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        self.informationchart_list=[]
        self.dataframe_list=[]
        self.folder=self.select_folder()
        self.parameters=self.initialize_parameters()
        #create the title and the back home button
        self.title = tk.Label(self, text=self.folder, font=LARGE_FONT)
        self.title.pack(side='top',fill='x',pady=10, padx=10)

        #create the back to home button
        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: self.controller.show_frame(StartPage))
        button1.pack(fill='x',pady=10, padx=10)

        self.leftframe=tk.Frame(self,width=SIZE_X-200)
        self.rightframe=tk.Frame(self,width=200)
        self.leftframe.pack(side='left',fill='both',expand=True)
        self.rightframe.pack(side='right',fill='both',expand=False)
        
        #create the figure 
        self.f=Figure(figsize=(5,5),dpi=100)
        self.a=self.f.add_subplot(111)
        self.cbar=None
        self.sm=None

        self.canvas=FigureCanvasTkAgg(self.f,self.leftframe)
        self.load_data()
        self.plot()

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, self.leftframe)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #create the canvas for the buttons
        self.controlcanvas=ControlCanvas(self.rightframe)

        #create the button
        xsep=260
        ysep=100
        self.controlcanvas.add_object(SweepFile)
        self.controlcanvas.add_object(SweepButtons,x=xsep)
        self.controlcanvas.add_object(Shift,x=-xsep,y=ysep)
        self.controlcanvas.add_object(Colour,x=xsep)
        self.controlcanvas.add_object(Cbar,x=-xsep,y=ysep)
        self.controlcanvas.add_object(CbarSweep,x=xsep)
        self.controlcanvas.add_object(Fit,x=-xsep,y=ysep)
        self.controlcanvas.add_object(GuessDelay,x=xsep)
        self.controlcanvas.add_object(PlotParameters,x=-xsep,y=ysep)
        self.controlcanvas.add_object(PlotY,x=xsep)
        self.controlcanvas.add_object(Baseline,x=-xsep,y=ysep)
        self.controlcanvas.add_object(BaselineSweep,x=xsep)
        self.controlcanvas.add_object(Smooth,x=-xsep,y=ysep)
        self.controlcanvas.add_object(ColorPlotButton,x=xsep)
        self.controlcanvas.pack(side='top',fill='both',expand=True)

        
        self.dataframe_list.append(SweepsDataframe(self))
        self.dataframe_list.append(NumberDataframe(self))

        for i in self.dataframe_list:
            self.informationchart_list.append(InformationChart(self.rightframe,i))

        for i in self.informationchart_list:
            i.treeview.pack(side='top',fill='x',expand=False)

    def initialize_parameters(self):
        filename="initial_parameters.txt"
        dicparameters={}
        with open(filename,"r") as f:
            lines=f.readlines()
            for line in lines:
                line=line.split("")
                if line[1]=="None":
                    dicparameters[line[0]]=""
                else:
                    dicparameters[line[0]]=line[1]
        return dicparameters

    def load_data(self,reset=True):
        self.Data=edf.Data(self.folder,verbose=True)
        file=int(self.parameters["file"])
        self.temp=self.Data.temp[file]
        self.power=self.Data.power[file]
        self.bandwidth=self.Data.bandwidth[file]
        self.freq=self.Data.freq[file]
        self.bx=self.Data.bx[file]
        self.by=self.Data.by[file]
        self.bz=self.Data.bz[file]
        self.amplitude_DB=self.Data.S21_DB[file]
        self.phase=self.Data.phase[file]
        self.nsimus=self.Data.number_of_simus[file]
        self.npoints=self.Data.number_of_points[file]
        self.nfiles=self.Data.number_of_files
        self.amplitude=self.Data.S21[file]
        self.amplitude_complex=self.Data.z[file]
        if reset:
            self.parameters["sweep_ini"]=0
            self.parameters["sweep_end"]=-1
            self.parameters["sweep_step"]=1
    def load_baseline(self):
        baseline_folder=self.parameters["baseline_folder"]
        baseline_sweep=[int(self.parameters["baseline_file"]),int(self.parameters["baseline_sweep"]),float(self.parameters["baseline_shift"])]
        if baseline_folder!="":
            self.Baseline=edf.Data(baseline_folder,verbose=True)
            self.Baseline_amplitude_DB=self.Baseline.S21_DB[baseline_sweep[0]][baseline_sweep[1]]
            self.Baseline_phase=self.Baseline.phase[baseline_sweep[0]][baseline_sweep[1]]

        else:
            self.Baseline_amplitude_DB=np.zeros(self.freq[0].shape)
            self.Baseline_phase=np.zeros(self.freq[0].shape)

        self.amplitude_DB=np.array([self.amplitude_DB[i]-self.Baseline_amplitude_DB+baseline_sweep[2] for i in range(len(self.amplitude_DB))])
        self.phase=np.array([self.phase[i]-self.Baseline_phase for i in range(len(self.phase))])
        self.amplitude=np.power(10,self.amplitude_DB/20)
        self.amplitude_complex=self.amplitude*np.exp(1j*self.phase)
    def smooth_data(self):
        smoothlist=int(self.parameters["smooth"])
        self.amplitude_DB=np.array([smoothfunc(self.amplitude_DB[i],smoothlist) for i in range(len(self.amplitude_DB))])
        self.phase=np.array([smoothfunc(self.phase[i],smoothlist) for i in range(len(self.phase))])
        self.amplitude=np.power(10,self.amplitude_DB/20)
        self.amplitude_complex=self.amplitude*np.exp(1j*self.phase)

    def plot(self):

        xlabel=self.parameters["xlabel"]
        xlabel_fontsize=float(self.parameters["xlabel_fontsize"])
        ylabel_fontsize=float(self.parameters["ylabel_fontsize"])
        title=self.parameters["title"]
        title_fontsize=float(self.parameters["title_fontsize"])
        linewidth=float(self.parameters["linewidth"])
        markersize=float(self.parameters["markersize"])
        linestyle=self.parameters["linestyle"]
        ticksin=bool(self.parameters["ticks_in"])
        sweep_list=[int(self.parameters["sweep_ini"]),int(self.parameters["sweep_end"]),int(self.parameters["sweep_step"])]
        colorbar_bool=bool(self.parameters["colorbar_bool"])
        colorbar_fontsize=float(self.parameters["colorbar_fontsize"])
        ticks_fontsize=float(self.parameters["ticks_fontsize"])
        grid_bool=bool(self.parameters["grid_bool"])

        if self.parameters["xticks_ini"]=="None":
            xticks=None
        else:
            xticks=np.linspace(float(self.parameters["xticks_ini"]),float(self.parameters["xticks_end"]),int(self.parameters["xticks_nintervals"]))
        if self.parameters["yticks_ini"]=="None":
            yticks=None
        else:
            yticks=np.linspace(float(self.parameters["yticks_ini"]),float(self.parameters["yticks_end"]),int(self.parameters["yticks_nintervals"]))

        cmap=matplotlib.pyplot.get_cmap(self.parameters["colormap"])
    
        if self.parameters["xmin"]!="None" and self.parameters["xmax"]!="None" and self.parameters["ymin"]!="None" and self.parameters["ymax"]!="None":
            xmin,xmax=self.a.get_xlim()
            ymin,ymax=self.a.get_ylim()
            self.parameters["xmin"]=xmin
            self.parameters["xmax"]=xmax
            self.parameters["ymin"]=ymin
            self.parameters["ymax"]=ymax

        self.a.clear()
        if self.parameters["yplot"]=="S21":
            self.yplot=self.amplitude
            self.parameters["ylabel"]="$\mathrm{S}_{21}$"
        elif self.parameters["yplot"]=="S21dB":
            self.yplot=self.amplitude_DB
            self.parameters["ylabel"]="$\mathrm{S}_{21}$ $\mathrm{(dB)}$"
        elif self.parameters["yplot"]=="Phase":
            self.yplot=self.phase
            self.parameters["ylabel"]="$\mathrm{Phase}$ $\mathrm{(rad)}$"
        if self.cbar==None:
            self.cbar.remove()
        ylabel=self.parameters["ylabel"]        

        if sweep_list[1]<0:
            sweep_list[1]=len(self.Data.freq[file[0]])+sweep_list[1]+1
    
        if self.parameters["colorbar_sweep"]=="T":
            if isinstance(self.temp,np.ndarray):
                first_value=self.temp[sweep_list[0]][0]
                last_value=self.temp[sweep_list[1]-1][0]
                self.parameters["colorbar_title"]="$\mathrm{T} \mathrm{(K)}$"
                self.itvector=self.temp
            else:
                first_value=0
                last_value=0
        elif self.parameters["colorbar_sweep"]=="P":
            if isinstance(self.power,np.ndarray):
                first_value=self.power[sweep_list[0]][0]
                last_value=self.power[sweep_list[1]-1][0]
                self.parameters["colorbar_title"]="$\mathrm{P} \mathrm{(dBm)}$"
                self.itvector=self.power
            else:
                first_value=0
                last_value=0
        elif self.parameters["colorbar_sweep"]=="B":
            if isinstance(self.bandwidth,np.ndarray):
                first_value=self.bandwidth[sweep_list[0]][0]
                last_value=self.bandwidth[sweep_list[1]-1][0]
                self.parameters["colorbar_title"]="$\mathrm{B} \mathrm{(Hz)}$"
                self.itvector=self.bandwidth
            else:
                first_value=0
                last_value=0
        elif self.parameters["colorbar_sweep"]=="Bx":
            if isinstance(self.bx,np.ndarray):
                first_value=self.bx[sweep_list[0]][0]
                last_value=self.bx[sweep_list[1]-1][0]
                self.parameters["colorbar_title"]="$\mathrm{B}_\mathrm{x}$ $\mathrm{(T)}$"
                self.itvector=self.bx
            else:
                first_value=0
                last_value=0
        elif self.parameters["colorbar_sweep"]=="By":
            if isinstance(self.by,np.ndarray):
                first_value=self.by[sweep_list[0]][0]
                last_value=self.by[sweep_list[1]-1][0]
                self.parameters["colorbar_title"]="$\mathrm{B}_\mathrm{y}$ $\mathrm{(T)}$"
                self.itvector=self.by
            else:
                first_value=0
                last_value=0
        elif self.parameters["colorbar_sweep"]=="Bz":
            if isinstance(self.bz,np.ndarray):
                first_value=self.bz[sweep_list[0]][0]
                last_value=self.bz[sweep_list[1]-1][0]
                self.parameters["colorbar_title"]="$\mathrm{B}_\mathrm{z}$ $\mathrm{(T)}$"
                self.itvector=self.bz
            else:
                first_value=0
                last_value=0
        colorbar_title=self.parameters["colorbar_title"]

        for j in range(sweep_list[0],sweep_list[1],sweep_list[2]):
            if last_value==first_value:
                self.a.plot(self.freq[j]/1e9, self.yplot[j]+shift*j,color=cmap(j/sweep_list[1]),linewidth=linewidth,linestyle=linestyle,markersize=markersize)
            else:
                self.a.plot(self.freq[j]/1e9, self.yplot[j]+shift*j,color=cmap((self.itvector[j][0]-first_value)/(last_value-first_value)),linewidth=linewidth,linestyle=linestyle,markersize=markersize)
        
        self.sm = matplotlib.pyplot.cm.ScalarMappable(cmap=cmap, norm=matplotlib.pyplot.Normalize(vmin=first_value, vmax=last_value))
        if colorbar_bool:
            if last_value!=first_value:
                self.cbar=matplotlib.pyplot.colorbar(self.sm,ticks=np.round(np.linspace(first_value,last_value,5),3),cax=self.f.add_axes([0.93, 0.15, 0.02, 0.7]))
            else:
                self.cbar=None
        else:
            self.cbar=None
        #put latex labels 
        self.a.set_xlabel(xlabel,fontsize=xlabel_fontsize)
        self.a.set_ylabel(ylabel,fontsize=ylabel_fontsize)
        self.a.set_title(title,fontsize=title_fontsize)
        #add plotlabels[3] as a label for the colorbar
        if self.cbar!=None:
            self.cbar.ax.set_title(colorbar_title,fontsize=colorbar_fontsize)
            self.cbar.ax.tick_params(labelsize=ticks_fontsize)
        #put the grid
        self.a.grid(grid_bool)
        if isinstance(xticks,type(None)):
            pass
        else:
            self.a.set_xticks(xticks)
        if isinstance(yticks,type(None)):
            pass
        else:
            self.a.set_yticks(yticks)
        self.a.tick_params(axis='both', labelsize=ticks_fontsize)        
        if ticksin:
            self.a.tick_params(direction='in')
        else:
            self.a.tick_params(direction='out')
        self.canvas.draw()
        for i in self.informationchart_list:
            i.update()
        if self.parameters["xmin"]!="None" and self.parameters["xmax"]!="None" and self.parameters["ymin"]!="None" and self.parameters["ymax"]!="None":
            self.a.set_xlim([float(self.parameters["xmin"]),float(self.parameters["xmax"])])
            self.a.set_ylim([float(self.parameters["ymin"]),float(self.parameters["ymax"])])


        
        
    def fit(self):
        sweep_list=[int(self.parameters["sweep_ini"]),int(self.parameters["sweep_end"]),int(self.parameters["sweep_step"])]

        self.temp_fit_list=[]
        self.power_fit_list=[]
        self.fr_fit_list=[]
        self.frmin_fit_list=[]
        self.Qi_fit_list=[]
        self.Qc_fit_list=[]
        self.fr_err_fit_list=[]
        self.Qi_err_fit_list=[]
        self.Qc_err_fit_list=[]
        number_of_fits=0
        self.xmin_list=[]
        self.xmax_list=[]
        guessdelay=bool(self.parameters["guessdelay"])
        for i in range(sweep_list[0],sweep_list[1],sweep_list[2]):
            xmin,xmax=self.a.get_xlim()
            cond=np.logical_and(self.freq[i]>xmin*1e9,self.freq[i]<xmax*1e9)
            self.xmin_list.append(xmin*1e9)
            self.xmax_list.append(xmax*1e9)
            freq_crop=self.freq[i][cond]
            amplitude_complex_crop=self.amplitude_complex[i][cond]
            port1=circuit.notch_port(freq_crop,amplitude_complex_crop)
            try:
                port1.autofit(guessdelay=guessdelay)
                Qi=port1.fitresults['Qi_dia_corr']
                Qi_err=port1.fitresults['Qi_dia_corr_err']
                Qc=port1.fitresults['absQc']
                Qc_err=port1.fitresults['absQc_err']
                fr=port1.fitresults['fr']
                fr_err=port1.fitresults['fr_err']

                self.Qi_fit_list.append(Qi)
                self.Qc_fit_list.append(Qc)
                self.fr_fit_list.append(fr)
                self.Qi_err_fit_list.append(Qi_err)
                self.Qc_err_fit_list.append(Qc_err)
                self.fr_err_fit_list.append(fr_err)
                number_of_fits+=1
            except:
                self.Qi_fit_list.append(np.nan)
                self.Qc_fit_list.append(np.nan)
                self.fr_fit_list.append(np.nan)
                self.Qi_err_fit_list.append(np.nan)
                self.Qc_err_fit_list.append(np.nan)
                self.fr_err_fit_list.append(np.nan)
            frmin=freq_crop[np.argmin(np.abs(amplitude_complex_crop))]
            self.frmin_fit_list.append(frmin)
            self.temp_fit_list.append(self.temp[i][0])
            self.power_fit_list.append(self.power[i][0])
        #Open a new window
        self.fitWindow=fitWindow(self,number_of_fits)
        self.fitWindow.mainloop()

    def customize_plot(self):
        self.customizePlotWindow=plotWindow(self)
        self.customizePlotWindow.mainloop()
    def color_plot(self):
        self.colorPlotWindow=ColorPlot(self)
        self.colorPlotWindow.mainloop()

class Compensation(Windows):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller=controller
        self.parent=parent
        self.title=tk.Label(self,text="Compensation",font=LARGE_FONT,bg=HOMEPAGEBG,fg="white")
        self.title.pack(side='top',fill='x',pady=10, padx=10)

        self.load_data()
        self.find_min()
        self.leftframe=tk.Frame(self,bg=HOMEPAGEBG)
        self.leftframe.pack(side='left',fill='y',expand=True)
        self.rightframe=tk.Frame(self,bg=HOMEPAGEBG)
        self.rightframe.pack(side='left',fill='y',expand=True)
        self.fig_main,self.ax_main=self.plot()
        self.fig_fit,self.ax_fit=self.plotfit()
        self.canvas_main=FigureCanvasTkAgg(self.fig_main,self.leftframe)
        self.canvas_main.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas_fit=FigureCanvasTkAgg(self.fig_fit,self.rightframe)
        self.canvas_fit.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar_main = NavigationToolbar2Tk(self.canvas_main, self.leftframe)
        self.toolbar_main.update()
        self.canvas_main._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar_fit = NavigationToolbar2Tk(self.canvas_fit, self.rightframe)
        self.toolbar_fit.update()
        self.canvas_fit._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def load_data(self):
        global compensation_file
        Data=edf.Data(compensation_file,data_type="Compensation")
        self.temp=Data.temp
        self.r=Data.r
        self.bx=Data.bx
        self.by=Data.by
        self.bz=Data.bz
        self.xmin_list=[]
        self.ymin_list=[]
        if isinstance(self.bx,type(None)):
            self.bfield=self.bz
        else:
            self.bfield=self.bx

    def find_min(self):
        global window_size
        for i in range(0,len(self.by),2):
                xmin_fs,ymin_fs=find_min(self.by[i,:],self.r[i,:],window_size=window_size[0])
                xmin_bs,ymin_bs=find_min(self.by[i+1,:],self.r[i+1,:],window_size=window_size[0])
                self.xmin_list.append((xmin_fs+xmin_bs)/2)
                self.ymin_list.append((ymin_fs+ymin_bs)/2)
    def plot(self):
        global compensationcolormap
        fig,ax=matplotlib.pyplot.subplots(figsize=(15,5),dpi=100)
        cmap=matplotlib.pyplot.get_cmap(compensationcolormap[0])
        for i in range(len(self.by)):
            ax.plot(self.by[i,:],self.r[i,:] ,color=cmap(i/len(self.by)))
            if i%2==0:
                ax.plot(self.xmin_list[i//2],self.ymin_list[i//2],"o",color=cmap(i/len(self.by)))
        ax.set_xlabel("$\mathrm{B_y} \mathrm{(T)}$")
        ax.set_ylabel("$\mathrm{R} (\Omega)$")
        ax.set_title("$\mathrm{Compensation}$")
        return fig,ax

    def plotfit(self):
        fig,ax=matplotlib.pyplot.subplots(figsize=(15,5),dpi=100)
        fig.subplots_adjust(left=0.2)
        xplot=self.bfield[::2,0]
        yplot=self.xmin_list
        ax.plot(xplot,yplot,'-o',label="Data")
        fit=np.polyfit(xplot,yplot,1)
        ax.plot(xplot,fit[0]*xplot+fit[1],"--",label="Fit. \nSlope="+str(fit[0])+"\nIntercept="+str(fit[1])+r" $\mathrm{T}$")
        if isinstance(self.bx,type(None)):
            ax.set_xlabel("$\mathrm{B_z} \mathrm{(T)}$")
        else:
            ax.set_xlabel("$\mathrm{B_x} \mathrm{(T)}$")
        ax.set_ylabel("$\mathrm{B_y} \mathrm{(T)}$")
        ax.legend()
        return fig,ax

app = MainContainer()
app.mainloop()
