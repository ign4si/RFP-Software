import numpy as np
import pandas as pd
class Dataframe:
    def __init__(self,root):
        self.root=root
        self.update()
class SweepsDataframe(Dataframe):
    def __init__(self,root):
        Dataframe.__init__(self,root)
    def update(self):
        sweep_list=[int(self.root.parameters["sweep_ini"]),int(self.root.parameters["sweep_end"]),int(self.root.parameters["sweep_step"])]
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
        self.df=pd.DataFrame({'Number of sweeps': self.root.nsimus,'Number of points per sweep': self.root.npoints})
class ParametersDataframe(Dataframe):
    def __init__(self,root):
        Dataframe.__init__(self,root)
    def update(self):
        port=self.root.port
        print(self.root.index_crop)
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

