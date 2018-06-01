import numpy as np
import matplotlib.pyplot as plt
#returns High and Low with the traces of respectively non-zero and zero multiplication
#data is the complete power trace
#ladderstep is high for every calculation and is used to cut traces
#level is the list of levels 1 for high and 0 for low
def patternClassification(data,ladderstep,level):
    High,Low=[],[]
    m=[]#temporary trace constructed to be stored in High or Low
    k=0
    run=0
    for i in range(len(data)):
        if ladderstep[i]>0.3:
            run=1
            m.append(data[i])
        if run==1:
            if ladderstep[i]<0.3:
                run=0
                if level[k]==0:
                    Low.append(m)
                    m=[]
                elif level[k]==1:
                    High.append(m)
                    m=[]
                else:
                    raise ValueError('The values of level should be 0s or 1s.')
                k+=1
    #we crop the sets so every sample are same length

    lref=len(Low[0])
    for i in range(len(Low)):
        if len(Low[i])<lref:
            lref=len(Low[i])
            for j in range(i):
                Low[j].pop()
        if len(Low[i])>lref:
            Low[i].pop()
    lref=len(High[0])
    for i in range(len(High)):
        if len(High[i])<lref:
            lref=len(High[i])
            for j in range(i):
                High[j].pop()
        if len(High[i])>lref:
            High[i].pop()
    return Low,High
