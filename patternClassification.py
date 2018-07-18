import numpy as np
import matplotlib.pyplot as plt
import time
#returns High and Low with the traces of respectively non-zero and zero multiplication
#data is the complete power trace
#ladderstep is high for every calculation and is used to cut traces
#level is the list of levels 1 for high and 0 for low

#this version of the function evaluate the length of one ladderstep and cut the signal in 256. The length of the 256 laddersteps is given by the trigger and then we divide 
#the number of points for the total time the trigger is ON by 256 and define this number as the length of one ladderstep.
def patternClassification(data,trigger,level):
    
    alt=False#used to separate the two patterns for high level
    m=[]#trace of 256 laddersteps
    High1,High2,Low=[],[],[]#in fact, after a few tries, it appeared there is 2 patterns for High

    idebut= time.time()
    for i in range(len(data)):
        if trigger[i] < -2:
            m.append(data[i])
    ifin=time.time()
    print("remove time = ",ifin-idebut)

    del m[:3263]#remove the points before laddersteps. This nb have been adjusted regarding the curves obtained after patternclassification
    
    #plot m
    # tm=np.linspace(0,len(m)-1,len(m))
    # plt.figure()
    # plt.plot(tm,m)

    ladderstep=[]
    k=0#indenter to go through 256 loops of ladderstep
    j=0#indenter to capture one ladderstep in 'ladderstep'
    run=1#semaphore to separate repplishing of 'ladderstep' and the classification with respect to 'level'
    len_ladderstep=len(m)/256#the number of points for one ladderstep

    for i in range(len(m)):
        if run==1:
            if j<len_ladderstep-1:
                ladderstep.append(m[i])
                j+=1
            else:
                run=0
                j=0
        if run==0:
            run=1
            # print(k)
            # if k==0:
            # print("level[",k,"]= ",level[k])
            # t=np.linspace(0,len_ladderstep-1,len_ladderstep)
            # plt.figure()
            # plt.plot(t,ladderstep)
            # plt.show()
            if level[k]==0:
                Low.append(ladderstep)
            elif level[k]==1:
                alt=not alt
                if alt==True:
                    High1.append(ladderstep)
                else:
                    High2.append(ladderstep)
            else:
                raise ValueError('The values of level should be 0s or 1s.')
            ladderstep=[]
            k+=1
    if k<256:#important if the last ladderstep is shorter than len_ladderstep else we would lost the last bit
        meanm=np.mean(ladderstep)
        while len(ladderstep)<len_ladderstep-1:#artifficial padding with the mean value of the signal but the best would be to add the values from data
            ladderstep.append(meanm)
        if level[k]==0:
            Low.append(ladderstep)
        elif level[k]==1:
            alt=not alt
            if alt==True:
                High1.append(ladderstep)
            else:
                High2.append(ladderstep)
        else:
            raise ValueError('The values of level should be 0s or 1s.')

    #we crop the sets so every sample are same length
    lref=len(Low[0])
    for i in range(len(Low)):
        if len(Low[i])<lref:
            lref=len(Low[i])
            for j in range(i):
                Low[j].pop()
        if len(Low[i])>lref:
            Low[i].pop()
    lref=len(High1[0])
    for i in range(len(High1)):
        if len(High1[i])<lref:
            lref=len(High1[i])
            for j in range(i):
                High1[j].pop()
        if len(High1[i])>lref:
            High1[i].pop()
    lref=len(High2[0])
    for i in range(len(High2)):
        if len(High2[i])<lref:
            lref=len(High2[i])
            for j in range(i):
                High2[j].pop()
        if len(High2[i])>lref:
            High2[i].pop()

    return Low,High1,High2


#4patterns
def patternClassification_v2(data,trigger,level):
    state = 1
    alt=False#used to separate the two patterns for high level
    m=[]#trace of 256 laddersteps
    High1,High2,Low1,Low2=[],[],[],[]#in fact, after a few tries, it appeared there is 2 patterns for High

    idebut= time.time()
    for i in range(len(data)):
        if trigger[i] < -2:
            m.append(data[i])
    ifin=time.time()
    print("remove time = ",ifin-idebut)

    del m[:3263]#remove the points before laddersteps. This nb have been adjusted regarding the curves obtained after patternclassification
    
    #plot m
    # tm=np.linspace(0,len(m)-1,len(m))
    # plt.figure()
    # plt.plot(tm,m)

    ladderstep=[]
    k=0#indenter to go through 256 loops of ladderstep
    j=0#indenter to capture one ladderstep in 'ladderstep'
    run=1#semaphore to separate repplishing of 'ladderstep' and the classification with respect to 'level'
    len_ladderstep=len(m)/256#the number of points for one ladderstep
    print("len(ladderstep = )",len_ladderstep)
    i=0
    petit=0
    while i<len(m):
        if run==1:
            if j<len_ladderstep-1:
                ladderstep.append(m[int(i)])
                j+=1
            else:
                run=0
                j=0
                petit+=0.13#because all laddersteps must be the same length we have to add a little time "petit" 
                #that will skip points to fit with the real time laddersteps. This parameter should be evaluated 
                #manualy as we don't know the duration of one ladderstep beforehand, but this parameter will be 
                #the same for every SCM.
        if run==0:
            run=1
            # print(k)
            # if k==0:
            # print("level[",k,"]= ",level[k])
            # t=np.linspace(0,len_ladderstep-1,len_ladderstep)
            # plt.figure()
            # plt.plot(t,ladderstep)
            # plt.show()
            if level[k]==0:
                if state==1:
                    Low1.append(ladderstep)
                    state=1
                elif state==2:
                    Low2.append(ladderstep)
                    state=3
                elif state==3:
                    Low2.append(ladderstep)
                    state=3
                elif state==4:
                    Low1.append(ladderstep)
                    state=1
                else:
                    print("f...")
            elif level[k]==1:
                if state==1:
                    High1.append(ladderstep)
                    state=2
                elif state==2:
                    High2.append(ladderstep)
                    state=4
                elif state==3:
                    High2.append(ladderstep)
                    state=4
                elif state==4:
                    High1.append(ladderstep)
                    state=2
                else:
                    print("f...")
            else:
                raise ValueError('The values of level should be 0s or 1s.')
            ladderstep=[]
            k+=1
        i+=1+petit
        petit=0
    if k<256:#important if the last ladderstep is shorter than len_ladderstep else we would lost the last bit
        meanm=np.mean(ladderstep)
        while len(ladderstep)<len_ladderstep-1:#artifficial padding with the mean value of the signal but the best would be to add the values from data
            ladderstep.append(meanm)
        if level[k]==0:
            if state==1:
                Low1.append(ladderstep)
                state=1
            elif state==2:
                Low2.append(ladderstep)
                state=3
            elif state==3:
                Low2.append(ladderstep)
                state=3
            elif state==4:
                Low1.append(ladderstep)
                state=1
            else:
                print("f...")
        elif level[k]==1:
            if state==1:
                High1.append(ladderstep)
                state=2
            elif state==2:
                High2.append(ladderstep)
                state=4
            elif state==3:
                High2.append(ladderstep)
                state=4
            elif state==4:
                High1.append(ladderstep)
                state=2
            else:
                print("f...")
        else:
            raise ValueError('The values of level should be 0s or 1s.')

    #we crop the sets so every sample are same length
    lref=len(Low1[0])
    for i in range(len(Low1)):
        if len(Low1[i])<lref:
            lref=len(Low1[i])
            for j in range(i):
                Low1[j].pop()
        if len(Low1[i])>lref:
            Low1[i].pop()
    lref=len(Low2[0])
    for i in range(len(Low2)):
        if len(Low2[i])<lref:
            lref=len(Low2[i])
            for j in range(i):
                Low2[j].pop()
        if len(Low2[i])>lref:
            Low2[i].pop()
    lref=len(High1[0])
    for i in range(len(High1)):
        if len(High1[i])<lref:
            lref=len(High1[i])
            for j in range(i):
                High1[j].pop()
        if len(High1[i])>lref:
            High1[i].pop()
    lref=len(High2[0])
    for i in range(len(High2)):
        if len(High2[i])<lref:
            lref=len(High2[i])
            for j in range(i):
                High2[j].pop()
        if len(High2[i])>lref:
            High2[i].pop()

    return Low1,Low2,High1,High2