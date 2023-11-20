import numpy as np

def read_data_2(name): #This is a new version for reading data. When the data is exported out directly from Sonnet.

    folder=''
    with open(folder+name,'r') as file:
        data_list=[] #Has three columns. The first one is the frequency, the second one is the magnitude and the third one is the phase.
        params_list=[] #Has the parameters of the simulation, in a dictionary.
        dict_params={}
        fq=[]
        s21=[]
        s21_phase=[]
        counter=0
        contador=0
        file_type=""
        vec=file.readlines()
        numberoflines=len(vec)
        if len(vec[2].split("="))==2:
            file_type="ParamSweep"
        else:
            file_type="SingleSweep"
        print(file_type)
        if file_type=="ParamSweep":
            for line in vec:#this will read the file line by line
                contador+=1
                if len(line.split("="))==2: #will save the parameters in a dictionary if the line is a parameter
                    counter=1
                    dict_params[line.split("=")[0]]=float(line.split("=")[1])
                elif len(line.split(","))==9 and counter==1: #will save the data in a list if the line is a data point and make the counter=1
                    fq.append(float(line.split(",")[0]))
                    s21.append(float(line.split(",")[5]))
                    s21_phase.append(float(line.split(",")[6]))
                    if contador==numberoflines-1:
                        counter=0
                        data_list.append(np.transpose(np.array([fq,s21,s21_phase])))
                        params_list.append(dict_params)
                        dict_params={}
                        fq=[]
                        s21=[]
                        s21_phase=[]
                elif counter==1: #if the line is not data and the counter is 1, it means that we have finished reading the data of a simulation and we can save it and reset the counter
                    counter=0
                    data_list.append(np.transpose(np.array([fq,s21,s21_phase])))
                    params_list.append(dict_params)
                    dict_params={}
                    fq=[]
                    s21=[]
                    s21_phase=[]
            file.close()
        elif file_type=="SingleSweep":
            for line in vec:
                contador+=1
                if contador>2:
                    try:
                        fq.append(float(line.split(",")[0]))
                        s21.append(float(line.split(",")[1]))
                        s21_phase.append(float(line.split(",")[2]))
                    except:
                        print(line.split(","))
                    if contador==numberoflines-1:
                        data_list.append(np.transpose(np.array([fq,s21,s21_phase])))
            file.close()
    return data_list,params_list

#Fit function 
def fit_function(params, f=None, dat1=None, dat2=None):
    
    fr = params['fr']
    Qc = params['Qc']
    Qi = params['Qi']
    phi0 = params['phi0']
    A = amplitude(f, fr, Qc, Qi)
    P = phase(f, fr, Qc, Qi, phi0)

    resid1 = dat1 - A
    resid2 = dat2 - P
    return np.concatenate((resid1, resid2))
def amplitude(f,fc,Q_c,Q_i):
    """ Compute the Amplitude from the parameter !!! compute the amplitude in magnitude !!!! """
    
    x=f/fc-fc/f  #
    a=Q_c/Q_i    #loss coef 
    S21=(2*Q_c*x/((1+a)**2+4*Q_c**2*x**2))**2 + (1-(1+a)/((1+a)**2+4*Q_c**2*x**2))**2
    
   # Sd=10*np.log(S21)   
    Sd = S21
    return Sd
##### fase

def phase(f,fc,Q_c,Q_i,phi0):
    
    x=f/fc-fc/f
    a=Q_c/Q_i
    arg=(2*Q_c*x)/(a*(a+1)+4*Q_c**2*x**2)
    theta=np.arctan(arg)
    
    return phi0+theta*180/np.pi
def tphase(f,fc,Q_c,Q_i):
    
    h=0.01
    tan=(phase(fc+h,fc,Q_c,Q_i)-phase(fc,fc,Q_c,Q_i))/h
    
    return phase(fc,fc,Q_c,Q_i)+tan*(f-fc)
def ttphase(fc,Q_c,Q_i):
    
    a=Q_c/Q_i
    tan=1/(a*(a+1))*(4*Q_c/fc)
    
    return tan
def tangente(f):
    
    recta=phase(f0,f0,Qc,Qi)+ttphase(f0,Qc,Qi)*(f-f0)
    
    return recta
def real(f,fc,Q_c,Q_i):
    
    x=(f/fc-fc/f)
    a=Q_c/Q_i
    arg=(a*(a+1)+4*Q_c**2*x**2)/((a+1)**2+4*Q_c**2*x**2)
 
    return arg
def imag(f,fc,Q_c,Q_i):
    
    x=(f/fc-fc/f)
    a=Q_c/Q_i
    arg2=2*Q_c*x/((a+1)**2+4*Q_c**2*x**2)
    
    return arg2
#data = 'data-resonator-fixedlength-fixedspacement-increasingdistbetweentlandres.csv'
#data='data-resonator-fixedlength-increasingspacement.csv'
