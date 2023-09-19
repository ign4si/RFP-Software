
import matplotlib.animation as animation
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
from matplotlib.widgets import Cursor, Slider, Button
matplotlib.rcParams['text.usetex'] = True   #Change to false if u dont have latex <3
import Sliders 
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
ylabel_fitwindow=["$\mathrm{f}_\mathrm{r}$","$\mathrm{Q}_\mathrm{i}$","$\mathrm{Q}_\mathrm{c}$"]
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

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        global application_path
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="tkinterstuff\logo.ico")
        tk.Tk.wm_title(self, "RFP")
        tk.Tk.wm_geometry(self, self.geometry())
        #change the background color
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

        #make it fullscreen
        self.winfo_screenwidth()
        self.winfo_screenheight()
        
        

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
            
            


            


class Windows(tk.Frame):
    def showImg(self, imagedir):
        load = Image.open(imagedir)
        load.thumbnail((500, 400))
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = ttk.Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

    def select_folder(self,controller):
        global folder

        folder = tk.filedialog.askdirectory()

        tk.messagebox.showinfo(
            title='Selected Folder',
            message=folder
        )
        frame = Workspace(controller.container, controller)
        controller.frames[Workspace] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        
        controller.show_frame(Workspace)
    
    def clear(self):
        for widgets in self.winfo_children():
            widgets.destroy()
    
    def select_sonnet_file(self,controller):
        global sonnet_file

        sonnet_file = tk.filedialog.askopenfilename()

        tk.messagebox.showinfo(
            title='Selected File',
            message=sonnet_file
        )
        frame = Sonnet(controller.container, controller)
        controller.frames[Sonnet] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        controller.show_frame(Sonnet)
    def select_compensation(self,controller):
        global compensation_file

        compensation_file = tk.filedialog.askopenfilename()

        tk.messagebox.showinfo(
            title='Selected File',
            message=compensation_file
        )
        frame = Compensation(controller.container, controller)
        controller.frames[Compensation] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        controller.show_frame(Compensation)

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
        global folder
        global sweep_list
        global file
        tk.Frame.__init__(self, parent)
        self.controller=controller
        self.informationchart_list=[]
        self.dataframe_list=[]
        #create the title and the back home button
        self.title = tk.Label(self, text=folder, font=LARGE_FONT)
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
        self.load_baseline()
        self.smooth_data()
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



    def load_data(self,reset=True):
        global sweep_list
        self.Data=edf.Data(folder,verbose=True)
        self.temp=self.Data.temp[file[0]]
        self.power=self.Data.power[file[0]]
        self.bandwidth=self.Data.bandwidth[file[0]]
        self.freq=self.Data.freq[file[0]]
        self.real=self.Data.real[file[0]]
        self.imag=self.Data.imag[file[0]]
        self.bx=self.Data.bx[file[0]]
        self.by=self.Data.by[file[0]]
        self.bz=self.Data.bz[file[0]]
        self.amplitude_DB=self.Data.S21_DB[file[0]]
        self.phase=self.Data.phase[file[0]]
        self.nsimus=self.Data.number_of_simus[file[0]]
        self.npoints=self.Data.number_of_points[file[0]]
        self.nfiles=self.Data.number_of_files
        self.amplitude=self.Data.S21[file[0]]
        self.amplitude_complex=self.Data.z[file[0]]
        if reset:
            sweep_list=[0,-1,1]
    def load_baseline(self):
        global baseline_folder
        global baseline_sweep
        if baseline_folder[0]!="":
            self.Baseline=edf.Data(baseline_folder[0],verbose=True)
            self.Baseline_amplitude_DB=self.Baseline.S21_DB[baseline_sweep[0]][baseline_sweep[1]]
            self.Baseline_phase=self.Baseline.phase[baseline_sweep[0]][baseline_sweep[1]]

        else:
            self.Baseline_amplitude_DB=np.zeros(self.freq[0].shape)
            self.Baseline_phase=np.zeros(self.freq[0].shape)

        self.amplitude_DB=np.array([self.amplitude_DB[i]-self.Baseline_amplitude_DB+baseline_sweep[2] for i in range(len(self.amplitude_DB))])
        self.phase=np.array([self.phase[i]-self.Baseline_phase for i in range(len(self.phase))])
        self.amplitude=np.power(10,self.amplitude_DB/20)
        self.amplitude_complex=self.amplitude*np.exp(1j*self.phase)
        self.real=self.amplitude_complex.real
        self.imag=self.amplitude_complex.imag
    def smooth_data(self):
        global smoothlist
        self.amplitude_DB=np.array([smoothfunc(self.amplitude_DB[i],smoothlist[0]) for i in range(len(self.amplitude_DB))])
        self.phase=np.array([smoothfunc(self.phase[i],smoothlist[0]) for i in range(len(self.phase))])
        self.amplitude=np.power(10,self.amplitude_DB/20)
        self.amplitude_complex=self.amplitude*np.exp(1j*self.phase)
        self.real=self.amplitude_complex.real
        self.imag=self.amplitude_complex.imag

    def plot(self):
        global folder
        global sweep_list
        global file
        global shift
        global colormap
        global xlabel
        global ylabel
        global title
        global yplot
        global baseline_folder
        global baseline_sweep

        global fontsize
        global plotlabels
        global grid_bool
        global xticks
        global yticks
        global marker_size
        global linewidth
        global linestyle
        global ticksin

        cmap=matplotlib.pyplot.get_cmap(colormap[0])
        #clean the plot

        self.a.clear()
        if yplot[0]=="S21":
            self.yplot=self.amplitude
        elif yplot[0]=="S21dB":
            self.yplot=self.amplitude_DB
        elif yplot[0]=="Phase":
            self.yplot=self.phase
        if self.cbar!=None:
            self.cbar.remove()
        if sweep_list[1]<0:
            sweep_list[1]=len(self.Data.freq[file[0]])+sweep_list[1]+1
        
        if cbarsweep[0]=="T":
            if isinstance(self.temp,np.ndarray):
                first_value=self.temp[sweep_list[0]][0]
                last_value=self.temp[sweep_list[1]-1][0]
                self.itvector=self.temp
            else:
                first_value=0
                last_value=0
        elif cbarsweep[0]=="P":
            if isinstance(self.power,np.ndarray):
                first_value=self.power[sweep_list[0]][0]
                last_value=self.power[sweep_list[1]-1][0]
                self.itvector=self.power
            else:
                first_value=0
                last_value=0
        elif cbarsweep[0]=="B":
            if isinstance(self.bandwidth,np.ndarray):
                first_value=self.bandwidth[sweep_list[0]][0]
                last_value=self.bandwidth[sweep_list[1]-1][0]
                self.itvector=self.bandwidth
            else:
                first_value=0
                last_value=0
        elif cbarsweep[0]=="Bx":
            if isinstance(self.bx,np.ndarray):
                first_value=self.bx[sweep_list[0]][0]
                last_value=self.bx[sweep_list[1]-1][0]
                self.itvector=self.bx
            else:
                first_value=0
                last_value=0
        elif cbarsweep[0]=="By":
            if isinstance(self.by,np.ndarray):
                first_value=self.by[sweep_list[0]][0]
                last_value=self.by[sweep_list[1]-1][0]
                self.itvector=self.by
            else:
                first_value=0
                last_value=0
        elif cbarsweep[0]=="Bz":
            if isinstance(self.bz,np.ndarray):
                first_value=self.bz[sweep_list[0]][0]
                last_value=self.bz[sweep_list[1]-1][0]
                self.itvector=self.bz
            else:
                first_value=0
                last_value=0


        for j in range(sweep_list[0],sweep_list[1],sweep_list[2]):
            if last_value==first_value:
                self.a.plot(self.freq[j]/1e9, self.yplot[j]+shift[0]*j,color=cmap(j/sweep_list[1]),linewidth=linewidth[0],linestyle=linestyle[0],markersize=marker_size[0])
            else:
                self.a.plot(self.freq[j]/1e9, self.yplot[j]+shift[0]*j,color=cmap((self.itvector[j][0]-first_value)/(last_value-first_value)),linewidth=linewidth[0],linestyle=linestyle[0],markersize=marker_size[0])
        
        self.sm = matplotlib.pyplot.cm.ScalarMappable(cmap=cmap, norm=matplotlib.pyplot.Normalize(vmin=first_value, vmax=last_value))
        if cbarbool[0]:
            if last_value!=first_value:
                self.cbar=matplotlib.pyplot.colorbar(self.sm,ticks=np.round(np.linspace(first_value,last_value,5),3),cax=self.f.add_axes([0.93, 0.15, 0.02, 0.7]))
            else:
                self.cbar=None
        else:
            self.cbar=None
        #put latex labels 
        self.a.set_xlabel(plotlabels[0],fontsize=fontsize[0])
        self.a.set_ylabel(plotlabels[1],fontsize=fontsize[1])
        self.a.set_title(plotlabels[2],fontsize=fontsize[2])
        #add plotlabels[3] as a label for the colorbar
        if self.cbar!=None:
            self.cbar.ax.set_title(plotlabels[3],fontsize=fontsize[3])
            self.cbar.ax.tick_params(labelsize=colorplotfontsize[4])
        #put the grid
        self.a.grid(grid_bool[0])
        if isinstance(xticks[0],type(None)):
            pass
        else:
            self.a.set_xticks(xticks[0])
        if isinstance(yticks[0],type(None)):
            pass
        else:
            self.a.set_yticks(yticks[0])
        self.a.tick_params(axis='both', labelsize=fontsize[4])        
        if ticksin[0]:
            self.a.tick_params(direction='in')
        else:
            self.a.tick_params(direction='out')
        self.canvas.draw()
        for i in self.informationchart_list:
            i.update()
    def onepointfit(self,i,index_crop,axis,draw_canvas):
        global guessdelay
        global xlabel_onepointfitwindow
        global ylabel_onepointfitwindow
        global suptitle_onepointfitwindow

        xmin,xmax=axis[1].get_xlim()
        cond=np.logical_and(self.freq[i]>xmin*1e9,self.freq[i]<xmax*1e9)
        self.xmin_list[index_crop]=xmin*1e9
        self.xmax_list[index_crop]=xmax*1e9
        self.cond=cond
        freq_crop=self.freq[i][cond]
        amplitude_complex_crop=self.amplitude_complex[i][cond]
        port1=circuit.notch_port(freq_crop,amplitude_complex_crop)
        try:
            port1.autofit(guessdelay=guessdelay[0])
            Qi=port1.fitresults['Qi_dia_corr']
            Qi_err=port1.fitresults['Qi_dia_corr_err']
            Qc=port1.fitresults['absQc']
            Qc_err=port1.fitresults['absQc_err']
            fr=port1.fitresults['fr']
            fr_err=port1.fitresults['fr_err']
            self.Qi_fit_list[index_crop]=Qi
            self.Qc_fit_list[index_crop]=Qc
            self.fr_fit_list[index_crop]=fr
            self.Qi_err_fit_list[index_crop]=Qi_err
            self.Qc_err_fit_list[index_crop]=Qc_err
            self.fr_err_fit_list[index_crop]=fr_err
        except:
            pass
        self.frmin=freq_crop[np.argmin(np.abs(amplitude_complex_crop))]
        self.frmin_fit_list[index_crop]=self.frmin
        
        real_raw=self.amplitude_complex[i].real
        imag_raw=self.amplitude_complex[i].imag
        real_fit=port1.z_data_sim.real
        imag_fit=port1.z_data_sim.imag

        axis[0].clear()
        axis[1].clear()
        axis[2].clear()

        axis[0].plot(real_raw,imag_raw,color='black',label='Data')
        axis[0].plot(real_fit,imag_fit,color="red",linestyle='dashed',label='Fit')  
        axis[0].set_xlabel(xlabel_onepointfitwindow[0])
        axis[0].set_ylabel(ylabel_onepointfitwindow[0])
        axis[0].legend()
        axis[0].grid(True)

        axis[1].plot(self.freq[i]/1e9,np.abs(self.amplitude_complex[i]),color='black',label='Data')
        axis[1].plot(freq_crop/1e9,np.abs(port1.z_data_sim),color='red',linestyle='dashed',label='Fit')
        axis[1].set_xlabel(xlabel_onepointfitwindow[1])
        axis[1].set_ylabel(ylabel_onepointfitwindow[1])
        axis[1].legend()
        axis[1].grid(True)

        axis[2].plot(self.freq[i]/1e9,np.angle(self.amplitude_complex[i]),color='black',label='Data')
        axis[2].plot(freq_crop/1e9,np.angle(port1.z_data_sim),color='red',linestyle='dashed',label='Fit')
        axis[2].set_xlabel(xlabel_onepointfitwindow[2])
        axis[2].set_ylabel(ylabel_onepointfitwindow[2])
        axis[2].legend()
        axis[2].grid(True)


        draw_canvas.draw()
        try:
            self.fitWindow.update_plot()
        except:
            pass
        return port1

        
        
    def fit(self):
        global sweep_list
        global file
        global shift
        global colormap
        global cbarbool
        global cbarsweep
        global guessdelay
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
        for i in range(sweep_list[0],sweep_list[1],sweep_list[2]):
            xmin,xmax=self.a.get_xlim()
            cond=np.logical_and(self.freq[i]>xmin*1e9,self.freq[i]<xmax*1e9)
            self.xmin_list.append(xmin*1e9)
            self.xmax_list.append(xmax*1e9)
            freq_crop=self.freq[i][cond]
            amplitude_complex_crop=self.amplitude_complex[i][cond]
            port1=circuit.notch_port(freq_crop,amplitude_complex_crop)
            try:
                port1.autofit(guessdelay=guessdelay[0])
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
class Sonnet(Windows):
    def __init__(self, root,controller):
        global sonnet_file
        global i
        global init_Qc
        global init_Qi
        global init_fr
        global init_phi0
        global deltaphi
        global deltafr
        global deltaQc
        global deltaQi
        global f
        global amp
        global angle
        tk.Frame.__init__(self, root)
        foldername=sonnet_file.split("/")[-1][:-4]
        datas,params=Sliders.read_data_2(sonnet_file)
        self.controller=controller
        i=0
        print(datas[i].shape)
        f_ = datas[i][:,0]
        amp_ = np.exp(2*datas[i][:,1]/10)
        angle_ = datas[i][:,2]

        init_phi0= -50
        init_Qc = 100e3
        init_Qi =  0.1e6
        init_fr = f_[np.argmin(amp_)] #Estimation of the resonante frequency 

        deltaphi=10
        deltafr=0.001
        deltaQc=40e3
        deltaQi=0.05e6
        f=[]
        amp=[]
        angle=[]
        
        for k in range(0, len(f_)): 
            if init_fr-0.001<f_[k] and f_[k]<init_fr+0.001 : 
                f.append(f_[k])
                amp.append(amp_[k])
                angle.append(angle_[k])
        f=np.array(f)
        amp=np.array(amp)
        angle=np.array(angle)

        fig, ax= matplotlib.pyplot.subplots(2, 1,sharex=True, figsize=(9, 8))
        ax=ax.ravel()
        amplitud_, =ax[0].plot(f, amp,'-o',markersize=1)
        fase_, =ax[1].plot(f, angle,'-o',markersize=1)
        line1, = ax[0].plot(f, Sliders.amplitude(f,init_fr,init_Qc,init_Qi), lw=2)
        line2, = ax[1].plot(f, Sliders.phase(f,init_fr,init_Qc,init_Qi,init_phi0), lw=2)
        ax[0].set_xlim([f[0],f[-1]])
        matplotlib.pyplot.subplots_adjust(left=0.25, bottom=0.25)

        sliders=[]
        axfr = matplotlib.pyplot.axes([0.25, 0.1, 0.65, 0.03])
        fr_slider = Slider(
            ax=axfr,
            label='fr [Hz]',
            valmin=init_fr-deltafr,
            valmax=init_fr+deltafr,
            valinit=init_fr,
        )
        sliders.append(fr_slider)
        # Make a vertically oriented slider to control phi
        axphi = matplotlib.pyplot.axes([0.1, 0.25, 0.0225, 0.63])
        phi_slider = Slider(
            ax=axphi,
            label="Phi0 [rad]",
            valmin=init_phi0-deltaphi,
            valmax=init_phi0+deltaphi,
            valinit=init_phi0,
            orientation="vertical"
        )
        sliders.append(phi_slider)
        # Make a horizontal slider to control qc.
        axQc = matplotlib.pyplot.axes([0.25, 0.05, 0.65, 0.03])
        Qc_slider = Slider(
            ax=axQc,
            label='Qc',
            valmin=init_Qc-deltaQc,
            valmax=init_Qc+deltaQc,
            valinit=init_Qc,
        )
        sliders.append(Qc_slider)

        # Make a vertically oriented slider to control Qi
        axQi = matplotlib.pyplot.axes([0.05, 0.25, 0.0225, 0.63])
        Qi_slider = Slider(
            ax=axQi,
            label="Qi",
            valmin=init_Qi-deltaQi,
            valmax=init_Qi+deltaQi,
            valinit=init_Qi,
            orientation="vertical"
        )

        sliders.append(Qi_slider)
        def update(val):
            line1.set_ydata(Sliders.amplitude(f, sliders[0].val,sliders[2].val,sliders[3].val))
            line2.set_ydata(Sliders.phase(f,sliders[0].val,sliders[2].val,sliders[3].val,sliders[1].val))
            fig.canvas.draw_idle()

        fr_slider.on_changed(update)
        phi_slider.on_changed(update)
        Qc_slider.on_changed(update)
        Qi_slider.on_changed(update)
        resetax = matplotlib.pyplot.axes([0.05, 0.075, 0.1, 0.04])
        parametsax = matplotlib.pyplot.axes([0.05, 0.025, 0.1, 0.04])
        fitax = matplotlib.pyplot.axes([0.05, 0.125, 0.1, 0.04])
        startaigan = matplotlib.pyplot.axes([0.05, 0.175, 0.1, 0.04])
        forwardax = matplotlib.pyplot.axes([0.9, 0.95, 0.04, 0.04])
        backwardax = matplotlib.pyplot.axes([0.1, 0.95, 0.04, 0.04])
        fitandgoax=matplotlib.pyplot.axes([0.9, 0.85, 0.04, 0.04])

        button = Button(resetax, 'Reset', hovercolor='0.975')
        button2 = Button(parametsax, 'Get Parameters', hovercolor='0.975')
        button3 = Button(fitax, 'Fit', hovercolor='0.975')
        button4 = Button(startaigan, 'StartAgain', hovercolor='0.975')
        button5 = Button(forwardax, 'Go next', hovercolor='0.975')
        button6 = Button(backwardax, 'Go back', hovercolor='0.975')
        button7 = Button(fitandgoax, 'Fit and Go', hovercolor='0.975')
        def reset(event):
            sliders[0].reset()
            sliders[1].reset()
            sliders[2].reset()
            sliders[3].reset()
        def getpars(event):
            global i 
            name=''
            if params!=[]:
                for j in list(params[i].values()):
                    name=name+str(j)+","
                name=name[:-1]
            else:
                name='SonnetSimulation'
            filename=foldername+name+".txt"
            #create a folder named "datos" in the same directory as the script
            if not os.path.exists(foldername):
                os.makedirs(foldername)
            with open(foldername+"/"+filename,'w') as o:
                print('fr',sliders[0].val,file=o)
                print('phi',sliders[1].val,file=o)
                print('Qc',sliders[2].val,file=o)
                print('Qi',sliders[3].val,file=o)                            
        def fit(event):
            global f
            global amp
            global angle
            parames = Parameters()
            parames.add('fr', value=sliders[0].val)
            parames.add('Qc', value=sliders[2].val)
            parames.add('Qi', value=sliders[3].val)
            parames.add('phi0', value=sliders[1].val)
            out = minimize(Sliders.fit_function, parames, kws={"f": f, "dat1":amp, "dat2": angle})
            a_=out.params['fr'].value
            b_ = out.params['Qc'].value
            c_= out.params['Qi'].value
            d_= out.params['phi0'].value
            line1.set_ydata(Sliders.amplitude(f, a_,b_,c_))
            line2.set_ydata(Sliders.phase(f,a_,b_,c_,d_))
            axfr.cla() #Clear the axis
            sliders[0].__init__(axfr, 'fr[Hz]',valmin=a_-deltafr, valmax=a_+deltafr, valinit=a_,)
            axphi.cla()
            sliders[1].__init__(ax=axphi,label="Phi0 [rad]",valmin=d_-deltaphi,valmax=d_+deltaphi,valinit=d_,orientation="vertical")
            axQc.cla()
            sliders[2].__init__(ax=axQc,label='Qc',valmin=b_-deltaQc,valmax=b_+deltaQc,valinit=b_)
            axQi.cla()
            sliders[3].__init__(ax=axQi,label='Qi',valmin=c_-deltaQi,valmax=c_+deltaQi,valinit=c_,orientation="vertical")
            sliders[0].on_changed(update)
            sliders[1].on_changed(update)
            sliders[2].on_changed(update)
            sliders[3].on_changed(update)
            fig.canvas.draw_idle()
        def start(event):
            global f
            global init_fr
            global init_Qc
            global init_Qi
            global init_phi0
            
            a_=init_fr
            b_ =init_Qc
            c_=init_Qi
            d_=init_phi0
            
            line1.set_ydata(Sliders.amplitude(f, a_,b_,c_))
            line2.set_ydata(Sliders.phase(f,a_,b_,c_,d_))
            
            axfr.cla() #Clear the axis
            sliders[0].__init__(axfr, 'fr[Hz]',valmin=a_-deltafr, valmax=a_+deltafr, valinit=a_,)
            axphi.cla()
            sliders[1].__init__(ax=axphi,label="Phi0 [rad]",valmin=d_-deltaphi,valmax=d_+deltaphi,valinit=d_,orientation="vertical")
            axQc.cla()
            sliders[2].__init__(ax=axQc,label='Qc',valmin=b_-deltaQc,valmax=b_+deltaQc,valinit=b_)
            axQi.cla()
            sliders[3].__init__(ax=axQi,label='Qi',valmin=c_-deltaQi,valmax=c_+deltaQi,valinit=c_,orientation="vertical")
            sliders[0].on_changed(update)
            sliders[1].on_changed(update)
            sliders[2].on_changed(update)
            sliders[3].on_changed(update)

            fig.canvas.draw_idle()
        def forward(event):
            global i
            global f
            global amp
            global angle
            global init_fr
            global init_Qc
            global init_Qi
            global init_phi0
            if(i<len(params)-1):
                i+=1    
            f_ = datas[i][:,0]
            amp_ = np.exp(2*datas[i][:,1]/10)
            angle_ = datas[i][:,2]
            
            title=""
            if params!=[]:
                for llave in list(params[i].keys()):
                    title+=llave+": "+str(params[i][llave])+" "
            fig.suptitle(title, fontsize=16)

            
            a_=f_[np.argmin(np.exp(2*datas[i][:,1]/10))]
            init_fr = a_
            b_=init_Qc
            c_=init_Qi
            d_=init_phi0

            f=[]
            amp=[]
            angle=[]

            for k in range(0, len(f_)): 
                if init_fr-0.001<f_[k] and f_[k]<init_fr+0.001 : 
                    f.append(f_[k])
                    amp.append(amp_[k])
                    angle.append(angle_[k])
            f=np.array(f)
            amp=np.array(amp)
            angle=np.array(angle)
            
            ax[0].set_xlim([f[0],f[-1]])
            amplitud_.set_xdata(f)
            amplitud_.set_ydata(amp)
            fase_.set_xdata(f)
            fase_.set_ydata(angle)
            line1.set_xdata(f)
            line2.set_xdata(f)
            line1.set_ydata(Sliders.amplitude(f, a_,b_,c_))
            line2.set_ydata(Sliders.phase(f,a_,b_,c_,d_))
            
            axfr.cla() #Clear the axis
            sliders[0].__init__(axfr, 'fr[Hz]',valmin=a_-deltafr, valmax=a_+deltafr, valinit=a_,)
            axphi.cla()
            sliders[1].__init__(axphi,label="Phi0 [rad]",valmin=d_-deltaphi,valmax=d_+deltaphi,valinit=d_,orientation="vertical")
            axQc.cla()
            sliders[2].__init__(axQc,label='Qc',valmin=b_-deltaQc,valmax=b_+deltaQc,valinit=b_)
            axQi.cla()
            sliders[3].__init__(axQi,label='Qi',valmin=c_-deltaQi,valmax=c_+deltaQi,valinit=c_,orientation="vertical")
            sliders[0].on_changed(update)
            sliders[1].on_changed(update)
            sliders[2].on_changed(update)
            sliders[3].on_changed(update)

            fig.canvas.draw_idle()
        def backward(event): 
            global i
            global f
            global amp
            global angle
            global init_fr
            global init_Qc
            global init_Qi
            global init_phi0
            if(i>0):
                i-=1
            
            f_ = datas[i][:,0]
            amp_ = np.exp(2*datas[i][:,1]/10)
            angle_ = datas[i][:,2]
            
            a_=f_[np.argmin(np.exp(2*datas[i][:,1]/10))]
            init_fr = a_   
            b_=init_Qc
            c_=init_Qi
            d_=init_phi0

            f=[]
            amp=[]
            angle=[]
            title=""
            if params!=[]:
                for llave in list(params[i].keys()):
                    title+=llave+": "+str(params[i][llave])+" "
            fig.suptitle(title, fontsize=16)
            for k in range(0, len(f_)): 
                if init_fr-0.001<f_[k] and f_[k]<init_fr+0.001 : 
                    f.append(f_[k])
                    amp.append(amp_[k])
                    angle.append(angle_[k])
            f=np.array(f)
            amp=np.array(amp)
            angle=np.array(angle)
            
            ax[0].set_xlim([f[0],f[-1]])
            amplitud_.set_xdata(f)
            amplitud_.set_ydata(amp)
            fase_.set_xdata(f)
            fase_.set_ydata(angle)
            line1.set_xdata(f)
            line2.set_xdata(f)
            line1.set_ydata(Sliders.amplitude(f, a_,b_,c_))
            line2.set_ydata(Sliders.phase(f,a_,b_,c_,d_))
            
            axfr.cla() #Clear the axis
            sliders[0].__init__(axfr, 'fr[Hz]',valmin=a_-deltafr, valmax=a_+deltafr, valinit=a_,)
            axphi.cla()
            sliders[1].__init__(axphi,label="Phi0 [rad]",valmin=d_-deltaphi,valmax=d_+deltaphi,valinit=d_,orientation="vertical")
            axQc.cla()
            sliders[2].__init__(axQc,label='Qc',valmin=b_-deltaQc,valmax=b_+deltaQc,valinit=b_)
            axQi.cla()
            sliders[3].__init__(axQi,label='Qi',valmin=c_-deltaQi,valmax=c_+deltaQi,valinit=c_,orientation="vertical")
            sliders[0].on_changed(update)
            sliders[1].on_changed(update)
            sliders[2].on_changed(update)
            sliders[3].on_changed(update)

            fig.canvas.draw_idle()
        def fitandgo(funcs):
            global i
            def combined_func(*args, **kwargs):
                while(i<len(datas)-1):
                    for j in range(5):
                        funcs[0](*args, **kwargs)
                    funcs[1](*args, **kwargs)
                    funcs[2](*args, **kwargs)
            return combined_func
        title=""
        if params!=[]:
            for llave in list(params[i].keys()):
                title+=llave+": "+str(params[i][llave])+" "
        fig.suptitle(title, fontsize=16)

        button.on_clicked(reset)
        button2.on_clicked(getpars)
        button3.on_clicked(fit)
        button4.on_clicked(start)
        button5.on_clicked(forward)
        button6.on_clicked(backward)
        button7.on_clicked(fitandgo([fit,getpars,forward]))
        matplotlib.pyplot.show()
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
        self.ix=Data.ix
        self.iy=Data.iy
        self.ux=Data.ux
        self.uy=Data.uy
        self.r=Data.r
        self.bx=Data.bx
        self.by=Data.by
        self.bz=Data.bz
        self.time=Data.time
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
class plotWindow(tk.Toplevel):
    def __init__(self,root):
        tk.Toplevel.__init__(self,root)
        self.root=root
        self.wm_title("Plot parameters")
        self.geometry("1280x720")
        self.configure(bg=HOMEPAGEBG)
        self.controlcanvas=ControlCanvas(self)
        xsep=500
        ysep=200
        self.controlcanvas.add_object(Fontsize) #all four sizes and the last one is the size of the ticks
        self.controlcanvas.add_object(PlotLabels,x=xsep)
        self.controlcanvas.add_object(GridBool,x=-xsep,y=ysep)
        self.controlcanvas.add_object(XTicks,x=xsep)
        self.controlcanvas.add_object(YTicks,x=-xsep,y=ysep)
        self.controlcanvas.add_object(Linestyle,x=xsep)
        self.controlcanvas.add_object(Linewidth,x=-xsep,y=ysep)
        self.controlcanvas.add_object(TicksIn,x=xsep)
        self.controlcanvas.pack(side='top',fill='both',expand=True,pady=10, padx=10)
class ColorPlot(tk.Toplevel):
    def __init__(self,root):
        global sweep_list
        global colorplotlabels
        global colorplotfontsize
        global colorplotcolormap
        cmap=matplotlib.pyplot.get_cmap(colorplotcolormap[0])
        tk.Toplevel.__init__(self,root)
        self.root=root
        self.wm_title("Color plot")
        self.geometry("1280x720")
        self.configure(bg=HOMEPAGEBG)
        self.title=tk.Label(self,text="Color Plot",font=LARGE_FONT,bg=HOMEPAGEBG,fg="white")
        self.title.pack(side='top',fill='x',pady=10, padx=10)

        self.x=self.root.freq[0]
        self.y=self.root.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0]
        self.Z=self.root.yplot[sweep_list[0]:sweep_list[1]:sweep_list[2],:]
        min_value=np.min(self.Z)
        max_value=np.max(self.Z)
        self.X,self.Y=np.meshgrid(self.x/1e9,self.y)
        self.fig=matplotlib.pyplot.figure(figsize=(15,5),dpi=100)
        self.ax=self.fig.add_subplot(111)
        self.imagen=self.ax.pcolormesh(self.X,self.Y,self.Z,cmap=cmap)
        self.ax.set_xlabel(colorplotlabels[0],fontsize=colorplotfontsize[0])
        self.ax.set_ylabel(colorplotlabels[1],fontsize=colorplotfontsize[1])
        self.ax.set_title(colorplotlabels[2],fontsize=colorplotfontsize[2])
        self.cbar=matplotlib.pyplot.colorbar(self.imagen,ax=self.ax)
        self.cbar.ax.set_title(colorplotlabels[3],fontsize=colorplotfontsize[3])
        self.cbar.ax.tick_params(labelsize=colorplotfontsize[4])
        self.ax.tick_params(axis='both', which='major', labelsize=colorplotfontsize[4])
        self.canvas=FigureCanvasTkAgg(self.fig,self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.draw()
        xsep=350
        self.controlcanvas=ControlCanvas(self)
        self.controlcanvas.add_object(ColorPlotLabels)
        self.controlcanvas.add_object(ColorPlotFontsize,x=xsep)
        self.controlcanvas.add_object(ColorPlotColormap,x=xsep)
        self.controlcanvas.pack(side='top',fill='x',pady=10, padx=10)

        cursor=Cursor(self.ax, useblit=True,horizOn=True,vertOn=True,color='red', linewidth=2)
        def onclick(event):
            if self.ax.get_navigate_mode() is not None and self.ax.get_navigate_mode() != '': 
                return None
            else:
                if event.inaxes!=self.ax:
                    return None
                xevent=event.xdata
        
                index=np.argmin(np.abs(self.x/1e9-xevent))
                CutWindow(self,index)

        self.fig.canvas.mpl_connect('button_press_event', onclick)
    def update_plot(self):
        global colorplotcolormap
        global sweep_list
        global colorplotlabels
        global colorplotfontsize


        self.ax.clear()
        self.y=self.root.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0]
        cmap=matplotlib.pyplot.get_cmap(colorplotcolormap[0])
        self.Z=self.root.yplot
        min_value=np.min(self.Z)
        max_value=np.max(self.Z)
        
        self.X,self.Y=np.meshgrid(self.x/1e9,self.y)
        self.imagen=self.ax.pcolormesh(self.X,self.Y,self.Z,cmap=matplotlib.pyplot.get_cmap(colorplotcolormap[0]))
        self.ax.set_xlabel(colorplotlabels[0],fontsize=colorplotfontsize[0])
        self.ax.set_ylabel(colorplotlabels[1],fontsize=colorplotfontsize[1])
        self.ax.set_title(colorplotlabels[2],fontsize=colorplotfontsize[2])
        self.cbar.ax.set_title(colorplotlabels[3],fontsize=colorplotfontsize[3])
        self.cbar.ax.tick_params(labelsize=colorplotfontsize[4])
        self.ax.tick_params(axis='both', which='major', labelsize=colorplotfontsize[4])
        self.canvas.draw()

    
class fitWindow(tk.Toplevel):
    def __init__(self,root,number_of_fits):
        global cbarsweep
        global xlabel_fitwindow
        global ylabel_fitwindow
        global suptitle_fitwindow
        tk.Toplevel.__init__(self,root)
        self.root=root
        self.wm_title("Fit")
        self.geometry("1280x720")
        self.configure(bg=HOMEPAGEBG)
        self.title=tk.Label(self,text="Fit",font=LARGE_FONT,bg=HOMEPAGEBG,fg="white")
        self.title.pack(side='top',fill='x',pady=10, padx=10)
        #create the figure
        if number_of_fits!=1:
            self.fig,(self.ax1,self.ax2,self.ax3)=matplotlib.pyplot.subplots(1,3,figsize=(15,5),dpi=100)
            self.ax1.plot(self.root.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0],np.array(self.root.frmin_fit_list)/1e9,'o',color='black')
            self.ax2.errorbar(self.root.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0],self.root.Qi_fit_list,yerr=self.root.Qi_err_fit_list,fmt='o',color='black')
            self.ax3.errorbar(self.root.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0],self.root.Qc_fit_list,yerr=self.root.Qc_err_fit_list,fmt='o',color='black')
            self.ax1.set_xlabel(xlabel_fitwindow[0])
            self.ax1.set_ylabel(ylabel_fitwindow[0])
            self.ax2.set_xlabel(xlabel_fitwindow[0])
            self.ax2.set_ylabel(ylabel_fitwindow[1])
            self.ax3.set_xlabel(xlabel_fitwindow[0])
            self.ax3.set_ylabel(ylabel_fitwindow[2])
            self.ax1.grid(True)
            self.ax2.grid(True)
            self.ax3.grid(True)
            self.fig.tight_layout()
            self.fig.suptitle(suptitle_fitwindow[0], fontsize=16)
            self.canvas=FigureCanvasTkAgg(self.fig,self)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(self.canvas, self)
            toolbar.update()
            self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.canvas.draw()
        else:
            OnePointFitWindow(self,0,0)
        cursor1=Cursor(self.ax1, useblit=True,horizOn=True,vertOn=True,color='red', linewidth=2)
        cursor2=Cursor(self.ax2, useblit=True,horizOn=True,vertOn=True,color='red', linewidth=2)
        cursor3=Cursor(self.ax3, useblit=True,horizOn=True,vertOn=True,color='red', linewidth=2)
        def onclick(event):
            if self.ax1.get_navigate_mode() is not None and self.ax1.get_navigate_mode() != '': 
                return None
            else:
                if event.inaxes!=self.ax1 and event.inaxes!=self.ax2 and event.inaxes!=self.ax3:
                    return None
                xevent=event.xdata
                index_crop=np.argmin(np.abs(self.root.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0]-xevent))
                selected_value=self.root.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0][index_crop]
                index=np.argmin(np.abs(self.root.itvector[:,0]-selected_value))
                OnePointFitWindow(self,index,index_crop)
        
        self.controlcanvas=ControlCanvas(self)
        self.controlcanvas.add_object(FitWindowLabelsX)
        self.controlcanvas.add_object(FitWindowLabelsY,x=400)
        self.controlcanvas.add_object(FitWindowSuptitle,x=400)
        self.controlcanvas.add_object(FitWindowSave,x=400)
        self.controlcanvas.pack(side=tk.TOP, fill="x", expand=True)
        cid = self.fig.canvas.mpl_connect('button_press_event', onclick)
    def update_plot(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax1.plot(self.root.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0],np.array(self.root.frmin_fit_list)/1e9,'o',color='black')
        self.ax2.errorbar(self.root.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0],self.root.Qi_fit_list,yerr=self.root.Qi_err_fit_list,fmt='o',color='black')
        self.ax3.errorbar(self.root.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0],self.root.Qc_fit_list,yerr=self.root.Qc_err_fit_list,fmt='o',color='black')
        self.ax1.set_xlabel(xlabel_fitwindow[0])
        self.ax1.set_ylabel(ylabel_fitwindow[0])
        self.ax2.set_xlabel(xlabel_fitwindow[0])
        self.ax2.set_ylabel(ylabel_fitwindow[1])
        self.ax3.set_xlabel(xlabel_fitwindow[0])
        self.ax3.set_ylabel(ylabel_fitwindow[2])
        self.ax1.grid()
        self.ax2.grid()
        self.ax3.grid()
        self.fig.tight_layout()
        self.fig.suptitle(suptitle_fitwindow[0], fontsize=16)
        self.canvas.draw()
    def save(self):
        #ask for a folder and a filename
        filename = tk.filedialog.asksaveasfilename(title="Select file",filetypes=(("txt files","*.txt"),("all files","*.*")))
        x=self.root.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0]
        y1=self.root.frmin_fit_list
        y2=self.root.Qi_fit_list
        y3=self.root.Qc_fit_list
        y2err=self.root.Qi_err_fit_list
        y3err=self.root.Qc_err_fit_list
        with open(filename,'w') as o:
            print("x\ty1\ty2\ty2err\ty3\ty3err",file=o)
            for i in range(len(x)):
                print(str(x[i])+"\t"+str(y1[i])+"\t"+str(y2[i])+"\t"+str(y2err[i])+"\t"+str(y3[i])+"\t"+str(y3err[i]),file=o)


    
class OnePointFitWindow(tk.Toplevel):
    def __init__(self,root,index,index_crop):
        global guessdelay
        global xlabel_onepointfitwindow
        global ylabel_onepointfitwindow
        global suptitle_onepointfitwindow
        tk.Toplevel.__init__(self,root)
        self.root=root
        self.index=index
        self.index_crop=index_crop
        x=self.root.root.freq[index]
        self.x=x
        z=self.root.root.amplitude_complex[index]
        
        xmin=self.root.root.xmin_list[index_crop]
        xmax=self.root.root.xmax_list[index_crop]
        
        cond=np.logical_and(x>xmin,x<xmax)
        self.cond=cond
        self.port=circuit.notch_port(x[cond],z[cond])
        self.port.autofit(guessdelay=guessdelay[0])
        self.fr_min=x[np.argmin(np.abs(z[cond]))]
        self.root.root.frmin_fit_list[index_crop]=self.fr_min
        self.fig,(self.ax1,self.ax2,self.ax3)=matplotlib.pyplot.subplots(1,3,figsize=(15,5),dpi=100)
        
        self.real_raw=z.real
        self.imag_raw=z.imag
        self.real_fit=self.port.z_data_sim.real
        self.imag_fit=self.port.z_data_sim.imag
        self.wm_title("Fit at "+cbarsweep[0]+" "+str(self.root.root.itvector[self.index,0]))
        self.fig.suptitle(suptitle_onepointfitwindow[0], fontsize=16)
        self.ax1.plot(self.real_raw,self.imag_raw,color='black',label='Raw')
        self.ax1.plot(self.real_fit,self.imag_fit,color='red',label='Fit',linestyle='--')
        self.ax1.set_xlabel(xlabel_onepointfitwindow[0])
        self.ax1.set_ylabel(ylabel_onepointfitwindow[0])
        self.ax1.legend()
        self.ax1.grid(True)

        self.ax2.plot(x/1e9,np.abs(z),color='black',label='Raw')
        self.ax2.plot(x[cond]/1e9,np.abs(self.port.z_data_sim),color='red',label='Fit',linestyle='--')
        self.ax2.set_xlabel(xlabel_onepointfitwindow[1])	
        self.ax2.set_ylabel(ylabel_onepointfitwindow[1])
        self.ax2.legend()
        self.ax2.grid(True)


        self.ax3.plot(x,np.angle(z),color='black',label='Raw') 
        self.ax3.plot(x[cond],np.angle(self.port.z_data_sim),color='red',label='Fit',linestyle='--')
        self.ax3.set_xlabel(xlabel_onepointfitwindow[2])
        self.ax3.set_ylabel(ylabel_onepointfitwindow[2])
        self.ax3.legend()
        self.ax3.grid(True)
        
        self.fig.tight_layout()
        self.upperframe=tk.Frame(self,width=SIZE_X,height=SIZE_Y-150)
        self.upperframe.pack(side='top',fill='both',expand=True)
        self.canvas=FigureCanvasTkAgg(self.fig,self.upperframe)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, self.upperframe)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.draw()


        
        self.lowerframe=tk.Frame(self,width=SIZE_X,height=150)
        self.lowerframe.pack(side='bottom',fill='both',expand=True)

        self.parameterschart=InformationChart(self.lowerframe,ParametersDataframe(self))
        self.parameterschart.treeview.pack(fill='both',expand=True)

        self.controlcanvas=ControlCanvas(self.lowerframe)
        self.controlcanvas.add_object(OnePointFit)
        self.controlcanvas.add_object(OnePointFitLabelsX,x=400)
        self.controlcanvas.add_object(OnePointFitLabelsY,x=400)
        self.controlcanvas.add_object(OnePointFitSave,x=400)
        self.controlcanvas.add_object(OnePointFitSaveChart,x=400)
        self.controlcanvas.pack(fill='x',expand=True)
        self.mainloop()
    def save(self):
        filename=tk.filedialog.asksaveasfilename(title="Select file",filetypes=(("txt files","*.txt"),("all files","*.*")))
        freq=self.port.f_data
        z_real_raw=self.port.z_data_raw.real
        z_imag_raw=self.port.z_data_raw.imag
        z_real_fit=self.port.z_data_sim.real
        z_real_imag=self.port.z_data_sim.imag
        s21_raw=np.abs(z_real_raw+1j*z_imag_raw)
        s21_fit=np.abs(z_real_fit+1j*z_real_imag)
        phase_raw=np.angle(z_real_raw+1j*z_imag_raw)
        phase_fit=np.angle(z_real_fit+1j*z_real_imag)

        with open(filename,'w') as o:
            print("freq\tz_real_raw\tz_imag_raw\tz_real_fit\tz_imag_fit\ts21_raw\ts21_fit\tphase_raw\tphase_fit",file=o)
            for i in range(len(freq)):
                print(str(freq[i])+"\t"+str(z_real_raw[i])+"\t"+str(z_imag_raw[i])+"\t"+str(z_real_fit[i])+"\t"+str(z_real_imag[i])+"\t"+str(s21_raw[i])+"\t"+str(s21_fit[i])+"\t"+str(phase_raw[i])+"\t"+str(phase_fit[i]),file=o)
    def save_chart(self):
        filename=tk.filedialog.asksaveasfilename(title="Select file",filetypes=(("txt files","*.txt"),("all files","*.*")))
        df=self.parameterschart.df
        df.to_csv(filename,sep='\t',index=False)
class CutWindow(tk.Toplevel):
    def __init__(self,root,index):
        self.root=root
        self.index=index
        tk.Toplevel.__init__(self,root)
        self.x=self.root.y
        fixed_freq=self.root.x[index]
        self.y=self.root.Z[:,index]
        self.fig,ax=matplotlib.pyplot.subplots(figsize=(15,5),dpi=100)
        ax.plot(self.x,self.y,'-o')
        ax.set_xlabel(self.root.ax.get_ylabel())
        ax.set_ylabel(self.root.cbar.ax.get_title())
        ax.set_title("$\mathrm{Frequency}$"+"="+str(fixed_freq/1e9)+"$\mathrm{GHz}$")
        self.canvas=FigureCanvasTkAgg(self.fig,self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.draw()


class InformationWindow(tk.Toplevel):
    def __init__(self,root,file):
        tk.Toplevel.__init__(self,root)
        self.file=file
        doc = fitz.open(file)
        zoom = 1
        mat = fitz.Matrix(zoom, zoom)
        num_pages = 0
        for p in doc:
            num_pages += 1
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side = tk.RIGHT, fill = "y")
        canvas = tk.Canvas(self, yscrollcommand = scrollbar.set)
        canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1)
        entry = tk.Entry(self)
        label = tk.Label(self, text="Enter page number to display:")
        def pdf_to_img(page_num):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=mat)
            return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        def show_image():
            try:
                page_num = int(entry.get()) - 1
                assert page_num >= 0 and page_num < num_pages
                im = pdf_to_img(page_num)
                img_tk = ImageTk.PhotoImage(im)
                frame = tk.Frame(canvas)
                panel = tk.Label(frame, image=img_tk)
                panel.pack(side="bottom", fill="both", expand="yes")
                frame.image = img_tk
                canvas.create_window(0, 0, anchor='nw', window=frame)
                frame.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))
            except:
                pass
        button = tk.Button(self, text="Show Page", command=show_image)
        label.pack(side=tk.TOP, fill=None)
        entry.pack(side=tk.TOP, fill=tk.BOTH)
        button.pack(side=tk.TOP, fill=None)
        entry.insert(0, '1')
        show_image()
        scrollbar.config(command = canvas.yview)
        self.mainloop()
        doc.close()



class ControlCanvas(tk.Canvas):
    def __init__(self,root):
        tk.Canvas.__init__(self,root,bg=MENU_COLOR)
        self.root=root
        self.object_list=[]
        self.posx=0
        self.posy=0
    def add_object(self,object,x=0,y=0):
        self.posx+=x
        self.posy+=y
        self.object_list.append(object(self))
    def clear(self):
        for widgets in self.winfo_children():
            widgets.destroy()
        self.posy=0


class ButtonsAndEntries:
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
    def switch(self,plot=True):
        if self.globalparams_list[0]==True:
            self.globalparams_list[0]=False
            self.entry_list[0].configure(text="Off")
        else:
            self.globalparams_list[0]=True
            self.entry_list[0].configure(text="On")
        if plot==True:
            self.canvas.root.master.plot()
    def switch_baseline(self):
        if self.globalparams_list[0]!="":
            self.globalparams_list[0]=""
            self.entry_list[0].configure(text="Off")
        else:
            filename=tk.filedialog.askdirectory()
            self.globalparams_list[0]=filename
            self.entry_list[0].configure(text="On")

        self.canvas.root.master.load_data(reset=False)
        self.canvas.root.master.load_baseline()
        self.canvas.root.master.smooth_data()
        self.canvas.root.master.plot()
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
        button_width=50
        button_height=120
        self.canvas=canvas
        self.canvas.create_window(self.canvas.posx+160, self.canvas.posy+140,width=button_width,height=button_height,
                                      window=tk.Button(self.canvas.root, text="Customize plot", command=lambda: self.customize_plot()))
class ColorPlotButton(ButtonsAndEntries):
    def __init__(self,canvas):
        button_width=50
        button_height=120
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

class Dataframe:
    def __init__(self,root):
        self.root=root
        self.update()
class SweepsDataframe(Dataframe):
    def __init__(self,root):
        Dataframe.__init__(self,root)
    def update(self):
        global sweep_list
        try:
            temp_ini=self.root.temp[sweep_list[0]][0]
            temp_end=self.root.temp[sweep_list[1]-1][0]
        except:
            temp_ini=np.nan
            temp_end=np.nan
        try:
            power_ini=self.root.power[sweep_list[0]][0]
            power_end=self.root.power[sweep_list[1]-1][0]
        except:
            power_ini=np.nan
            power_end=np.nan
        try:
            bandwidth_ini=self.root.bandwidth[sweep_list[0]][0]
            bandwidth_end=self.root.bandwidth[sweep_list[1]-1][0]
        except:
            bandwidth_ini=np.nan
            bandwidth_end=np.nan
        try:
            bx_ini=self.root.bx[sweep_list[0]][0]
            bx_end=self.root.bx[sweep_list[1]-1][0]
        except:
            bx_ini=np.nan
            bx_end=np.nan
        try:
            by_ini=self.root.by[sweep_list[0]][0]
            by_end=self.root.by[sweep_list[1]-1][0]
        except:
            by_ini=np.nan
            by_end=np.nan
        try:
            bz_ini=self.root.bz[sweep_list[0]][0]
            bz_end=self.root.bz[sweep_list[1]-1][0]
        except:
            bz_ini=np.nan
            bz_end=np.nan

        self.df=pd.DataFrame({' ': ['Initial sweep','Final sweep'],'Temperature (K)': [temp_ini,temp_end],'Power (dBm)': [power_ini,power_end],'Bandwidth (Hz)': [bandwidth_ini,bandwidth_end],'Bx (T)': [bx_ini,bx_end],'By (T)': [by_ini,by_end],'Bz (T)': [bz_ini,bz_end]})
class NumberDataframe(Dataframe):
    def __init__(self,root):
        Dataframe.__init__(self,root)
    def update(self):
        self.df=pd.DataFrame({'Number of Files': [self.root.nfiles],'Number of sweeps': [self.root.nsimus],'Number of points per sweep': [self.root.npoints]})
class ParametersDataframe(Dataframe):
    def __init__(self,root):
        Dataframe.__init__(self,root)
    def update(self):
        port=self.root.port
        Qi=port.fitresults['Qi_dia_corr']
        Qi_err=port.fitresults['Qi_dia_corr_err']
        Qc=port.fitresults['absQc']
        Qc_err=port.fitresults['absQc_err']
        fr=port.fitresults['fr']
        fr_err=port.fitresults['fr_err']
        phi0=port.fitresults['phi0']
        phi0_err=port.fitresults['phi0_err']
        a=port.fitresults['a']
        alpha=port.fitresults['alpha']
        delay=port.fitresults['delay']
        Qt=1/(1/Qi+1/Qc)
        #formula to calculate the error of Qt
        Qt_err=Qt**2*np.sqrt((Qi_err/Qi**2)**2+(Qc_err/Qc**2)**2)
        self.df=pd.DataFrame({'Parameter':['Resonance frequency(fit)','Resonance frequency(min)','Qi','Qc','Qt','phi0','a','alpha','delay'],
                              'Value':[fr/1e9,self.root.fr_min/1e9,Qi,Qc,Qt,phi0,a,alpha,delay],
                              'Uncertainty':[fr_err/1e9,0,Qi_err,Qc_err,Qt_err,phi0_err,0,0,0]})


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

app = SeaofBTCapp()
app.mainloop()
