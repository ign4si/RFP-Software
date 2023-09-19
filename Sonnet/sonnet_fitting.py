from ..Classes.windows import Windows
import Sliders
import numpy as np

class Sonnet(Windows):
    def __init__(self, root,controller):
        super().__init__(root,controller)
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
    def initialize_parameters(self):

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
        #define a dictionary with all the parameters
        
