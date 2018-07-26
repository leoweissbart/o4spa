import numpy as np
import matplotlib.pyplot as plt
#returns PatternA and PatternB with the traces of each patterns of order 4 attack
#data is the complete power trace
#trigger represents the duration of SCM
#level is the list of levels 1 for high and 0 for low

#4patterns
def patternClassification_v2(data,trigger,level):
    state = 1
    m=[]#trace of 256 laddersteps
    A,B=[[],[]],[[],[]]

    for i in range(len(data)):
        if trigger[i] < -2:
            m.append(data[i])
    del m[:3263]#remove the points before laddersteps. This nb have been adjusted regarding the curves obtained after patternclassification

    ladderstep=[]
    k=0#indenter to go through 256 loops of ladderstep
    j=0#indenter to capture one ladderstep in 'ladderstep'
    run=1#semaphore to separate repplishing of 'ladderstep' and the classification with respect to 'level'
    len_ladderstep=len(m)/256#the number of points for one ladderstep
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
            if level[k]==0:
                if state==1:
                    A[0].append(ladderstep)
                    state=1
                elif state==2:
                    A[1].append(ladderstep)
                    state=3
                elif state==3:
                    A[1].append(ladderstep)
                    state=3
                elif state==4:
                    A[0].append(ladderstep)
                    state=1
                else:
                    print("f...")
            elif level[k]==1:
                if state==1:
                    B[0].append(ladderstep)
                    state=2
                elif state==2:
                    B[1].append(ladderstep)
                    state=4
                elif state==3:
                    B[1].append(ladderstep)
                    state=4
                elif state==4:
                    B[0].append(ladderstep)
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
                A[0].append(ladderstep)
                state=1
            elif state==2:
                A[1].append(ladderstep)
                state=3
            elif state==3:
                A[1].append(ladderstep)
                state=3
            elif state==4:
                A[0].append(ladderstep)
                state=1
            else:
                print("f...")
        elif level[k]==1:
            if state==1:
                B[0].append(ladderstep)
                state=2
            elif state==2:
                B[1].append(ladderstep)
                state=4
            elif state==3:
                B[1].append(ladderstep)
                state=4
            elif state==4:
                B[0].append(ladderstep)
                state=2
            else:
                print("f...")
        else:
            raise ValueError('The values of level should be 0s or 1s.')

    #we crop the sets so every sample are same length
    lref=len(A[0][0])
    for ind in [A[0],A[1],B[0],B[1]]:
        for i in range(len(ind)):
            if len(ind[i])<lref:
                lref=len(ind[i])
                for j in range(i):
                    ind[j].pop()
            while len(ind[i])>lref:
                ind[i].pop()

    return A,B