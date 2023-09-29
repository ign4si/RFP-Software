from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk


import matplotlib
import expdatafunc as edf
matplotlib.use("TkAgg")
import numpy as np
from resonator_tools import circuit

import numpy as np
from Classes.windows import Windows
from Classes.canvas import ControlCanvas,InformationChart
from Classes.buttonsandentries import Switchs,Entries,Navigator,RadioButtons,FunctionButtons
from Classes.toplevels import plotWindow,ColorPlot,fitWindow,OnePointFitWindow,CutWindow
from Classes.dataframe import SweepsDataframe,NumberDataframe


LARGE_FONT = ("CMU Serif", 16)
NORM_FONT = ("CMU Serif", 10)
SMALL_FONT = ("CMU Serif", 6)

SIZE_Y=720
SIZE_X=1280

HOMEPAGEBG="#273746"
MENU_COLOR="#1B252F"


COLORMAP_LIST=['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 
'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']


def smoothfunc(y, box_pts):
    if box_pts==0:
        return y
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
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
                             command=lambda: self.controller.back_to_start())
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
        self.canvas.draw()
        
       
        
        self.create_controlcanvas()

        self.dataframe_list.append(SweepsDataframe(self))
        self.dataframe_list.append(NumberDataframe(self))
        
        for i in self.dataframe_list:
            self.informationchart_list.append(InformationChart(self.rightframe,i,self))

        for i in self.informationchart_list:
            i.treeview.pack(side='top',fill='x',expand=False)
        self.bind_all("<Return>",lambda event:[print("Workspace"),self.controlcanvas.submit_all()])
    def create_controlcanvas(self):
        #create the canvas for the buttons
        self.controlcanvas=ControlCanvas(self.rightframe,self)

        #create the button
        xsep=260
        ysep=70
        SweepFile=Entries(self.controlcanvas,["file"],["file"],[int])
        self.controlcanvas.add_object(SweepFile)
        self.controlcanvas.move(xsep,0)

        SweepEntries=Entries(self.controlcanvas,["sweep_ini","sweep_end","sweep_step"],["ini","end","step"],[int,int,int])
        self.controlcanvas.add_object(SweepEntries)
        self.controlcanvas.move(-xsep,ysep)

        Shift=Entries(self.controlcanvas,["shift"],["shift"],[float],autoscale=True)
        self.controlcanvas.add_object(Shift)
        self.controlcanvas.move(xsep,0)

        Colour=Navigator(self.controlcanvas,"colormap",COLORMAP_LIST,"colormap")
        self.controlcanvas.add_object(Colour)
        self.controlcanvas.move(-xsep,ysep)

        Cbar=Switchs(self.controlcanvas,"colorbar_bool","colorbar_bool",spec_func_on=lambda: self.plot(),spec_func_off=lambda: self.plot())
        self.controlcanvas.add_object(Cbar)
        self.controlcanvas.move(xsep,0)

        CbarSweep=Navigator(self.controlcanvas,"colorbar_sweep",["T","P","B","Bx","By","Bz"],"cbar")
        self.controlcanvas.add_object(CbarSweep)
        self.controlcanvas.move(-xsep,ysep)

        Fit=FunctionButtons(self.controlcanvas,self.fit,"Fit")
        self.controlcanvas.add_object(Fit)
        self.controlcanvas.move(xsep,0)

        GuessDelay=Switchs(self.controlcanvas,"guessdelay","guessdelay")
        self.controlcanvas.add_object(GuessDelay)
        self.controlcanvas.move(-xsep,ysep)

        PlotParameters=FunctionButtons(self.controlcanvas,self.customize_plot,"Plot Parameters")
        self.controlcanvas.add_object(PlotParameters)
        self.controlcanvas.move(xsep,0)

        PlotY=Navigator(self.controlcanvas,"yplot",["S21","S21dB","Phase"],"y",autoscale=True)
        self.controlcanvas.add_object(PlotY)
        self.controlcanvas.move(-xsep,ysep)

        Baseline=FunctionButtons(self.controlcanvas,lambda: [self.load_baseline(),self.add_baseline(),self.smooth_data(),self.plot(),self.autoscale()],"Baseline")
        self.controlcanvas.add_object(Baseline)
        self.controlcanvas.move(xsep,0)

        BaselineSweep=Entries(self.controlcanvas,["baseline_file","baseline_sweep","baseline_shift"],["file","sweep","shift"],[int,int,float],spec_func=lambda:[self.add_baseline(),self.smooth_data()])
        self.controlcanvas.add_object(BaselineSweep)
        self.controlcanvas.move(-xsep,ysep)

        Smooth=Entries(self.controlcanvas,["smooth"],["smooth"],[int],spec_func=lambda:[self.add_baseline(),self.smooth_data()])
        self.controlcanvas.add_object(Smooth)
        self.controlcanvas.move(xsep,0)

        ColorPlotButton=FunctionButtons(self.controlcanvas,self.color_plot,"Color Plot")
        self.controlcanvas.add_object(ColorPlotButton)
        self.controlcanvas.move(-xsep,ysep)

        Autoscale=FunctionButtons(self.controlcanvas,self.autoscale,"Autoscale")
        self.controlcanvas.add_object(Autoscale)
        self.controlcanvas.move(xsep,0)
        self.controlcanvas.pack(side='top',fill='both',expand=True)
    def initialize_parameters(self):
        filename="initial_parameters.txt"
        dicparameters={}
        with open(filename,"r") as f:
            lines=f.readlines()
            for line in lines:
                line=line.split()
                try:
                    if line[1]=="None":
                        dicparameters[line[0]]=None
                    else:
                        dicparameters[line[0]]=line[1]
                except:
                    pass
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
        self.parameters["baseline_folder"]=self.select_folder()
        if self.parameters["baseline_folder"]!=None:
            try:
                self.Baseline=edf.Data(self.parameters["baseline_folder"],verbose=True)
            except:
                print("Baseline not loaded")
    def add_baseline(self):
        baseline_sweep=[int(self.parameters["baseline_file"]),int(self.parameters["baseline_sweep"]),float(self.parameters["baseline_shift"])]
        file=int(self.parameters["file"])
        if self.parameters["baseline_folder"]!=None and self.parameters["baseline_folder"]!="":
            self.Baseline_amplitude_DB=self.Baseline.S21_DB[baseline_sweep[0]][baseline_sweep[1]]
            self.Baseline_phase=self.Baseline.phase[baseline_sweep[0]][baseline_sweep[1]]
        else:
            self.Baseline_amplitude_DB=np.zeros(len(self.Data.freq[0][0]))
            self.Baseline_phase=np.zeros(len(self.Data.freq[0][0]))

        self.amplitude_DB=np.array([self.Data.S21_DB[file][i]-self.Baseline_amplitude_DB+baseline_sweep[2] for i in range(len(self.Data.S21_DB[file]))])
        self.phase=np.array([self.Data.phase[file][i]-self.Baseline_phase for i in range(len(self.Data.phase[file]))])
        self.amplitude=np.power(10,self.amplitude_DB/20)
        self.amplitude_complex=self.amplitude*np.exp(1j*self.phase)

    def smooth_data(self):
        smoothlist=int(self.parameters["smooth"])

        self.amplitude_DB=np.array([smoothfunc(self.amplitude_DB[i],smoothlist) for i in range(len(self.amplitude_DB))])
        self.phase=np.array([smoothfunc(self.phase[i],smoothlist) for i in range(len(self.phase))])
        self.amplitude=np.power(10,self.amplitude_DB/20)
        self.amplitude_complex=self.amplitude*np.exp(1j*self.phase)



    def save_limits(self):
        xmin,xmax=self.a.get_xlim()
        ymin,ymax=self.a.get_ylim()
        self.parameters["xmin"]=xmin
        self.parameters["xmax"]=xmax
        self.parameters["ymin"]=ymin
        self.parameters["ymax"]=ymax
    def plot(self):
        xscale=self.parameters["xscale"]
        yscale=self.parameters["yscale"]
        shift=float(self.parameters["shift"])
        xlabel=self.parameters["xlabel"]
        xlabel_fontsize=float(self.parameters["xlabel_fontsize"])
        ylabel_fontsize=float(self.parameters["ylabel_fontsize"])
        title=self.parameters["title"]
        title_fontsize=float(self.parameters["title_fontsize"])
        linewidth=float(self.parameters["linewidth"])
        marker=self.parameters["marker"]
        markersize=float(self.parameters["markersize"])
        linestyle=self.parameters["linestyle"]
        ticksin=bool(self.parameters["ticks_in"])
        sweep_list=[int(self.parameters["sweep_ini"]),int(self.parameters["sweep_end"]),int(self.parameters["sweep_step"])]
        colorbar_bool=bool(self.parameters["colorbar_bool"])
        colorbar_fontsize=float(self.parameters["colorbar_fontsize"])
        ticks_fontsize=float(self.parameters["ticks_fontsize"])
        grid_bool=bool(self.parameters["grid_bool"])
        file=int(self.parameters["file"]) 
        # print("xscale=",xscale)
        # print("yscale=",yscale)
        # print("shift=",shift)
        # print("xlabel=",xlabel)
        # print("xlabel_fontsize=",xlabel_fontsize)
        # print("ylabel_fontsize=",ylabel_fontsize)
        # print("title=",title)
        # print("title_fontsize=",title_fontsize)
        # print("linewidth=",linewidth)
        # print("markersize=",markersize)
        # print("linestyle=",linestyle)
        # print("ticksin=",ticksin)
        # print("sweep_list=",sweep_list)
        # print("colorbar_bool=",colorbar_bool)
        # print("colorbar_fontsize=",colorbar_fontsize)
        # print("ticks_fontsize=",ticks_fontsize)
        # print("grid_bool=",grid_bool)
        # print("file=",file)

        if self.parameters["xticks_ini"]==None:
            xticks=None
        else:
            xticks=np.linspace(float(self.parameters["xticks_ini"]),float(self.parameters["xticks_end"]),int(self.parameters["xticks_nintervals"]))
        if self.parameters["yticks_ini"]==None:
            yticks=None
        else:
            yticks=np.linspace(float(self.parameters["yticks_ini"]),float(self.parameters["yticks_end"]),int(self.parameters["yticks_nintervals"]))

        cmap=matplotlib.pyplot.get_cmap(self.parameters["colormap"])
        if self.parameters["xmin"]!=None and self.parameters["xmax"]!=None and self.parameters["ymin"]!=None and self.parameters["ymax"]!=None:
            self.save_limits()
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
        if self.cbar!=None:
            self.cbar.remove()
        ylabel=self.parameters["ylabel"]        

        if sweep_list[1]<0:
            sweep_list[1]=len(self.Data.freq[file])+sweep_list[1]+1
            self.parameters["sweep_end"]=sweep_list[1]
    
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
                self.a.plot(self.freq[j]/1e9, self.yplot[j]+shift*j,color=cmap(j/sweep_list[1]),marker=marker,linewidth=linewidth,linestyle=linestyle,markersize=markersize)
            else:
                self.a.plot(self.freq[j]/1e9, self.yplot[j]+shift*j,color=cmap((self.itvector[j][0]-first_value)/(last_value-first_value)),marker=marker,linewidth=linewidth,linestyle=linestyle,markersize=markersize)
        
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
        self.a.set_xscale(xscale)
        self.a.set_yscale(yscale)
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
        for i in self.informationchart_list:
            i.update()
        if self.parameters["xmin"]!=None and self.parameters["xmax"]!=None and self.parameters["ymin"]!=None and self.parameters["ymax"]!=None:
            self.a.set_xlim([float(self.parameters["xmin"]),float(self.parameters["xmax"])])
            self.a.set_ylim([float(self.parameters["ymin"]),float(self.parameters["ymax"])])
        else:
            self.save_limits()
        self.canvas.draw()


        
    def autoscale(self):
        self.a.autoscale()
        self.canvas.draw()
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