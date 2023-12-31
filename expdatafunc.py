import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from resonator_tools import circuit
labels=["temperature","power","bandwidth","Bx","By","Bz","freq","Re_S21","Im_S21","amplitude","phase"]
labels_datacomp=["temperature","Ix","Iy","Ux","Uy","R","Bx","By","Bz","time"]
class Data:
    def __init__(self,path,data_type=None,freq_column=None,verbose=False):
        if data_type==None:
            Data,number_of_points_list,number_of_simus_list,number_of_files=TakeDataNew(path,verbose=verbose)
            self.temp=Data[0]
            self.power=Data[1]
            self.bandwidth=Data[2]
            self.bx=Data[3]
            self.by=Data[4]
            self.bz=Data[5]
            self.freq=Data[6]
            self.real=Data[7]
            self.imag=Data[8]
            self.S21_DB=Data[9]
            self.phase=Data[10]
            self.number_of_simus=number_of_simus_list
            self.number_of_points=number_of_points_list
            self.number_of_files=number_of_files
            self.S21=[10**(i/20) for i in self.S21_DB]
            try:
                hola=1j*self.phase
                hola=hola.astype(complex)
                self.z=[self.S21[i]*np.exp(hola[i]) for i in range(len(self.S21))]
            except:
                self.z=[self.S21[i]*np.exp(1j*self.phase[i]) for i in range(len(self.S21))]
        if data_type=="Compensation":
            Data=read_datacomp(path)
            self.temp=Data[0]
            self.ix=Data[1]
            self.iy=Data[2]
            self.ux=Data[3]
            self.uy=Data[4]
            self.r=Data[5]
            self.bx=Data[6]
            self.by=Data[7]
            self.bz=Data[8]
            self.time=Data[9]

def read_datacomp(filename):
    global labels_datacomp
    data = np.loadtxt(filename, skiprows=1)
    with open(filename) as f:
        header = f.readline().split()[1:]
    index_list=[]
    column_list=[]
    #read labels
    for i in range(len(labels_datacomp)):
        try:
            index_list.append(header.index(labels_datacomp[i]))
            column_list.append(data[:,index_list[i]])
        except:
            index_list.append(None)
            column_list.append(None)
    #calculate the number of sweeps and points per sweep
    try:
        number_of_sweeps=len(np.where(np.diff(column_list[7])==0)[0]+1)+1
        number_of_points_per_sweep=len(column_list[0])//number_of_sweeps
    except:
        number_of_sweeps=1
        number_of_points_per_sweep=len(column_list[0])
    #reshape the data
    for i in range(len(labels_datacomp)):
        if index_list[i]!=None:
            column_list[i]=np.reshape(column_list[i],(number_of_sweeps,number_of_points_per_sweep))
    return column_list
    

def ReadFiles(filename):
    data = []
    headings=[]
    data.append(np.loadtxt(filename,skiprows=1))
    with open(filename) as f:
        first_line=f.readline()
    headings.append(first_line.split()[1:])
    return data,headings

        
def TakeDataNew(path,verbose=False):
    global labels
    data,headings=ReadFiles(path)
    number_of_files=1
    #find the index of the labels in the headings
    index_list=[]
    for i in range(len(labels)):
        try:
            index_list.append(headings[0].index(labels[i]))
        except:
            index_list.append(None)
    columns_list=[]#same labelling as the labels list

    number_of_points_list=[]
    number_of_simus_list=[]
    for datas in data: #sweeping in the datafiles
        for i in range(len(labels)):
            if index_list[i]!=None:
                columns_list.append(datas[:,index_list[i]])
            else:
                columns_list.append(None)
        #try to do the calculation of the number of points, but in case the np.where function does not find the point, it will return the number of points as the number of data points
        try:
            number_of_points=np.where(np.abs(np.diff(np.diff(columns_list[6])))>5)[0][0]+2
            number_of_simus=len(columns_list[6])//number_of_points
        except:
            number_of_points=len(columns_list[6])
            number_of_simus=1    

        for i in range(len(labels)):
            if index_list[i]!=None:
                columns_list[i]=columns_list[i].reshape(number_of_simus,number_of_points)
        number_of_points_list.append(number_of_points)
        number_of_simus_list.append(number_of_simus)
    number_of_points_list=np.array(number_of_points_list)
    number_of_simus_list=np.array(number_of_simus_list)
    
    
    return columns_list,number_of_points_list,number_of_simus_list,number_of_files
def TakeDataCW(path):
    data=ReadFiles(path,sort=False)
    time_list=[]
    real_list=[]
    imag_list=[]
    amplitude_list=[]
    phase_list=[]
    for datas in data: #sweeping in the datafiles
        time=datas[:,0]
        real=datas[:,1]
        imag=datas[:,2]
        amplitude=datas[:,3]
        phase=datas[:,4]
        time_list.append(time)
        real_list.append(real)
        imag_list.append(imag)
        amplitude_list.append(amplitude)
        phase_list.append(phase)




    return time_list,real_list,imag_list,amplitude_list,phase_list

def TakeDataCWPower(path,verbose=False):
    data=ReadFiles(path,sort=False,verbose=verbose)
    time_list=[]
    power_list=[]
    bandwidth_list=[]
    real_list=[]
    imag_list=[]
    amplitude_list=[]
    phase_list=[]
    for datas in data: #sweeping in the datafiles
        time=datas[:,0]
        power=datas[:,1]
        bandwidth=datas[:,2]
        real=datas[:,3]
        imag=datas[:,4]
        amplitude=datas[:,5]
        phase=datas[:,6]
        number_of_points=np.where(np.diff(np.diff(power))!=0)[0][0]+2
        number_of_simus=len(power)//number_of_points
        time=time.reshape(number_of_simus,number_of_points)
        power=power.reshape(number_of_simus,number_of_points)
        bandwidth=bandwidth.reshape(number_of_simus,number_of_points)
        real=real.reshape(number_of_simus,number_of_points)
        imag=imag.reshape(number_of_simus,number_of_points)
        amplitude=amplitude.reshape(number_of_simus,number_of_points)
        phase=phase.reshape(number_of_simus,number_of_points)

        time_list.append(time)
        power_list.append(power)
        bandwidth_list.append(bandwidth)
        real_list.append(real)
        imag_list.append(imag)
        amplitude_list.append(amplitude)
        phase_list.append(phase)
    if verbose:
        print("number of sweeps: ",number_of_simus,"\nnumber of points for each simulation: ",number_of_points)
        print("So the total number of points should be: ",number_of_simus*number_of_points)
    return time_list,power_list,bandwidth_list,real_list,imag_list,amplitude_list,phase_list

def plot_CW_3(data_object,data_object2,sweep1,sweep2,fq,extra_title="",title1="",title2="",xlim1=None,ylim1=None,xlim2=None,ylim2=None,shift1=0,shift2=0,cmap="jet",savefig=None,dataindex1=[],dataindex2=[]):
    fig,ax=plt.subplots(1,2,figsize=(15,7))
    axes=ax.flatten()
    cmap=plt.get_cmap(cmap)
    colors=[cmap(i) for i in np.linspace(0,1,len(data_object.power[sweep1]))]
    if dataindex1==[]:
        for i in range(len(data_object.power[sweep1])-1,-1,-1):
            x=data_object.time[sweep1][i]
            y=data_object.S21_DB[sweep1][i]
            axes[0].plot(x,y,color=colors[i],label="P={:.2f}dBm".format(data_object.power[sweep1][i][0]+shift1))
    else:
        for i in dataindex1:
            x=data_object.time[sweep1][i]
            y=data_object.S21_DB[sweep1][i]
            axes[0].plot(x,y,color=colors[i],label="P={:.2f}dBm".format(data_object.power[sweep1][i][0]+shift1))
    axes[0].set_title(title1+"Continuous wave in resonance in Resonator fq={} GHz".format(fq))
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("S21 (DB)")
    axes[0].legend()
    axes[0].set_xlim(0,data_object.time[sweep1][-1][-1])
    axes[0].grid()
    if(xlim1!=None):
        axes[0].set_xlim(xlim1)
    if(ylim1!=None):
        axes[0].set_ylim(ylim1)

    #do the same as above for the second data object
    cmap=plt.get_cmap(cmap)
    colors=[cmap(i) for i in np.linspace(0,1,len(data_object2.power[sweep2]))]
    if dataindex2==[]:
        for i in range(len(data_object2.power[sweep2])-1,-1,-1):
            x=data_object2.time[sweep2][i]
            y=data_object2.S21_DB[sweep2][i]
            axes[1].plot(x,y,color=colors[i],label="P={:.2f}dBm".format(data_object2.power[sweep2][i][0]+shift2))
    else:
        for i in dataindex2:
            x=data_object2.time[sweep2][i]
            y=data_object2.S21_DB[sweep2][i]
            axes[1].plot(x,y,color=colors[i],label="P={:.2f}dBm".format(data_object2.power[sweep2][i][0]+shift2))
    axes[1].set_title(title2+"Continuous wave in resonance in Resonator fq={} GHz".format(fq))
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("S21 (DB)")
    axes[1].legend()
    axes[1].set_xlim(0,data_object2.time[sweep2][-1][-1])
    axes[1].grid()

    if(xlim2!=None):
        axes[1].set_xlim(xlim2)
    if(ylim2!=None):
        axes[1].set_ylim(ylim2)



    #set the bandwith as a suptitle
    plt.suptitle(extra_title+"Bandwidth={:.2f}Hz".format(data_object.bandwidth[sweep1][0][0])+"; Bandwidth2={:.2f}Hz".format(data_object2.bandwidth[sweep2][0][0]))
    if(savefig!=None):
        plt.savefig(savefig)

    plt.show()

def FreqShift(data_object,skip_indexes=[],double_plot=False,file=0,shift=0,figsize=(10,10),cmap='gnuplot',sweep="T",dB_plot=False,fit=True,fr_min=False,fcrop1=None,fcrop2=None,start=0,end=-1,step=2,title='',guessdelay=False,plot_fit_results=True,legend=True,invert_colorbar=False,fit_range=(0,-1,1),savefig1=None,savefig2=None):
    #this function selects the file 0 in the data object
    if end<0:
        end=len(data_object.freq[file])+end+1

    if sweep=="T":
        last_value=data_object.temp[file][end-1][0]
        first_value=data_object.temp[file][start][0]
    elif sweep=="P":
        last_value=data_object.power[file][end-1][0]
        first_value=data_object.power[file][start][0]
    else:
        raise ValueError("sweep must be either T or P")

    cmap=plt.get_cmap(cmap)
    if double_plot==False:
        plt.figure(figsize=figsize)
    else:
        fig,axe=plt.subplots(1,2,figsize=figsize,sharey=True,sharex=True)
        axes=axe.ravel()
    if invert_colorbar==True:
        colors=colors[::-1]
    temp_list=[]
    power_list=[]
    fr_list=[]
    frmin_list=[]
    Qi_list=[]
    Qc_list=[]
    fr_list_err=[]
    Qi_list_err=[]
    Qc_list_err=[]
    endi=0
    for i in range(start,end,step):
        if i in skip_indexes:
            continue
        x_=np.array(data_object.freq[file][i]) 
        y_=data_object.z[file][i]
        if fit==True:
            if fcrop1!=None and fcrop2!=None:
                cond=np.logical_and(x_>fcrop1,x_<fcrop2)
                x=x_[cond]
                y=y_[cond]
            else:
                x=x_
                y=y_
            port1=circuit.notch_port(x,y)
            try:
                port1.autofit(guessdelay=guessdelay)
                x_fit=port1.f_data
                z_fit=port1.z_data_sim
                Qi=port1.fitresults['Qi_dia_corr']
                Qi_err=port1.fitresults['Qi_dia_corr_err']
                Qc=port1.fitresults['absQc']
                Qc_err=port1.fitresults['absQc_err']
                fr=port1.fitresults['fr']
                fr_err=port1.fitresults['fr_err']
            
                fr_list.append(fr)
                Qi_list.append(Qi)
                Qc_list.append(Qc)
                fr_list_err.append(fr_err)
                Qi_list_err.append(Qi_err)
                Qc_list_err.append(Qc_err)
            except:
                print("Fit failed for T={} K. Iteration i={}".format(data_object.temp[file][i][0],i))
                fr_list.append(np.nan)
                Qi_list.append(np.nan)
                Qc_list.append(np.nan)
                fr_list_err.append(np.nan)
                Qi_list_err.append(np.nan)
                Qc_list_err.append(np.nan)
        if double_plot==False:
            if sweep=="T":
                if dB_plot==False:
                    plt.plot(x_/1e9,(np.abs(y_)-shift*i),color=cmap((data_object.temp[file][i][0]-first_value)/(last_value-first_value)))
                else:
                    plt.plot(x_/1e9,20*np.log10(np.abs(y_))-shift*i,color=cmap((data_object.temp[file][i][0]-first_value)/(last_value-first_value)))

            elif sweep=="P":
                if dB_plot==False:
                    plt.plot(x_/1e9,(np.abs(y_)-shift*i),color=cmap((data_object.power[file][i][0]-first_value)/(last_value-first_value)))
                else:
                    plt.plot(x_/1e9,20*np.log10(np.abs(y_))-shift*i,color=cmap((data_object.power[file][i][0]-first_value)/(last_value-first_value)))
            else:
                raise ValueError("sweep must be either T or P")
        else:
            if sweep=="T":
                if dB_plot==False:
                    axes[0].plot(x_/1e9,(np.abs(y_)-shift*i),color=cmap((data_object.temp[file][i][0]-first_value)/(last_value-first_value)))
                    axes[1].plot(x/1e9,(np.abs(z_fit)-shift*i),'--',color=cmap((data_object.temp[file][i][0]-first_value)/(last_value-first_value)))
                else:
                    axes[0].plot(x_/1e9,20*np.log10(np.abs(y_))-shift*i,color=cmap((data_object.temp[file][i][0]-first_value)/(last_value-first_value)))
                    axes[1].plot(x/1e9,20*np.log10(np.abs(z_fit))-shift*i,'--',color=cmap((data_object.temp[file][i][0]-first_value)/(last_value-first_value)))

            elif sweep=="P":
                if dB_plot==False:
                    axes[0].plot(x_/1e9,(np.abs(y_)-shift*i),color=cmap((data_object.power[file][i][0]-first_value)/(last_value-first_value)))
                    axes[1].plot(x/1e9,(np.abs(z_fit)-shift*i),'--',color=cmap((data_object.power[file][i][0]-first_value)/(last_value-first_value)))
                else:
                    axes[0].plot(x_/1e9,20*np.log10(np.abs(y_))-shift*i,color=cmap((data_object.power[file][i][0]-first_value)/(last_value-first_value)))
                    axes[1].plot(x/1e9,20*np.log10(np.abs(z_fit))-shift*i,'--',color=cmap((data_object.power[file][i][0]-first_value)/(last_value-first_value)))
            else:
                raise ValueError("sweep must be either T or P")

        frmin=x_[np.argmin(np.abs(y_))]
        frmin_list.append(frmin)
        temp_list.append(data_object.temp[file][i][0])
        power_list.append(data_object.power[file][i][0])
        endi=i
        


    temp_list=np.array(temp_list)
    fr_list=np.array(fr_list)
    frmin_list=np.array(frmin_list)
    Qi_list=np.array(Qi_list)
    Qc_list=np.array(Qc_list)
    fr_list_err=np.array(fr_list_err)
    Qi_list_err=np.array(Qi_list_err)
    Qc_list_err=np.array(Qc_list_err)

    if title!='':
        plt.suptitle(title)
    plt.xlabel("Frequency (GHz)")
    if shift==0:
        if dB_plot==False:
            axes[0].set_ylabel("S21")
        else:
            axes[0].set_ylabel("S21 (dB)")
        
    else:
        if dB_plot==False:
            axes[0].set_ylabel("S21 shifted")
            axes[0].set_yticks([])
        else:
            axes[0].set_ylabel("S21 (dB) shifted ")
            axes[0].set_yticks([])
    #put a colorbar on the plot
    if sweep=="T":
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=first_value, vmax=last_value))
        cbar=plt.colorbar(sm,ticks=np.linspace(first_value,last_value,10))
    if sweep=="P":
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=first_value, vmax=last_value))
        cbar=plt.colorbar(sm,ticks=np.linspace(first_value,last_value,10))
    #put a title in the colorbar
    
    if sweep=="T":
        cbar.set_label("Temperature (K)")
    if sweep=="P":
        cbar.set_label("Power (dBm)")


    axes[0].grid()
    axes[1].grid()
    if savefig1!=None:
        plt.savefig(savefig1)
    plt.show()
    if plot_fit_results:
        if fit==True:
            fig,axels=plt.subplots(1,3,figsize=(15,5))
            ax=[axels[0],axels[1],axels[2]]
            if sweep=="T":
                if fr_min==False:
                    ax[0].errorbar(temp_list[fit_range[0]:fit_range[1]:fit_range[2]],fr_list[fit_range[0]:fit_range[1]:fit_range[2]]/1e9,yerr=fr_list_err[fit_range[0]:fit_range[1]:fit_range[2]]/1e9,fmt='-o')
                    ax[0].set_xlabel("Temperature (K)")
                    ax[0].set_ylabel("Frequency (GHz)")
                    ax[0].grid()
                else:
                    ax[0].plot(temp_list,frmin_list/1e9,'-o')
                    ax[0].set_xlabel("Temperature (K)")
                    ax[0].set_ylabel("Frequency (GHz)")
                    ax[0].grid()
                ax[1].errorbar(temp_list[fit_range[0]:fit_range[1]:fit_range[2]],Qi_list[fit_range[0]:fit_range[1]:fit_range[2]],yerr=Qi_list_err[fit_range[0]:fit_range[1]:fit_range[2]],fmt='-o')
                ax[1].set_xlabel("Temperature (K)")
                ax[1].set_ylabel("Qi")
                ax[1].grid()
                ax[2].errorbar(temp_list[fit_range[0]:fit_range[1]:fit_range[2]],Qc_list[fit_range[0]:fit_range[1]:fit_range[2]],yerr=Qc_list_err[fit_range[0]:fit_range[1]:fit_range[2]],fmt='-o')
                ax[2].set_xlabel("Temperature (K)")
                ax[2].set_ylabel("Qc")
                ax[2].grid()
            if sweep=="P":
                if fr_min==False:
                    ax[0].errorbar(power_list[fit_range[0]:fit_range[1]:fit_range[2]],fr_list[fit_range[0]:fit_range[1]:fit_range[2]]/1e9,yerr=fr_list_err[fit_range[0]:fit_range[1]:fit_range[2]]/1e9,fmt='-o')
                    ax[0].set_xlabel("Power (dBm)")
                    ax[0].set_ylabel("Frequency (GHz)")
                    ax[0].grid()
                else:
                    ax[0].plot(power_list,frmin_list/1e9,'-o')
                    ax[0].set_xlabel("Power (dBm)")
                    ax[0].set_ylabel("Frequency (GHz)")
                    ax[0].grid()
                ax[1].errorbar(power_list[fit_range[0]:fit_range[1]:fit_range[2]],Qi_list[fit_range[0]:fit_range[1]:fit_range[2]],yerr=Qi_list_err[fit_range[0]:fit_range[1]:fit_range[2]],fmt='-o')
                ax[1].set_xlabel("Power (dBm)")
                ax[1].set_ylabel("Qi")
                ax[1].grid()
                ax[2].errorbar(power_list[fit_range[0]:fit_range[1]:fit_range[2]],Qc_list[fit_range[0]:fit_range[1]:fit_range[2]],yerr=Qc_list_err[fit_range[0]:fit_range[1]:fit_range[2]],fmt='-o')
                ax[2].set_xlabel("Power (dBm)")
                ax[2].set_ylabel("Qc")
                ax[2].grid()
        else:
            fig,ax=plt.subplots(1,1,figsize=(10,5))
            if sweep=="T":
                ax.plot(temp_list,frmin_list/1e9,'-o')
                ax.set_xlabel("Temperature (K)")
                ax.set_ylabel("Frequency (GHz)")
                ax.grid()
            if sweep=="P":
                ax.plot(power_list,frmin_list/1e9,'-o')
                ax.set_xlabel("Power (dBm)")
                ax.set_ylabel("Frequency (GHz)")
                ax.grid()
        
        if title!='':
            plt.suptitle(title)
        if savefig2!=None:
            plt.savefig(savefig2)
        plt.show()

def FreqShiftComparison(data_object1,data_object2,cmap1='gnuplot',cmap2='gnuplot',guessdelay1=False,guessdelay2=False,start1=0,end1=-1,step1=2,start2=0,end2=-1,step2=2,suptitle='',label1='data1',label2='data2',title1='',title2='',plot_fit_results=True,legend=True,invert_colorbar1=False,invert_colorbar2=False,savefig1=None,savefig2=None,sharex=True,sharey=False):
    cmap1_=plt.get_cmap(cmap1)
    cmap2_=plt.get_cmap(cmap2)
    fig,ax=plt.subplots(2,1,figsize=(10,10),sharex=sharex)
    axes=ax.flatten()
    colors1=[cmap1_(i) for i in np.linspace(0,1,len(data_object1.freq[0]))]
    colors2=[cmap2_(i) for i in np.linspace(0,1,len(data_object2.freq[0]))]
    if invert_colorbar1==True:
        colors1=colors1[::-1]
    if invert_colorbar2==True:
        colors2=colors2[::-1]

    temp_list1=[]
    fr_list1=[]
    Qi_list1=[]
    Qc_list1=[]
    fr_list_err1=[]
    Qi_list_err1=[]
    Qc_list_err1=[]

    temp_list2=[]
    fr_list2=[]
    Qi_list2=[]
    Qc_list2=[]
    fr_list_err2=[]
    Qi_list_err2=[]
    Qc_list_err2=[]

    if end1==-1:
        end1=len(data_object1.freq[0])
    if end2==-1:
        end2=len(data_object2.freq[0])

    for i in range(start1,end1,step1):
        x=np.array(data_object1.freq[0][i]) 
        y=data_object1.z[0][i]
        port1=circuit.notch_port(x,y)

        port1.autofit(guessdelay=guessdelay1)
        Qi=port1.fitresults['Qi_dia_corr']
        Qi_err=port1.fitresults['Qi_dia_corr_err']
        Qc=port1.fitresults['absQc']
        Qc_err=port1.fitresults['absQc_err']
        fr=port1.fitresults['fr']
        fr_err=port1.fitresults['fr_err']
        axes[0].plot(x,(np.abs(y)),color=colors1[i],label="T={:.2f}K P={:.2f}dBm Qi={:.2f} Qc={:.2f} fr={:.4f}GHz".format(data_object1.temp[0][i][0],data_object1.power[0][i][0],Qi,Qc,fr/1e9))
        #plot fr vs T
        temp_list1.append(data_object1.temp[0][i][0])
        fr_list1.append(fr)
        Qi_list1.append(Qi)
        Qc_list1.append(Qc)
        fr_list_err1.append(fr_err)
        Qi_list_err1.append(Qi_err)
        Qc_list_err1.append(Qc_err)

    for i in range(start2,end2,step2):
        x=np.array(data_object2.freq[0][i]) 
        y=data_object2.z[0][i]
        port2=circuit.notch_port(x,y)

        port2.autofit(guessdelay=guessdelay2)
        Qi=port2.fitresults['Qi_dia_corr']
        Qi_err=port2.fitresults['Qi_dia_corr_err']
        Qc=port2.fitresults['absQc']
        Qc_err=port2.fitresults['absQc_err']
        fr=port2.fitresults['fr']
        fr_err=port2.fitresults['fr_err']
        axes[1].plot(x,(np.abs(y)),color=colors2[i],label="T={:.2f}K P={:.2f}dBm Qi={:.2f} Qc={:.2f} fr={:.4f}GHz".format(data_object2.temp[0][i][0],data_object2.power[0][i][0],Qi,Qc,fr/1e9))
        #plot fr vs T
        temp_list2.append(data_object2.temp[0][i][0])
        fr_list2.append(fr)
        Qi_list2.append(Qi)
        Qc_list2.append(Qc)
        fr_list_err2.append(fr_err)
        Qi_list_err2.append(Qi_err)
        Qc_list_err2.append(Qc_err)

    temp_list1=np.array(temp_list1)
    fr_list1=np.array(fr_list1)
    Qi_list1=np.array(Qi_list1)
    Qc_list1=np.array(Qc_list1)
    fr_list_err1=np.array(fr_list_err1)
    Qi_list_err1=np.array(Qi_list_err1)
    Qc_list_err1=np.array(Qc_list_err1)

    temp_list2=np.array(temp_list2)
    fr_list2=np.array(fr_list2)
    Qi_list2=np.array(Qi_list2)
    Qc_list2=np.array(Qc_list2)
    fr_list_err2=np.array(fr_list_err2)
    Qi_list_err2=np.array(Qi_list_err2)
    Qc_list_err2=np.array(Qc_list_err2)


    
    if legend:
        plt.legend()
    if title1!='':
        axes[0].set_title(title1)
    if title2!='':
        axes[1].set_title(title2)
    if sharex:
        axes[1].set_xlabel("Frequency (GHz)")
    else:
        axes[0].set_xlabel("Frequency (GHz)")
        axes[1].set_xlabel("Frequency (GHz)")

    axes[0].set_ylabel("S_{21}")
    axes[1].set_ylabel("S_{21}")

    #put a colorbar on each plot
    sm = plt.cm.ScalarMappable(cmap=cmap1_, norm=plt.Normalize(vmin=np.min(temp_list1), vmax=np.max(temp_list1)))
    sm._A = []
    cbar1=plt.colorbar(sm,ax=axes[0])
    cbar1.set_label("Temperature (K)")
    sm = plt.cm.ScalarMappable(cmap=cmap2_, norm=plt.Normalize(vmin=np.min(temp_list2), vmax=np.max(temp_list2)))
    sm._A = []
    cbar2=plt.colorbar(sm,ax=axes[1])
    cbar2.set_label("Temperature (K)")




    axes[0].grid()
    axes[1].grid()
    if savefig1!=None:
        plt.savefig(savefig1)
    plt.show()
    if plot_fit_results:
        fig,ax=plt.subplots(1,3,figsize=(15,5))
        ax[0].errorbar(temp_list1,fr_list1/1e9,yerr=fr_list_err1/1e9,fmt='-o',label=label1)
        ax[0].errorbar(temp_list2,fr_list2/1e9,yerr=fr_list_err2/1e9,fmt='-o',label=label2)
        ax[0].set_xlabel("Temperature (K)")
        ax[0].set_ylabel("Frequency (GHz)")
        ax[0].grid()
        ax[1].errorbar(temp_list1,Qi_list1,yerr=Qi_list_err1,fmt='-o',label=label1)
        ax[1].errorbar(temp_list2,Qi_list2,yerr=Qi_list_err2,fmt='-o',label=label2)
        ax[1].set_xlabel("Temperature (K)")
        ax[1].set_ylabel("Qi")
        ax[1].grid()
        ax[2].errorbar(temp_list1,Qc_list1,yerr=Qc_list_err1,fmt='-o',label=label1)
        ax[2].errorbar(temp_list2,Qc_list2,yerr=Qc_list_err2,fmt='-o',label=label2)
        ax[2].set_xlabel("Temperature (K)")
        ax[2].set_ylabel("Qc")
        ax[2].grid()
        if suptitle!='':
            plt.suptitle(suptitle)
        plt.legend()
        if savefig2!=None:
            plt.savefig(savefig2)

        
        plt.show()

def CalculateTc(data,value,line=1,file=0,start=0,end=-1,step=1,savefig=None):
    #function that find a value in a list closest to a given value
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    S21_DB=[]   
    temp=[]
    if end<0:
        end=len(data.freq[file])+end+1
    for i in range(start,end,step):
        x=data.freq[file][i]
        z=data.S21_DB[file][i]
        idx=find_nearest(x,value)
        S21_DB.append(z[idx])
        temp.append(data.temp[file][i][0])
    plt.plot(temp,S21_DB,'-o')
    plt.xlabel("Temperature (K)")
    plt.ylabel("S21 (dB)")
    plt.title("S21 at {} GHz".format(value/1e9))
    meanpoint=(S21_DB[0]-S21_DB[-1])/2+S21_DB[-1]
    plt.axhline(y=meanpoint,color='r',linestyle='--')
    #find the temperature at which the S21 is at the mean point
    idx=find_nearest(S21_DB,meanpoint)
    #make a straight line between temp[idx] and temp[idx+line]
    m=(temp[idx+line]-temp[idx])/(S21_DB[idx+line]-S21_DB[idx])
    b=temp[idx]-m*S21_DB[idx]
    temp_mean=m*meanpoint+b
    idxmas=idx+line
    idxmenos=idx
    print("Temperature at which the S21 is at the mean point is {} K. The transition is between: {} K and {} K".format(temp_mean,temp[idxmenos],temp[idxmas]))
    plt.axvline(x=temp[idxmenos],color='g',linestyle='--',label="$T_{{c,\mathrm{{start}}}}={}$ K".format(temp[idxmenos]))
    plt.axvline(x=temp[idxmas],color='b',linestyle='--',label="$T_{{c,\mathrm{{end}}}}={}$ K".format(temp[idxmas]))
    plt.axvline(x=temp_mean,color='orange',linestyle='--',label="$T_c={}$ K".format(temp_mean))
    plt.legend()
    if savefig!=None:
        plt.savefig(savefig,dpi=300)
    plt.show()


def Fit(f_data_1,z_data_1,showfits=False):
    from resonator_tools import circuit
    port1=circuit.notch_port(f_data_1,z_data_1)
    results=port1.do_calibration(f_data_1,z_data_1)

    z_data_1_normalized=port1.do_normalization(f_data_1,z_data_1,results[0],results[1],results[2],0,0)
    results1=port1.circlefit(f_data_1,z_data_1_normalized,results[3],results[4])
    tau=results[0]
    a=results[1]
    alpha=results[2]
    Qi=results1["Qi_dia_corr"]
    Qc=results1["Qc_dia_corr"]
    Ql=results1["Ql"]
    fr=results1["fr"]
    phi=results1["theta0"]+np.pi
    if showfits==True:
        S21fit=a*np.exp(np.complex(0,alpha))*np.exp(-2j*np.pi*f_data_1*tau)*(1.-Ql/Qc*np.exp(1j*phi)/(1.+2j*Ql*(f_data_1-fr)/fr))
        plt.figure(figsize=(10,10))
        plt.plot(f_data_1,np.abs(z_data_1),label="data")
        plt.plot(f_data_1,np.abs(S21fit),label="fit")
        plt.xlabel("Frequency (GHz)")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.show()
    return results1