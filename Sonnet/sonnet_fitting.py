from Classes.windows import Windows
import Sonnet.Sliders as Sliders
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import  Slider, Button
import os
from lmfit import Parameters, minimize,fit_report
from scipy.signal import argrelextrema

def find_deeps(y):
    # Define a comparator for argrelextrema to find minima
    comparator = np.less

    # Find indices of relative minima
    indices = argrelextrema(y, comparator)

    return indices

class Sonnet(Windows):
    def __init__(self, root,controller):
        super().__init__(root,controller)
        self.i=0
        self.j=0
        self.filename=self.select_file()
        self.foldername=self.filename.split("/")[-1][:-4]
        self.read_data(self.filename)
        self.initialize_parameters()
        self.initialize_plot()
        self.initialize_sliders()
        self.create_buttons()
        self.set_title()
        plt.show()
    def update_frame(self):
        self.initialize_parameters()
        self.set_title()
        a_=self.init_fr
        b_ =self.init_Qc
        c_=self.init_Qi
        d_=self.init_phi0
        self.update_dataplot()
        self.update_plot(a_,b_,c_,d_)
    def forward(self,event):
        if(self.i<len(self.params)-1):
            self.i+=1
        self.update_frame()
    def backward(self,event): 
        if(self.i>0):
            self.i-=1
        self.update_frame()
    def change_min(self,event):
        if(self.j<len(self.deeps[0])-1):
            self.j+=1
        elif(self.j==len(self.deeps[0])-1):
            self.j=0
        else:
            print("There is only one minimum")
        self.update_frame()
    def fitandgo(self,funcs):
        def combined_func(*args, **kwargs):
            while(self.i<len(self.datas)-1):
                for j in range(5):
                    funcs[0](*args, **kwargs)
                funcs[1](*args, **kwargs)
                funcs[2](*args, **kwargs)
        return combined_func
    def read_data(self,sonnet_file):
        self.foldername=sonnet_file.split("/")[-1][:-4]
        self.datas,self.params=Sliders.read_data_2(sonnet_file)
    def initialize_parameters(self):
        f_ = self.datas[self.i][:,0]
        amp_ = np.exp(2*self.datas[self.i][:,1]/10)
        angle_ = self.datas[self.i][:,2]
        self.init_phi0= -50
        self.init_Qc = 100e3
        self.init_Qi =  0.1e6
        self.deeps=find_deeps(amp_)
        if len(self.deeps[0])>1:
            self.init_fr=f_[self.deeps[0][self.j]]
        else:
            self.init_fr=f_[np.argmin(amp_)]
        self.deltaphi=10
        self.deltafr=0.001
        self.deltaQc=40e3
        self.deltaQi=0.05e6


        f=[]
        amp=[]
        angle=[]
        
        for k in range(0, len(f_)): 
            if self.init_fr-0.001<f_[k] and f_[k]<self.init_fr+0.001 : 
                f.append(f_[k])
                amp.append(amp_[k])
                angle.append(angle_[k])
        self.f=np.array(f)
        self.amp=np.array(amp)
        self.angle=np.array(angle)
    def initialize_plot(self):
        self.fig, self.ax= plt.subplots(2, 1,sharex=True, figsize=(9, 8))
        self.ax=self.ax.ravel()
        self.amplitud_, =self.ax[0].plot(self.f, self.amp,'-o',markersize=1)
        self.fase_, =self.ax[1].plot(self.f, self.angle,'-o',markersize=1)
        self.line1, = self.ax[0].plot(self.f, Sliders.amplitude(self.f,self.init_fr,self.init_Qc,self.init_Qi), lw=2)
        self.line2, = self.ax[1].plot(self.f, Sliders.phase(self.f,self.init_fr,self.init_Qc,self.init_Qi,self.init_phi0), lw=2)
        self.ax[0].set_xlim([self.f[0],self.f[-1]])
        self.fig.subplots_adjust(left=0.25, bottom=0.25)
    def initialize_sliders(self):
        axfr = plt.axes([0.25, 0.1, 0.65, 0.03])
        fr_slider = Slider(
            ax=axfr,
            label='fr [Hz]',
            valmin=self.init_fr-self.deltafr,
            valmax=self.init_fr+self.deltafr,
            valinit=self.init_fr,
        )
        # Make a vertically oriented slider to control phi
        axphi = plt.axes([0.1, 0.25, 0.0225, 0.63])
        phi_slider = Slider(
            ax=axphi,
            label="Phi0 [rad]",
            valmin=self.init_phi0-self.deltaphi,
            valmax=self.init_phi0+self.deltaphi,
            valinit=self.init_phi0,
            orientation="vertical"
        )

        # Make a horizontal slider to control qc.
        axQc = plt.axes([0.25, 0.05, 0.65, 0.03])
        Qc_slider = Slider(
            ax=axQc,
            label='Qc',
            valmin=self.init_Qc-self.deltaQc,
            valmax=self.init_Qc+self.deltaQc,
            valinit=self.init_Qc,
        )

        # Make a vertically oriented slider to control Qi
        axQi = plt.axes([0.05, 0.25, 0.0225, 0.63])
        Qi_slider = Slider(
            ax=axQi,
            label="Qi",
            valmin=self.init_Qi-self.deltaQi,
            valmax=self.init_Qi+self.deltaQi,
            valinit=self.init_Qi,
            orientation="vertical"
        )
        self.sliders=[fr_slider,phi_slider,Qc_slider,Qi_slider]
        self.sliders_axis=[axfr,axphi,axQc,axQi]

        for slider in self.sliders:
            slider.on_changed(self.update)
    def update(self,event):
        self.line1.set_ydata(Sliders.amplitude(self.f, self.sliders[0].val,self.sliders[2].val,self.sliders[3].val))
        self.line2.set_ydata(Sliders.phase(self.f,self.sliders[0].val,self.sliders[2].val,self.sliders[3].val,self.sliders[1].val))
        self.fig.canvas.draw()
    def create_buttons(self):
        resetax = plt.axes([0.05, 0.075, 0.1, 0.04])
        parametsax = plt.axes([0.05, 0.025, 0.1, 0.04])
        fitax = plt.axes([0.05, 0.125, 0.1, 0.04])
        startaigan = plt.axes([0.05, 0.175, 0.1, 0.04])
        forwardax = plt.axes([0.9, 0.95, 0.04, 0.04])
        backwardax = plt.axes([0.1, 0.95, 0.04, 0.04])
        fitandgoax=plt.axes([0.9, 0.85, 0.04, 0.04])
        change_min=plt.axes([0.9, 0.75, 0.04, 0.04])


        button = Button(resetax, 'Reset', hovercolor='0.975')
        button2 = Button(parametsax, 'Get Parameters', hovercolor='0.975')
        button3 = Button(fitax, 'Fit', hovercolor='0.975')
        button4 = Button(startaigan, 'StartAgain', hovercolor='0.975')
        button5 = Button(forwardax, 'Go next', hovercolor='0.975')
        button6 = Button(backwardax, 'Go back', hovercolor='0.975')
        button7 = Button(fitandgoax, 'Fit and Go', hovercolor='0.975')
        button8 = Button(change_min, 'Change min', hovercolor='0.975')

        self.buttons=[button,button2,button3,button4,button5,button6,button7,button8]
        self.buttons_axis=[resetax,parametsax,fitax,startaigan,forwardax,backwardax,fitandgoax,change_min]
        self.buttons_functions=[self.reset,self.getpars,self.fit,self.start,self.forward,self.backward,self.fitandgo([self.fit,self.getpars,self.forward]),self.change_min]
        for i in range(len(self.buttons)):
            self.buttons[i].on_clicked(self.buttons_functions[i])
    def update_dataplot(self):
        self.amplitud_.set_xdata(self.f)
        self.amplitud_.set_ydata(self.amp)
        self.fase_.set_xdata(self.f)
        self.fase_.set_ydata(self.angle)
        self.line1.set_xdata(self.f)
        self.line2.set_xdata(self.f)
    def update_plot(self,a_,b_,c_,d_):
        self.line1.set_ydata(Sliders.amplitude(self.f, a_,b_,c_))
        self.line2.set_ydata(Sliders.phase(self.f,a_,b_,c_,d_))

        for axis in self.sliders_axis:
            axis.cla()
        
        self.sliders[0].__init__(ax=self.sliders_axis[0], label='fr[Hz]',valmin=a_-self.deltafr, valmax=a_+self.deltafr, valinit=a_,)
        self.sliders[1].__init__(ax=self.sliders_axis[1], label="Phi0 [rad]",valmin=d_-self.deltaphi,valmax=d_+self.deltaphi,valinit=d_,orientation="vertical")
        self.sliders[2].__init__(ax=self.sliders_axis[2], label='Qc',valmin=b_-self.deltaQc,valmax=b_+self.deltaQc,valinit=b_)
        self.sliders[3].__init__(ax=self.sliders_axis[3], label='Qi',valmin=c_-self.deltaQi,valmax=c_+self.deltaQi,valinit=c_,orientation="vertical")

        for slider in self.sliders:
            slider.on_changed(self.update)
        self.fig.canvas.draw()
    def reset(self,event):
            for slider in self.sliders:
                slider.reset()
    def getpars(self,event):
        name=''
        if self.params!=[]:
            for j in list(self.params[self.i].values()):
                name=name+str(j)+","
            name=name[:-1]
        else:
            name='SonnetSimulation'
        file=self.foldername+name+".txt"
        #create a folder named "datos" in the same directory as the script
        if not os.path.exists(self.foldername):
            os.makedirs(self.foldername)
        with open(self.foldername+"/"+file,'w') as o:
            print('fr',self.sliders[0].val,file=o)
            print('phi',self.sliders[1].val,file=o)
            print('Qc',self.sliders[2].val,file=o)
            print('Qi',self.sliders[3].val,file=o)                            
    def fit(self,event):
        parames = Parameters()
        parames.add('fr', value=self.sliders[0].val)
        parames.add('Qc', value=self.sliders[2].val)
        parames.add('Qi', value=self.sliders[3].val)
        parames.add('phi0', value=self.sliders[1].val)
        out = minimize(Sliders.fit_function, parames, kws={"f": self.f, "dat1":self.amp, "dat2": self.angle})
        a_=out.params['fr'].value
        b_ = out.params['Qc'].value
        c_= out.params['Qi'].value
        d_= out.params['phi0'].value
        self.update_plot(a_,b_,c_,d_)
    def start(self,event):
        a_=self.init_fr
        b_ =self.init_Qc
        c_=self.init_Qi
        d_=self.init_phi0
        self.update_plot(a_,b_,c_,d_)
    def set_title(self):
        title=""
        if self.params!=[]:
            for llave in list(self.params[self.i].keys()):
                title+=llave+": "+str(self.params[self.i][llave])+" "
        self.fig.suptitle(title, fontsize=16)