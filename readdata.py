import os
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
from scipy import signal
from order4_keybits_to_HL import order4_keybits_to_HL
from patternClassification import patternClassification, patternClassification_v2,patternClassification_v3
from correlation_vs_model import correlation_vs_model_v2_2,correlation_vs_model_v3
from order4_HL_to_keybits import order4_HL_to_keybits
from printHex256bits import printHex256bits
import time

debut = time.time()

#lowpass filter function
def butter_lowpass_filter(data,cut_freq, fs, order=5):
    nyq = 0.5 * fs
    cut_freq = cut_freq / nyq
    b,a=signal.butter(order,cut_freq,btype='lowpass')
    y = signal.lfilter(b, a, data)
    return y

#the unknown
#t=time
#x=power consuption
#u=trigger
unknown_raw_data = pd.read_csv('testset.csv',header=23,names = ('t','x','u'))

###################################################################################
##    plot test set                                                              ##
###################################################################################
unknown_raw_data.x-=0.3
plt.figure()
plt.title('Test set')
plt.plot(unknown_raw_data.t,unknown_raw_data.x,unknown_raw_data.t,unknown_raw_data.u)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Trigger'),loc='best')
###################################################################################


#for model
#t=time
#x=power consuption
#u=trigger            (not used)
#y=ladderstep
#z=bitvalue           (not used)
model_raw_data = pd.read_csv('trainingset.csv',header=23,names = ('t','x','u','y','z'))

###################################################################################
##    plot training set                                                          ##
###################################################################################
model_raw_data.x-=0.3
plt.figure()
plt.title('Training set')
plt.plot(model_raw_data.t,model_raw_data.x,model_raw_data.t,model_raw_data.y)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Ladderstep'),loc='best')
###################################################################################

###################################################################################
##    apply lowpass filter to the datasets                                      ##
###################################################################################
fs=1e4#sampling frequency of the datasets
cutoff_hz=1250#cutting frequency chosen for the lowpass filter
unknown_filtered_x=butter_lowpass_filter(unknown_raw_data.x,cutoff_hz,fs)
unknown_filtered_trigger=butter_lowpass_filter(unknown_raw_data.u,cutoff_hz,fs)

model_filtered_x=butter_lowpass_filter(model_raw_data.x,cutoff_hz,fs)
model_filtered_y=butter_lowpass_filter(model_raw_data.y,cutoff_hz,fs)
###################################################################################

###################################################################################
##    plot the filtered datasets                                                ##
###################################################################################
plt.figure()
plt.title('Unknown filtered data')
plt.plot(unknown_raw_data.t,unknown_filtered_x,unknown_raw_data.t,unknown_filtered_trigger)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Trigger'),loc='best')
plt.figure()
plt.title('Filterd training set')
plt.plot(model_raw_data.t,model_filtered_x,model_raw_data.t,model_filtered_y)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Ladderstep'),loc='best')
###################################################################################


#recover keybits from file keybits.txt
with open('keybits.txt') as f:
    keybits = f.read().splitlines()
keybits = [int(i) for i in keybits]

#transform the 0 and 1 bits of the key into high and low levels of trace for X and Z
predicted_level_x,predicted_level_z=order4_keybits_to_HL(keybits)

#cut the measure in pattern according to the signal (supervised)
A,B=patternClassification(model_filtered_x,model_filtered_y,predicted_level_z)
P1,P2,H1,H2=patternClassification_v3(model_filtered_x,model_filtered_y,predicted_level_z)
###################################################################################
##    plot all the elements of A and B                                           ##
###################################################################################
ta=np.linspace(0,len(A[0])-1,len(A[0]))
colors=['k','g','r','y','b']
j=0
plt.figure()
for i in range(len(A)):
    j=(i%5)
    plt.plot(ta,A[i],colors[j])
    plt.title('A')
tb=np.linspace(0,len(B[0])-1,len(B[0]))
plt.figure()
for i in range(len(B)):
    j=i%5
    plt.plot(tb,B[i],colors[j])
    plt.title('B')
###################################################################################
###################################################################################
##    plot all the elements of P1,P2,P3,P4,H1,H2,H3,H4                           ##
###################################################################################
ta=np.linspace(0,len(P1[0])-1,len(P1[0]))
colors=['k','g','r','y','b']
j=0
plt.figure()
for i in range(len(P1)):
    j=(i%5)
    plt.plot(ta,P1[i],colors[j])
    plt.title('P1')
ta=np.linspace(0,len(P2[0])-1,len(P2[0]))
plt.figure()
for i in range(len(P2)):
    j=(i%5)
    plt.plot(ta,P2[i],colors[j])
    plt.title('P2')
tb=np.linspace(0,len(H1[0])-1,len(H1[0]))
plt.figure()
for i in range(len(H1)):
    j=i%5
    plt.plot(tb,H1[i],colors[j])
    plt.title('H1')
tb=np.linspace(0,len(H2[0])-1,len(H2[0]))
plt.figure()
for i in range(len(H2)):
    j=i%5
    plt.plot(tb,H2[i],colors[j])
    plt.title('H2')
###################################################################################

#create the model of pattern A and B
model_low=np.mean(A,axis=0)
model_high=np.mean(B,axis=0)
#normalize models before correlation
model_low=(model_low-np.mean(model_low))/(np.std(model_low))
model_high=(model_high-np.mean(model_high))/(np.std(model_high))

#create the model of pattern P1,P2,P3,P4,H1,H2,H3,H4
model_P1=np.mean(P1,axis=0)
model_P2=np.mean(P2,axis=0)
model_H1=np.mean(H1,axis=0)
model_H2=np.mean(H2,axis=0)
#normalize models before correlation
model_P1=(model_P1-np.mean(model_P1))/(np.std(model_P1))
model_P2=(model_P2-np.mean(model_P2))/(np.std(model_P2))
model_H1=(model_H1-np.mean(model_H1))/(np.std(model_H1))
model_H2=(model_H2-np.mean(model_H2))/(np.std(model_H2))


###################################################################################
##    plot models                                                                ##
###################################################################################
t=np.linspace(0,(len(model_low)-1)*1e-4,len(model_low))
plt.figure()
plt.title('Model A,B for filtered trace (model_low, model_high)')
plt.plot(t,model_low,'r',t,model_high,'b')
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('A','B'),loc='best')
###################################################################################

###################################################################################
##    plot models                                                                ##
###################################################################################
t=np.linspace(0,(len(model_P1)-1)*1e-4,len(model_P1))
plt.figure()
plt.title('Model P1,P2,P3,P4,H1,H2,H3,H4 for filtered trace')
plt.plot(t,model_P1,t,model_P2,t,model_H1,t,model_H2)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('P1','P2','H1','H2'),loc='best')
###################################################################################

#we do correlation
unknown_level = correlation_vs_model_v3(unknown_filtered_x,unknown_filtered_trigger,model_P1,model_P2,model_H1,model_H2)
plt.show()
#and convert the levels into keybits with order 4 point algorithm
unknown_keybits=order4_HL_to_keybits(unknown_level,'z')

#print the extracted key in hexadecimal base
printHex256bits(unknown_keybits)

fin = time.time()
print("time = ",fin-debut," s.")

plt.show()