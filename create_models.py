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
from scipy.interpolate import interp1d


#for model
#t=time
#x=power consuption
#u=trigger            (not used)
#y=ladderstep
#z=bitvalue           (not used)
model_raw_power = pd.read_csv('ecc_order4_256_avg64.csv',header=23,names = ('t','x'))
model_raw_trigger = pd.read_csv('ecc_order4_256_avg64_trig.csv',header=23,names = ('t','y'))
#should use pd.merge() to fuse the two frames

unknown_raw_power = pd.read_csv('C:/Users/Leo/Documents/ecc_FPGA_rev-1_order4_day2/ecc_order4_256_avg64_pssvprobe.csv',header=23, names=('t','x'))
unknown_raw_trigger = pd.read_csv('C:/Users/Leo/Documents/ecc_FPGA_rev-1_order4_day2/ecc_order4_256_avg64_pssvprobe_trig.csv',header=23, names=('t','y'))

#if the sampling frequency of testing dataset is lower than the one for training dataset, we should do an interpolation to match the total number of points
#we create interpolation for power and trigger so the data is the same size as training data (we lose time information)
x=unknown_raw_power.t
xnew=np.linspace(unknown_raw_power.t.iloc[0],unknown_raw_power.t.iloc[-1],len(model_raw_power.t))
f_power=interp1d(x,unknown_raw_power.x,kind='cubic')
f_trigger=interp1d(x,unknown_raw_trigger.y)
unknwon_inter_power=f_power(xnew)#interpolation of power trace of unknown attack
unknown_inter_trigger=f_trigger(xnew)#interpolation of trigger trace of unknwon attack
#change the name of filtered data if it not filtered change x to power and y to trigger
model_filtered_x=model_raw_power.x
model_filtered_y=model_raw_trigger.y

plt.figure()
plt.title('Training set')
plt.plot(model_raw_power.t,model_filtered_x,model_raw_trigger.t,model_filtered_y)
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')
plt.legend(('Power','Ladderstep'),loc='best')
plt.figure()
plt.title('Test set')
plt.plot(xnew,unknwon_inter_power,xnew,unknown_inter_trigger)
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
#cut the measure in pattern according to the signal (supervised)
A,B1,B2=patternClassification(model_filtered_x,model_filtered_y,predicted_level_z)


#create the model of pattern A and B
model_low=np.mean(A,axis=0)
model_high1=np.mean(B1,axis=0)
model_high2=np.mean(B2,axis=0)
#normalization by Z-score
model_low=(model_low-np.mean(model_low))/(np.std(model_low))
model_high1=(model_high1-np.mean(model_high1))/(np.std(model_high1))
model_high2=(model_high2-np.mean(model_high2))/(np.std(model_high2))


#print models
t=np.linspace(0,(len(model_low)-1)*5e-10,len(model_low))
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
plt.figure()
plt.title('Model B2 for filtered trace (model_high2)')
plt.plot(t,model_high2,'k')
plt.xlabel('Time (in Second)')
plt.ylabel('Tension (in Volt)')


#we do correlation
unknown_level = correlation_vs_model_v3(unknwon_inter_power,unknown_inter_trigger,model_high1,model_high2,model_low)


#and convert the levels into keybits with order 4 point algorithm
unknown_keybits=order4_HL_to_keybits(unknown_level,'z')
#print extracted key
printHex256bits(unknown_keybits)


plt.show()