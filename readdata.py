import os
import glob
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
from scipy import signal
from order4_keybits_to_HL import order4_keybits_to_HL
from patternClassification import patternClassification_v2
from correlation_vs_model import correlation_vs_model_v2
from order4_HL_to_keybits import order4_HL_to_keybits
from printHex256bits import printHex256bits
from scipy.interpolate import interp1d
import time


#t=time
#x=power consuption
#y=trigger
model_raw_power = pd.read_csv('ecc_order4_256_avg64.csv',header=23,names = ('t','x'))
model_raw_trigger = pd.read_csv('ecc_order4_256_avg64_trig.csv',header=23,names = ('t','y'))

unknown_raw_power = pd.read_csv('ecc_order4_256_avg64_data2.csv',header=23, names=('t','x'))
unknown_raw_trigger = pd.read_csv('ecc_order4_256_avg64_data2_trig.csv',header=23, names=('t','y'))

debut= time.time()
#if the sampling frequency of testing dataset is lower than the one for training dataset, we should do an interpolation to match the total number of points
#we create interpolation for power and trigger so the data is the same size as training data (we lose time information)
t_interpolate=np.linspace(unknown_raw_power.t.iloc[0],unknown_raw_power.t.iloc[-1],len(model_raw_power.t))#same time array as unknown raw power but with the number of point of model raw power
f_power=interp1d(unknown_raw_power.t,unknown_raw_power.x,kind='cubic')
f_trigger=interp1d(unknown_raw_power.t,unknown_raw_trigger.y)
unknwon_inter_power=f_power(t_interpolate)#interpolation of power trace of unknown attack
unknown_inter_trigger=f_trigger(t_interpolate)#interpolation of trigger trace of unknwon attack
fin= time.time()
print("interpolation time : ",fin-debut)

plt.figure()
plt.title('Training set')
plt.plot(model_raw_power.t,model_raw_power.x,model_raw_trigger.t,model_raw_trigger.y)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Ladderstep'),loc='best')
plt.figure()
plt.title('Test set')
plt.plot(t_interpolate,unknwon_inter_power,t_interpolate,unknown_inter_trigger)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Ladderstep'),loc='best')


#recover keybits from file keybits.txt
with open('keybits_bin.txt') as f:
    keybits = f.read().splitlines()
keybits = [int(i) for i in keybits]
#transform the 0 and 1 of bit key into high and low levels of trace for X and Z abd take one to class the patterns
predicted_level_x,predicted_level_z=order4_keybits_to_HL(keybits)
pkey=order4_HL_to_keybits(predicted_level_z,'z')


debut = time.time()
#cut the measure in pattern according to the signal (supervised)
patternA,patternB=patternClassification_v2(model_raw_power.x,model_raw_trigger.y,predicted_level_z)
fin = time.time()
print("classification time : ",fin-debut)


colors=['k','g','r','y','b']
model=[[],[],[],[]]
for j,ind in enumerate([patternA[0],patternA[1],patternB[0],patternB[1]]):
    for i in range(len(ind)):
        ind[i]-=np.mean(ind[i])
    t=np.linspace(0,len(ind[0])-1,len(ind[0]))
    icolors=0
    name=['A1','A2','B1','B2']
    plt.figure()
    plt.title(name[j])
    for i in range(len(ind)):
        icolors=(i%5)
        plt.plot(t,ind[i],colors[icolors])
    model[j]=np.mean(ind,axis=0)
    model[j]=(model[j]-np.mean(model[j]))/(np.std(model[j]))

#print all model
plt.figure()
plt.title('Model A1,A2,B1,B2,C1,C2')
for i in range(len(model)):
    t=np.linspace(0,(len(model[i])-1)*1e-4,len(model[i]))
    plt.plot(t,model[i])
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('A1','A2','B1','B2','C1','C2'),loc='best')
fin=time.time()
print("creating models from samples = ",fin-debut,"s")

#we do correlation
unknown_level = correlation_vs_model_v2(unknwon_inter_power,unknown_inter_trigger,model)
fin = time.time()
print("correlation time : ", fin-debut)
print("extracted levels : \n",unknown_level)

#and convert the levels into keybits with order 4 point algorithm
unknown_keybits=order4_HL_to_keybits(unknown_level,'z')

#print extracted key
print("extracted key : ")
printHex256bits(unknown_keybits)


plt.show()