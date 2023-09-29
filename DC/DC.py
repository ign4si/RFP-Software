from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

import matplotlib
import expdatafunc as edf
import numpy as np

from Classes.windows import Windows
LARGE_FONT = ("CMU Serif", 16)
NORM_FONT = ("CMU Serif", 10)
SMALL_FONT = ("CMU Serif", 6)

SIZE_Y=720
SIZE_X=1280

HOMEPAGEBG="#273746"
MENU_COLOR="#1B252F"

def find_min(x,y,window_size=10):
            min_index=np.argmin(y)
            #make a second order polynomial fit around the minimum and find the minimum of the fit
            x=x[min_index-window_size:min_index+window_size]
            y=y[min_index-window_size:min_index+window_size]
            fit=np.polyfit(x,y,2)
            xmin=-fit[1]/(2*fit[0])
            ymin=fit[0]*xmin**2+fit[1]*xmin+fit[2]
            return xmin,ymin

class Compensation(Windows):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller=controller
        self.parent=parent
        self.title=tk.Label(self,text="Compensation",font=LARGE_FONT,bg=HOMEPAGEBG,fg="white")
        self.title.pack(side='top',fill='x',pady=10, padx=10)
        self.compensation_file=self.select_file()
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
        self.canvas_main.draw()
        self.canvas_fit.draw()


    def load_data(self):
        Data=edf.Data(self.compensation_file,data_type="Compensation")
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
        window_size=[20]
        for i in range(0,len(self.by),2):
                xmin_fs,ymin_fs=find_min(self.by[i,:],self.r[i,:],window_size=window_size[0])
                xmin_bs,ymin_bs=find_min(self.by[i+1,:],self.r[i+1,:],window_size=window_size[0])
                self.xmin_list.append((xmin_fs+xmin_bs)/2)
                self.ymin_list.append((ymin_fs+ymin_bs)/2)
    def plot(self):
        fig,ax=matplotlib.pyplot.subplots(figsize=(15,5),dpi=100)
        cmap=matplotlib.pyplot.get_cmap("viridis")
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
        ax.plot(xplot,yplot,'-o')
        if len(yplot)>1:
            fit=np.polyfit(xplot,yplot,1)
            ax.plot(xplot,fit[0]*xplot+fit[1],"--")
            if isinstance(self.bx,type(None)):
                ax.set_xlabel("$\mathrm{B_z} \mathrm{(T)}$")
            else:
                ax.set_xlabel("$\mathrm{B_x} \mathrm{(T)}$")
            ax.set_ylabel("$\mathrm{B_y} \mathrm{(T)}$")
            ax.legend(["Data","Fit. \nSlope="+str(fit[0])+"\nIntercept="+str(fit[1])+r" $\mathrm{T}$"])
        elif len(yplot)==1:
            ax.legend(["{}".format(yplot)])
        return fig,ax
