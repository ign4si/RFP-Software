import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from resonator_tools import circuit
from Classes.canvas import ControlCanvas,InformationChart
from Classes.buttonsandentries import Switchs,Entries,Navigator,FunctionButtons
from matplotlib.widgets import Cursor
from Classes.dataframe import ParametersDataframe
HOMEPAGEBG="#273746"
LARGE_FONT = ("CMU Serif", 16)
NORM_FONT = ("CMU Serif", 10)
SMALL_FONT = ("CMU Serif", 6)

COLORMAP_LIST=['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 
'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']
LINESTYLE_LIST=['-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted']
MARKER_LIST=[".",",","o","v","^","<",">","1","2","3","4","8","s","p","P","*","h","H","+","D","d"]
X_PREFIX_LIST=["","k","M","G","T","P","E","Z","Y"]
COLORBAR_PREFIX_LIST=["","m","\mu ","n","p","f","a","z","y"]
X_PREFIX_VALUES_LIST=[1,1e3,1e6,1e9,1e12,1e15,1e18,1e21,1e24]
COLORBAR_PREFIX_VALUES_LIST=[1,1e-3,1e-6,1e-9,1e-12,1e-15,1e-18,1e-21,1e-24]
class plotWindow(tk.Toplevel):
    def __init__(self,controller):
        tk.Toplevel.__init__(self,controller)
        self.controller=controller
        self.wm_title("Plot parameters")
        self.configure(bg=HOMEPAGEBG)
        self.create_controlcanvas()
        self.bind("<Return>",lambda event:[print("plotWindow"),self.controlcanvas.submit_all()])
        self.state('zoomed')

    def create_controlcanvas(self):
        self.controlcanvas=ControlCanvas(self,self.controller)
        xsep=500
        ysep=200
        
        Fontsize=Entries(self.controlcanvas,["xlabel_fontsize","ylabel_fontsize","title_fontsize","ticks_fontsize","colorbar_fontsize"],["xlabel","ylabel","title","ticks","colorbar"],[float,float,float,float,float])
        self.controlcanvas.add_object(Fontsize)
        self.controlcanvas.move(xsep,0)
        
        PlotLabels=Entries(self.controlcanvas,["title"],["title"],[str])
        self.controlcanvas.add_object(PlotLabels)
        self.controlcanvas.move(xsep,0)
        
        GridBool=Switchs(self.controlcanvas,"grid_bool","grid",spec_func_on=self.controller.plot,spec_func_off=self.controller.plot)
        self.controlcanvas.add_object(GridBool)
        self.controlcanvas.move(-2*xsep,ysep)

        
        Marker=Navigator(self.controlcanvas,"marker",MARKER_LIST,"marker",type=str)
        self.controlcanvas.add_object(Marker)
        self.controlcanvas.move(xsep,0)
        
        
        Linestyle=Navigator(self.controlcanvas,"linestyle",LINESTYLE_LIST,"linestyle",type=str)	
        self.controlcanvas.add_object(Linestyle)
        self.controlcanvas.move(xsep,0)
        
        Linewidth=Entries(self.controlcanvas,["linewidth"],["linewidth"],[float])
        self.controlcanvas.add_object(Linewidth)
        self.controlcanvas.move(-2*xsep,ysep)
        
        TicksIn=Switchs(self.controlcanvas,"ticks_in","ticksin",spec_func_on=self.controller.plot,spec_func_off=self.controller.plot)
        self.controlcanvas.add_object(TicksIn)
        self.controlcanvas.move(xsep,0)
        
        XScale=Navigator(self.controlcanvas,"xscale",["linear","log"],"xscale")
        self.controlcanvas.add_object(XScale)
        self.controlcanvas.move(xsep,0)
        
        YScale=Navigator(self.controlcanvas,"yscale",["linear","log"],"yscale") 
        self.controlcanvas.add_object(YScale)
        self.controlcanvas.move(-2*xsep,ysep)

        self.controlcanvas.pack(side='top',fill='both',expand=True,pady=10, padx=10)
class ColorPlot(tk.Toplevel):
    def __init__(self,controller):
        tk.Toplevel.__init__(self,controller)
        self.controller=controller
        self.configure(bg=HOMEPAGEBG)
        self.title=tk.Label(self,text="Color Plot",font=LARGE_FONT,bg=HOMEPAGEBG,fg="white")
        self.title.pack(side='top',fill='x',pady=10, padx=10)
        self.state('zoomed')
        #initialize data
        self.initialize_data()
        #initialize empty figure
        self.fig=plt.figure(figsize=(15,5),dpi=100)
        self.ax=self.fig.add_subplot(111)
        self.canvas=FigureCanvasTkAgg(self.fig,self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.plot()
        self.create_controlcanvas()
        self.cut_cursor()
        self.bind("<Return>",lambda event:[self.controlcanvas.submit_all(),self.update_plot()])

    def cut_cursor(self):
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
    def create_controlcanvas(self):
        #add ControlCanvas
        self.controlcanvas=ControlCanvas(self,self.controller)
        xsep=350
        cp_Title=Entries(self.controlcanvas,["cp_title"],["title"],[str])
        self.controlcanvas.add_object(cp_Title)
        cp_Fontsize=Entries(self.controlcanvas,["cp_title_fontsize","cp_xlabel_fontsize","cp_ylabel_fontsize","cp_colorbar_title_fontsize","cp_ticks_fontsize"],["title","xlabel","ylabel","colorbar title","ticks"],[float,float,float,float,float])
        self.controlcanvas.add_object(cp_Fontsize)
        self.controlcanvas.move(xsep,0)
        cp_Colormap=Navigator(self.controlcanvas,"cp_colormap",COLORMAP_LIST,"colormap")
        self.controlcanvas.add_object(cp_Colormap)
        self.controlcanvas.pack(side='top',fill='x',pady=10, padx=10)
    def initialize_data(self):
        sweep_list=[int(self.controller.parameters["sweep_ini"]),int(self.controller.parameters["sweep_end"]),int(self.controller.parameters["sweep_step"])]
        self.wm_title("Color plot")
        self.x=self.controller.freq[0]
        self.y=self.controller.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0]
        self.Z=self.controller.yplot[sweep_list[0]:sweep_list[1]:sweep_list[2],:]
        self.X,self.Y=np.meshgrid(self.x/1e9,self.y)
    def plot(self):
        cp_colormap = self.controller.parameters["cp_colormap"]
        cp_title = self.controller.parameters["cp_title"]
        cp_title_fontsize = self.controller.parameters["cp_title_fontsize"]
        cp_xlabel = self.controller.parameters["xlabel"]
        cp_xlabel_fontsize = self.controller.parameters["cp_xlabel_fontsize"]
        cp_ylabel = self.controller.parameters["colorbar_title"]
        cp_ylabel_fontsize = self.controller.parameters["cp_ylabel_fontsize"]
        cp_colorbar_title = self.controller.parameters["ylabel"]
        cp_colorbar_title_fontsize = self.controller.parameters["cp_colorbar_title_fontsize"]
        cp_ticks_fontsize = self.controller.parameters["cp_ticks_fontsize"]
        
        cmap = plt.get_cmap(cp_colormap)
        
        self.imagen = self.ax.pcolormesh(self.X, self.Y, self.Z, cmap=cmap)
        self.ax.set_xlabel(cp_xlabel, fontsize=cp_xlabel_fontsize)
        self.ax.set_ylabel(cp_ylabel, fontsize=cp_ylabel_fontsize)
        self.ax.set_title(cp_title, fontsize=cp_title_fontsize)
        self.cbar = plt.colorbar(self.imagen, ax=self.ax)
        self.cbar.ax.set_title(cp_colorbar_title, fontsize=cp_colorbar_title_fontsize)
        self.cbar.ax.tick_params(labelsize=cp_ticks_fontsize)
        
        self.ax.tick_params(axis='both', which='major', labelsize=cp_ticks_fontsize)
        self.canvas.draw()
    def update_plot(self):
        cp_colormap = self.controller.parameters["cp_colormap"]
        cp_title = self.controller.parameters["cp_title"]
        cp_title_fontsize = self.controller.parameters["cp_title_fontsize"]
        cp_xlabel = self.controller.parameters["xlabel"]
        cp_xlabel_fontsize = self.controller.parameters["cp_xlabel_fontsize"]
        cp_ylabel = self.controller.parameters["colorbar_title"]
        cp_ylabel_fontsize = self.controller.parameters["cp_ylabel_fontsize"]
        cp_colorbar_title = self.controller.parameters["ylabel"]
        cp_colorbar_title_fontsize = self.controller.parameters["cp_colorbar_title_fontsize"]
        cp_ticks_fontsize = self.controller.parameters["cp_ticks_fontsize"]
        
        cmap = plt.get_cmap(cp_colormap)
        
        self.imagen.set_cmap(cmap)
        self.ax.set_xlabel(cp_xlabel, fontsize=cp_xlabel_fontsize)
        self.ax.set_ylabel(cp_ylabel, fontsize=cp_ylabel_fontsize)
        self.ax.set_title(cp_title, fontsize=cp_title_fontsize)
        self.cbar.update_normal(self.imagen)
        self.cbar.ax.set_title(cp_colorbar_title, fontsize=cp_colorbar_title_fontsize)
        self.cbar.ax.tick_params(labelsize=cp_ticks_fontsize)
        
        self.ax.tick_params(axis='both', which='major', labelsize=cp_ticks_fontsize)
        self.canvas.draw()
class fitWindow(tk.Toplevel):
    def __init__(self,controller,number_of_fits):
        tk.Toplevel.__init__(self,controller)
        self.controller=controller
        self.wm_title("Fit")
        self.configure(bg=HOMEPAGEBG)
        self.title=tk.Label(self,text="Fit",font=LARGE_FONT,bg=HOMEPAGEBG,fg="white")
        self.title.pack(side='top',fill='x',pady=10, padx=10)
        #initialize sweep_list
        sweep_list=[int(self.controller.parameters["sweep_ini"]),int(self.controller.parameters["sweep_end"]),int(self.controller.parameters["sweep_step"])]
        #create the figure
        self.state('zoomed')
        if number_of_fits!=1:
            self.fig,(self.ax1,self.ax2,self.ax3)=plt.subplots(1,3,figsize=(15,5),dpi=100)
            self.canvas=FigureCanvasTkAgg(self.fig,self)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(self.canvas, self)
            toolbar.update()
            self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.plot()
            #create the cursor for the plot updating
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
                    index_crop=np.argmin(np.abs(self.controller.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0]-xevent))
                    OnePointFitWindow(self,index_crop)
            self.create_controlcanvas()
            self.bind("<Return>",lambda event:[self.controlcanvas.submit_all(),self.plot()])
            cid = self.fig.canvas.mpl_connect('button_press_event', onclick)
        else:
            OnePointFitWindow(self,0)
        
    def create_controlcanvas(self):
        self.controlcanvas=ControlCanvas(self,self.controller)
        xsep=400
        fw_Suptitle=Entries(self.controlcanvas,["fw_suptitle"],["suptitle"],[str])
        self.controlcanvas.add_object(fw_Suptitle)
        self.controlcanvas.move(xsep,0)
        fw_SuptitleFontsize=Entries(self.controlcanvas,["fw_suptitle_fontsize"],["title"],[float])
        self.controlcanvas.add_object(fw_SuptitleFontsize)
        self.controlcanvas.move(xsep,0)
        fw_Save=FunctionButtons(self.controlcanvas,self.save,"Save")
        self.controlcanvas.add_object(fw_Save)
        self.controlcanvas.pack(side=tk.TOP, fill="x", expand=True)
    def plot(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        sweep_list=[int(self.controller.parameters["sweep_ini"]),int(self.controller.parameters["sweep_end"]),int(self.controller.parameters["sweep_step"])]
        fw_ylabel_1=self.controller.parameters["xlabel"]
        fw_ylabel_2=self.controller.parameters["fw_ylabel_2"]
        fw_ylabel_3=self.controller.parameters["fw_ylabel_3"]
        fw_xlabel=self.controller.parameters["colorbar_title"]
        fw_grid_bool=self.controller.parameters["fw_grid_bool"]
        fw_suptitle=self.controller.parameters["fw_suptitle"]
        fw_xlabel_fontsize=self.controller.parameters["fw_xlabel_fontsize"]
        fw_ylabel_fontsize=self.controller.parameters["fw_ylabel_fontsize"]
        fw_suptitle_fontsize=self.controller.parameters["fw_title_fontsize"]
        fw_ticks_fontsize=self.controller.parameters["fw_ticks_fontsize"]

        x_prefix=self.controller.parameters["x_prefix"]
        colorbar_prefix=self.controller.parameters["colorbar_prefix"]
        x_prefix_value=float(X_PREFIX_VALUES_LIST[X_PREFIX_LIST.index(x_prefix)])
        colorbar_prefix_value=float(COLORBAR_PREFIX_VALUES_LIST[COLORBAR_PREFIX_LIST.index(colorbar_prefix)])

        self.ax1.plot(self.controller.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0]/colorbar_prefix_value,np.array(self.controller.frmin_fit_list)/x_prefix_value,'o',color='black')
        print(self.controller.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0]/colorbar_prefix_value)
        print(self.controller.Qi_err_fit_list)
        self.ax2.errorbar(self.controller.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0]/colorbar_prefix_value,self.controller.Qi_fit_list,yerr=self.controller.Qi_err_fit_list,fmt='o',color='black')
        self.ax3.errorbar(self.controller.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0]/colorbar_prefix_value,self.controller.Qc_fit_list,yerr=self.controller.Qc_err_fit_list,fmt='o',color='black')
        self.ax1.set_xlabel(fw_xlabel,fontsize=fw_xlabel_fontsize)
        self.ax1.set_ylabel(fw_ylabel_1,fontsize=fw_ylabel_fontsize)
        self.ax2.set_xlabel(fw_xlabel,fontsize=fw_xlabel_fontsize)
        self.ax2.set_ylabel(fw_ylabel_2,fontsize=fw_ylabel_fontsize)
        self.ax3.set_xlabel(fw_xlabel,fontsize=fw_xlabel_fontsize)
        self.ax3.set_ylabel(fw_ylabel_3,fontsize=fw_ylabel_fontsize)
        self.ax1.grid(fw_grid_bool)
        self.ax2.grid(fw_grid_bool)
        self.ax3.grid(fw_grid_bool)
        self.ax1.tick_params(axis='both', labelsize=fw_ticks_fontsize)
        self.ax2.tick_params(axis='both', labelsize=fw_ticks_fontsize)
        self.ax3.tick_params(axis='both', labelsize=fw_ticks_fontsize)

        self.fig.suptitle(fw_suptitle, fontsize=fw_suptitle_fontsize)
        self.canvas.draw()
        
        self.fig.savefig("image_fit.pdf",dpi=100)
    def save(self):
        #ask for a folder and a filename
        filename = tk.filedialog.asksaveasfilename(title="Select file",filetypes=(("txt files","*.txt"),("all files","*.*")))
        sweep_list=[int(self.controller.parameters["sweep_ini"]),int(self.controller.parameters["sweep_end"]),int(self.controller.parameters["sweep_step"])]
        x=self.controller.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0]
        y1=self.controller.frmin_fit_list
        y1_fit=self.controller.fr_fit_list
        y1_fit_err=self.controller.fr_err_fit_list
        y2=self.controller.Qi_fit_list
        y3=self.controller.Qc_fit_list
        y2err=self.controller.Qi_err_fit_list
        y3err=self.controller.Qc_err_fit_list
        try:
            bx=self.controller.bx[sweep_list[0]:sweep_list[1]:sweep_list[2],0]
        except:
            bx=np.zeros(len(x))
        try:
            by=self.controller.by[sweep_list[0]:sweep_list[1]:sweep_list[2],0]
        except:
            by=np.zeros(len(x))
        try:
            bz=self.controller.bz[sweep_list[0]:sweep_list[1]:sweep_list[2],0]
        except:
            bz=np.zeros(len(x))
        try:
            temp=self.controller.temp[sweep_list[0]:sweep_list[1]:sweep_list[2],0]
        except:
            temp=np.zeros(len(x))
        try:
            power=self.controller.power[sweep_list[0]:sweep_list[1]:sweep_list[2],0]
        except:
            power=np.zeros(len(x))
        try:
            bandwidth=self.controller.bandwidth[sweep_list[0]:sweep_list[1]:sweep_list[2],0]
        except:
            bandwidth=np.zeros(len(x))
        with open(filename,'w') as o:
            print("x\ty1\ty1fit\ty1fit_err\ty2\ty2err\ty3\ty3err\tbx\tby\tbz\ttemp\tpower\tbandwidth",file=o)
            for i in range(len(x)):
                print(str(x[i])+"\t"+str(y1[i])+"\t"+str(y1_fit[i])+"\t"+str(y1_fit_err[i])+"\t"+str(y2[i])+"\t"+str(y2err[i])+"\t"+str(y3[i])+"\t"+str(y3err[i])+"\t"+str(bx[i])+"\t"+str(by[i])+"\t"+str(bz[i])+"\t"+str(temp[i])+"\t"+str(power[i])+"\t"+str(bandwidth[i]),file=o)
class OnePointFitWindow(tk.Toplevel):
    def __init__(self,root,index_crop):
        tk.Toplevel.__init__(self,root)
        self.root=root
        self.controller=root.controller
        self.index_crop=index_crop
        sweep_list=[int(self.controller.parameters["sweep_ini"]),int(self.controller.parameters["sweep_end"]),int(self.controller.parameters["sweep_step"])]
        selected_value=self.controller.itvector[sweep_list[0]:sweep_list[1]:sweep_list[2],0][self.index_crop]
        self.index=np.argmin(np.abs(self.controller.itvector[:,0]-selected_value))

        self.initialize_data()
        self.fit()
        #initialize empty figure
        self.fig,(self.ax1,self.ax2,self.ax3)=plt.subplots(1,3,figsize=(15,5),dpi=100)
        self.canvas=FigureCanvasTkAgg(self.fig,self)
        self.plot()
        
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.create_controlcanvas()
        self.create_parameterschart()
        self.bind("<Return>",lambda event:[self.controlcanvas.submit_all(),self.plot()])
        self.state('zoomed')
    def initialize_data(self):
        self.x=self.controller.freq[self.index]
        self.z=self.controller.amplitude_complex[self.index]
        
        xmin=self.controller.xmin_list[self.index_crop]
        xmax=self.controller.xmax_list[self.index_crop]
        self.cond=np.logical_and(self.x>xmin,self.x<xmax)
    def fit(self):
        self.port=circuit.notch_port(self.x[self.cond],self.z[self.cond])
        try:
            self.port.autofit(guessdelay=self.controller.parameters["guessdelay"])
            Qi=self.port.fitresults['Qi_dia_corr']
            Qi_err=self.port.fitresults['Qi_dia_corr_err']
            Qc=self.port.fitresults['absQc']
            Qc_err=self.port.fitresults['absQc_err']
            fr=self.port.fitresults['fr']
            fr_err=self.port.fitresults['fr_err']
            self.controller.Qi_fit_list[self.index_crop]=Qi
            self.controller.Qi_err_fit_list[self.index_crop]=Qi_err
            self.controller.Qc_fit_list[self.index_crop]=Qc
            self.controller.Qc_err_fit_list[self.index_crop]=Qc_err
            self.controller.fr_fit_list[self.index_crop]=fr
            self.controller.fr_err_fit_list[self.index_crop]=fr_err
        except:
            #pop up a window saying that the fit failed
            print("Fit failed")
        self.fr_min=self.x[self.cond][np.argmin(np.abs(self.z[self.cond]))]
        self.controller.frmin_fit_list[self.index_crop]=self.fr_min

    def plot(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        colorbar_sweep=self.controller.parameters["colorbar_sweep"]
        self.wm_title("Fit at "+colorbar_sweep+" "+str(self.controller.itvector[self.index,0]))

        opf_xlabel_1=self.controller.parameters["opf_xlabel_1"]
        opf_ylabel_1=self.controller.parameters["opf_ylabel_1"]
        opf_xlabel_2=self.controller.parameters["opf_xlabel_2"]
        opf_ylabel_2=self.controller.parameters["opf_ylabel_2"]
        opf_xlabel_3=self.controller.parameters["opf_xlabel_3"]
        opf_ylabel_3=self.controller.parameters["opf_ylabel_3"]
        opf_grid_bool=self.controller.parameters["opf_grid_bool"]
        opf_fontsize=self.controller.parameters["opf_fontsize"]
    
        self.ax1.plot(self.z.real,self.z.imag,color='black',label='Raw')
        self.ax1.plot(self.port.z_data_sim.real,self.port.z_data_sim.imag,color='red',label='Fit',linestyle='--')
        self.ax1.set_xlabel(opf_xlabel_1,fontsize=opf_fontsize)
        self.ax1.set_ylabel(opf_ylabel_1,fontsize=opf_fontsize)
        self.ax1.legend()
        self.ax1.grid(opf_grid_bool)

        self.ax2.plot(self.x/1e9,np.abs(self.z),color='black',label='Raw')
        self.ax2.plot(self.x[self.cond]/1e9,np.abs(self.port.z_data_sim),color='red',label='Fit',linestyle='--')
        self.ax2.set_xlabel(opf_xlabel_2,fontsize=opf_fontsize)
        self.ax2.set_ylabel(opf_ylabel_2,fontsize=opf_fontsize)
        self.ax2.legend()
        self.ax2.grid(opf_grid_bool)


        self.ax3.plot(self.x,np.angle(self.z),color='black',label='Raw') 
        self.ax3.plot(self.x[self.cond],np.angle(self.port.z_data_sim),color='red',label='Fit',linestyle='--')
        self.ax3.set_xlabel(opf_xlabel_3,fontsize=opf_fontsize)
        self.ax3.set_ylabel(opf_ylabel_3,fontsize=opf_fontsize)
        self.ax3.legend()
        self.ax3.grid(opf_grid_bool)
        
        self.canvas.draw()
    def create_parameterschart(self):
        self.parameterschart=InformationChart(self,ParametersDataframe(self),self.controller)
        self.parameterschart.treeview.pack(fill='both',expand=True)
    def create_controlcanvas(self):
        self.controlcanvas=ControlCanvas(self,self.controller)
        xsep=400
        opf_button=FunctionButtons(self.controlcanvas,self.fit_button_function,"Fit")
        self.controlcanvas.add_object(opf_button)
        self.controlcanvas.move(xsep,0)
        opf_Fontsize=Entries(self.controlcanvas,["opf_fontsize"],["fontsize"],[float])
        self.controlcanvas.add_object(opf_Fontsize)
        self.controlcanvas.move(xsep,0)
        opf_GridBool=Switchs(self.controlcanvas,"opf_grid_bool","grid")
        self.controlcanvas.add_object(opf_GridBool)
        self.controlcanvas.move(xsep,0)
        opf_Save=FunctionButtons(self.controlcanvas,self.save,"Save")
        self.controlcanvas.add_object(opf_Save)
        self.controlcanvas.move(xsep,0)
        opf_SaveChart=FunctionButtons(self.controlcanvas,self.save_chart,"Save chart")
        self.controlcanvas.add_object(opf_SaveChart)
        self.controlcanvas.pack(fill='x',expand=True)
    def fit_button_function(self):
        xmin,xmax=self.ax2.get_xlim()
        self.controller.xmin_list[self.index_crop]=xmin*1e9
        self.controller.xmax_list[self.index_crop]=xmax*1e9
        self.cond=np.logical_and(self.x>(xmin*1e9),self.x<(xmax*1e9))
        self.fit()
        self.plot()
        try:
            self.root.plot()
        except:
            pass
        self.parameterschart.update()
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
        self.controller=self.root.controller
        self.index=index
        tk.Toplevel.__init__(self,root)
        self.initialize_data()
        
        self.fig,self.ax=plt.subplots(figsize=(15,5),dpi=100)
        self.canvas=FigureCanvasTkAgg(self.fig,self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.plot()
        self.state('zoomed')
    def initialize_data(self):
        self.x=self.root.y
        self.fixed_freq=self.root.x[self.index]
        self.y=self.root.Z[:,self.index]
    def plot(self):
        self.ax.clear()
        self.ax.plot(self.x,self.y,'-o')
        self.ax.set_xlabel(self.root.ax.get_ylabel())
        self.ax.set_ylabel(self.root.cbar.ax.get_title())
        self.ax.set_title("$\mathrm{Frequency}$"+"="+str(self.fixed_freq/1e9)+"$\mathrm{GHz}$")
        
        self.canvas.draw()


# class InformationWindow(tk.Toplevel):
#     def __init__(self,root,file):
#         tk.Toplevel.__init__(self,root)
#         self.file=file
#         doc = fitz.open(file)
#         zoom = 1
#         mat = fitz.Matrix(zoom, zoom)
#         num_pages = 0
#         for p in doc:
#             num_pages += 1
#         scrollbar = tk.Scrollbar(self)
#         scrollbar.pack(side = tk.RIGHT, fill = "y")
#         canvas = tk.Canvas(self, yscrollcommand = scrollbar.set)
#         canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1)
#         entry = tk.Entry(self)
#         label = tk.Label(self, text="Enter page number to display:")
#         def pdf_to_img(page_num):
#             page = doc.load_page(page_num)
#             pix = page.get_pixmap(matrix=mat)
#             return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#         def show_image():
#             try:
#                 page_num = int(entry.get()) - 1
#                 assert page_num >= 0 and page_num < num_pages
#                 im = pdf_to_img(page_num)
#                 img_tk = ImageTk.PhotoImage(im)
#                 frame = tk.Frame(canvas)
#                 panel = tk.Label(frame, image=img_tk)
#                 panel.pack(side="bottom", fill="both", expand="yes")
#                 frame.image = img_tk
#                 canvas.create_window(0, 0, anchor='nw', window=frame)
#                 frame.update_idletasks()
#                 canvas.config(scrollregion=canvas.bbox("all"))
#             except:
#                 pass
#         button = tk.Button(self, text="Show Page", command=show_image)
#         label.pack(side=tk.TOP, fill=None)
#         entry.pack(side=tk.TOP, fill=tk.BOTH)
#         button.pack(side=tk.TOP, fill=None)
#         entry.insert(0, '1')
#         show_image()
#         scrollbar.config(command = canvas.yview)
#         self.mainloop()
#         doc.close()

