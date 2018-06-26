import os
import glob
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
from scipy import signal
from order4_keybits_to_HL import order4_keybits_to_HL
from patternClassification import patternClassification
from correlation_vs_model import correlation_vs_model_v3
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


#for model
#t=time
#x=power consuption
#u=trigger            (not used)
#y=ladderstep
#z=bitvalue           (not used)
model_raw_power = pd.read_csv('C:/Users/Leo/Documents/ecc_FPGA_rev-1_order4/ecc_order4_256_avg64.csv',header=23,names = ('t','x'))
model_raw_trigger = pd.read_csv('C:/Users/Leo/Documents/ecc_FPGA_rev-1_order4/ecc_order4_256_avg64_trig.csv',header=23,names = ('t','y'))
#should use pd.merge() to fuse the two frames

# model_raw_data.x-=0.3
plt.figure()
plt.title('Training set')
plt.plot(model_raw_power.t,model_raw_power.x,model_raw_trigger.t,model_raw_trigger.y)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Ladderstep'),loc='best')



#Be carefull because for now there is no numeric filter so if the signal is noisy, the averaging will reduce the voltage level and the models won't fit with the patterns from power traces.
# fs=1e3
# cutoff_hz=1250
# #filter the mesure and replace its value in the data_frame
# model_filtered_x=butter_lowpass_filter(model_raw_data.x,cutoff_hz,fs)
# model_filtered_y=butter_lowpass_filter(model_raw_data.y,cutoff_hz,fs)
# plt.figure()
# plt.title('Filterd training set')
# plt.plot(model_raw_data.t,model_filtered_x,model_raw_data.t,model_filtered_y)
# plt.xlabel('Time (in Second)')
# plt.ylabel('Tension (in Volt)')
# plt.legend(('Power','Ladderstep'),loc='best')

model_filtered_x=model_raw_power.x
model_filtered_y=model_raw_trigger.y

#recover keybits from file keybits.txt
with open('C:/Users/Leo/Documents/ecc_FPGA_rev-1_order4/keybits_bin.txt') as f:
    keybits = f.read().splitlines()
keybits = [int(i) for i in keybits]
#transform the 0 and 1 of bit key into high and low levels of trace for X and Z abd take one to class the patterns
predicted_level_x,predicted_level_z=order4_keybits_to_HL(keybits)
print(predicted_level_z)
#cut the measure in pattern according to the signal (supervised)
A,B1,B2=patternClassification(model_filtered_x,model_filtered_y,predicted_level_z)

# ta=np.linspace(0,len(A[0])-1,len(A[0]))
# colors=['k','g','r','y','b']
# j=0
# plt.figure()
# for i in range(len(A)):
#     j=(i%5)
#     plt.plot(ta,A[i],colors[j])
#     plt.title('A')

# tb=np.linspace(0,len(B[0])-1,len(B[0]))
# plt.figure()
# for i in range(len(B)):
#     j=i%5
#     plt.plot(tb,B[i],colors[j])
#     plt.title('B')

#create the model of pattern A and B
model_low=np.mean(A,axis=0)
model_high1=np.mean(B1,axis=0)
model_high2=np.mean(B2,axis=0)
model_low-=np.mean(model_low)
model_high1-=np.mean(model_high1)
model_high2-=np.mean(model_high2)


#print both model
t=np.linspace(0,(len(model_low)-1)*5e-10,len(model_low))
# fig = plt.figure()
# plt.title('Model A,B1,B2 for filtered trace (model_low, model_high1,model_high2)')
# plt.plot(t,model_low,'r',t,model_high1,'b',t,model_high2,'k')
# plt.xlabel('Time (in Second)')
# plt.ylabel('Tension (in Volt)')
# plt.legend(('A','B1','B2'),loc='best')
# fig = plt.figure()
plt.figure()
plt.title('Model B1 for filtered trace (model_high1)')
plt.plot(t,model_high1,'b')
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
fig = plt.figure()
plt.title('Model A for filtered trace (model_low)')
plt.plot(t,model_low,'r')
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
fig = plt.figure()
plt.title('Model B2 for filtered trace (model_high2)')
plt.plot(t,model_high2,'k')
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
# fig.savefig('C:/Users/Leo/Documents/VSworkspace/o4spa/models16000pts/%d.png' % num)
# plt.close(fig)


#we do correlation
unknown_level = correlation_vs_model_v3(model_filtered_x,model_filtered_y,model_high1,model_high2,model_low)


# #and convert the levels into keybits with order 4 point algorithm
unknown_keybits=order4_HL_to_keybits(unknown_level,'z')

printHex256bits(unknown_keybits)

# fin = time.time()
# print("time = ",fin-debut," s.")

plt.show()