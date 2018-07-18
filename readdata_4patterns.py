import os
import glob
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
from scipy import signal
from order4_keybits_to_HL import order4_keybits_to_HL
from patternClassification import patternClassification,patternClassification_v2
from correlation_vs_model import correlation_vs_model,correlation_vs_model_v2
from order4_HL_to_keybits import order4_HL_to_keybits
from printHex256bits import printHex256bits
from scipy.interpolate import interp1d
import time

#for model
#t=time
#x=power consuption
#u=trigger            (not used)
#y=ladderstep
#z=bitvalue           (not used)
model_raw_power = pd.read_csv('ecc_order4_256_avg64.csv',header=23,names = ('t','x'))
model_raw_trigger = pd.read_csv('ecc_order4_256_avg64_trig.csv',header=23,names = ('t','y'))
#should use pd.merge() to fuse the two frames

unknown_raw_power = pd.read_csv('C:/Users/Leo/Documents/ecc_FPGA_rev-1_order4_day2/ecc_order4_256_avg64_data2.csv',header=23, names=('t','x'))
unknown_raw_trigger = pd.read_csv('C:/Users/Leo/Documents/ecc_FPGA_rev-1_order4_day2/ecc_order4_256_avg64_data2_trig.csv',header=23, names=('t','y'))

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
print(predicted_level_z)
pkey=order4_HL_to_keybits(predicted_level_z,'z')
printHex256bits(pkey)

debut = time.time()
#cut the measure in pattern according to the signal (supervised)
A1,A2,B1,B2=patternClassification_v2(model_raw_power.x,model_raw_trigger.y,predicted_level_z)
fin = time.time()
print("classification time : ",fin-debut)

ta=np.linspace(0,len(A1[0])-1,len(A1[0]))
colors=['k','g','r','y','b']
j=0
plt.figure()
for i in range(len(A1)):
    j=(i%5)
    plt.plot(ta,A1[i],colors[j])
    plt.title('A1')

ta=np.linspace(0,len(A2[0])-1,len(A2[0]))
colors=['k','g','r','y','b']
j=0
plt.figure()
for i in range(len(A2)):
    j=(i%5)
    plt.plot(ta,A2[i],colors[j])
    plt.title('A2')

tb1=np.linspace(0,len(B1[0])-1,len(B1[0]))
plt.figure()
for i in range(len(B1)):
    j=i%5
    plt.plot(tb1,B1[i],colors[j])
    plt.title('B1')

tb2=np.linspace(0,len(B2[0])-1,len(B2[0]))
plt.figure()
for i in range(len(B2)):
    j=i%5
    plt.plot(tb2,B2[i],colors[j])
    plt.title('B2')

#create the model of pattern A and B
model_low1=np.mean(A1,axis=0)
model_low2=np.mean(A2,axis=0)
model_high1=np.mean(B1,axis=0)
model_high2=np.mean(B2,axis=0)
#normalization by Z-score
model_low1=(model_low1-np.mean(model_low1))/(np.std(model_low1))
model_low2=(model_low2-np.mean(model_low2))/(np.std(model_low2))
model_high1=(model_high1-np.mean(model_high1))/(np.std(model_high1))
model_high2=(model_high2-np.mean(model_high2))/(np.std(model_high2))


#print models
t=np.linspace(0,(len(model_low1)-1)*5e-10,len(model_low1))
plt.figure()
plt.title('Model B1 for filtered trace (model_high1)')
plt.plot(t,model_high1,'b')
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.figure()
plt.title('Model A1 for filtered trace (model_low)')
plt.plot(t,model_low1,'r')
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.figure()
plt.title('Model A2 for filtered trace (model_low)')
plt.plot(t,model_low2,'g')
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.figure()
plt.title('Model B2 for filtered trace (model_high2)')
plt.plot(t,model_high2,'k')
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.figure()
plt.title('4 models')
plt.plot(t,model_high1,t,model_high2,t,model_low1,t,model_low2)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('B1','B2','A1','A2'),loc='best')
plt.figure()
plt.title('A1 B2 models')
plt.plot(t,model_high2,t,model_low1)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('B2','A1'),loc='best')
plt.figure()
plt.title('A2 B1 models')
plt.plot(t,model_high1,t,model_low2)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('B1','A2'),loc='best')
debut = time.time()
#we do correlation
unknown_level = correlation_vs_model_v2(unknwon_inter_power,unknown_inter_trigger,model_high1,model_high2,model_low1,model_low2)
fin = time.time()
print("correlation time : ", fin-debut)
print("extracted levels : \n",unknown_level)

#and convert the levels into keybits with order 4 point algorithm
unknown_keybits=order4_HL_to_keybits(unknown_level,'z')

#print extracted key
print("extracted key : ")
printHex256bits(unknown_keybits)


plt.show()