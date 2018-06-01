import os
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
from scipy import signal
from order4_keybits_to_HL import order4_keybits_to_HL
from patternClassification import patternClassification
from correlation_vs_model import correlation_vs_model_v2_2
from order4_HL_to_keybits import order4_HL_to_keybits
from printHex256bits import printHex256bits
import time

debut = time.time()

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


unknown_raw_data.x-=0.3
plt.figure()
plt.title('Test set')
plt.plot(unknown_raw_data.t,unknown_raw_data.x,unknown_raw_data.t,unknown_raw_data.u)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Trigger'),loc='best')


#for model
#t=time
#x=power consuption
#u=trigger            (not used)
#y=ladderstep
#z=bitvalue           (not used)
model_raw_data = pd.read_csv('trainingset.csv',header=23,names = ('t','x','u','y','z'))

model_raw_data.x-=0.3
plt.figure()
plt.title('Training set')
plt.plot(model_raw_data.t,model_raw_data.x,model_raw_data.t,model_raw_data.y)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Ladderstep'),loc='best')


fs=1e4
cutoff_hz=1250
unknown_filtered_x=butter_lowpass_filter(unknown_raw_data.x,cutoff_hz,fs)
unknown_filtered_trigger=butter_lowpass_filter(unknown_raw_data.u,cutoff_hz,fs)
plt.figure()
plt.title('Unknown filtered data')
plt.plot(unknown_raw_data.t,unknown_filtered_x,unknown_raw_data.t,unknown_filtered_trigger)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Trigger'),loc='best')



#filter the mesure and replace its value in the data_frame
model_filtered_x=butter_lowpass_filter(model_raw_data.x,cutoff_hz,fs)
model_filtered_y=butter_lowpass_filter(model_raw_data.y,cutoff_hz,fs)
plt.figure()
plt.title('Filterd training set')
plt.plot(model_raw_data.t,model_filtered_x,model_raw_data.t,model_filtered_y)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Ladderstep'),loc='best')



#recover keybits from file keybits.txt
with open('keybits.txt') as f:
    keybits = f.read().splitlines()
keybits = [int(i) for i in keybits]
#transform the 0 and 1 of bit key into high and low levels of trace for X and Z abd take one to class the patterns
predicted_level_x,predicted_level_z=order4_keybits_to_HL(keybits)

#cut the measure in pattern according to the signal (supervised)
A,B=patternClassification(model_filtered_x,model_filtered_y,predicted_level_z)

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

#create the model of pattern A and B
model_low=np.mean(A,axis=0)
model_high=np.mean(B,axis=0)
model_low-=np.mean(model_low)
model_high-=np.mean(model_high)


#print both model
t=np.linspace(0,(len(model_low)-1)*1e-4,len(model_low))
plt.figure()
plt.title('Model A,B for filtered trace (model_low, model_high)')
plt.plot(t,model_low,'r',t,model_high,'b')
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('A','B'),loc='best')



#we do correlation
unknown_level = correlation_vs_model_v2_2(unknown_filtered_x,unknown_filtered_trigger,model_high,model_low)


#and convert the levels into keybits with order 4 point algorithm
unknown_keybits=order4_HL_to_keybits(unknown_level,'z')

printHex256bits(unknown_keybits)

fin = time.time()
print("time = ",fin-debut," s.")

plt.show()