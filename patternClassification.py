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

#separate into 8 pattern depending in which state we enter
def patternClassification_v2(data,ladderstep,level):
    P1,P2,P3,P4=[],[],[],[]
    H1,H2,H3,H4=[],[],[],[]
    state=1
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
                    if state==1:
                        P1.append(m)
                        state=1
                    elif state==2:
                        P2.append(m)
                        state=3
                    elif state==3:
                        P3.append(m)
                        state=3
                    elif state==4:
                        P4.append(m)
                        state=1
                    else:
                        print("f...")
                elif level[k]==1:
                    if state==1:
                        H1.append(m)
                        state=2
                    elif state==2:
                        H2.append(m)
                        state=4
                    elif state==3:
                        H3.append(m)
                        state=4
                    elif state==4:
                        H4.append(m)
                        state=2
                    else:
                        print("f...")
                else:
                    raise ValueError('The values of level should be 0s or 1s.')
                m=[]
                k+=1
    #we crop the sets so every sample are same length

    lref=len(P1[0])
    for i in range(len(P1)):
        if len(P1[i])<lref:
            lref=len(P1[i])
            for j in range(i):
                P1[j].pop()
        if len(P1[i])>lref:
            P1[i].pop()
    lref=len(P2[0])
    for i in range(len(P2)):
        if len(P2[i])<lref:
            lref=len(P2[i])
            for j in range(i):
                P2[j].pop()
        if len(P2[i])>lref:
            P2[i].pop()
    lref=len(P3[0])
    for i in range(len(P3)):
        if len(P3[i])<lref:
            lref=len(P3[i])
            for j in range(i):
                P3[j].pop()
        if len(P3[i])>lref:
            P3[i].pop()
    lref=len(P4[0])
    for i in range(len(P4)):
        if len(P4[i])<lref:
            lref=len(P4[i])
            for j in range(i):
                P4[j].pop()
        if len(P4[i])>lref:
            P4[i].pop()
    lref=len(H1[0])
    for i in range(len(H1)):
        if len(H1[i])<lref:
            lref=len(H1[i])
            for j in range(i):
                H1[j].pop()
        if len(H1[i])>lref:
            H1[i].pop()
    lref=len(H2[0])
    for i in range(len(H2)):
        if len(H2[i])<lref:
            lref=len(H2[i])
            for j in range(i):
                H2[j].pop()
        if len(H2[i])>lref:
            H2[i].pop()
    lref=len(H3[0])
    for i in range(len(H3)):
        if len(H3[i])<lref:
            lref=len(H3[i])
            for j in range(i):
                H3[j].pop()
        if len(H3[i])>lref:
            H3[i].pop()
    lref=len(H4[0])
    for i in range(len(H4)):
        if len(H4[i])<lref:
            lref=len(H4[i])
            for j in range(i):
                H4[j].pop()
        if len(H4[i])>lref:
            H4[i].pop()
    return P1,P2,P3,P4,H1,H2,H3,H4

#separate into 4 pattern depending in which state we enter
def patternClassification_v3(data,ladderstep,level):
    P1,P2=[],[]
    H1,H2=[],[]
    state=1
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
                    if state==1:
                        P1.append(m)
                        state=1
                    elif state==2:
                        P2.append(m)
                        state=3
                    elif state==3:
                        P2.append(m)
                        state=3
                    elif state==4:
                        P1.append(m)
                        state=1
                    else:
                        print("f...")
                elif level[k]==1:
                    if state==1:
                        H1.append(m)
                        state=2
                    elif state==2:
                        H2.append(m)
                        state=4
                    elif state==3:
                        H2.append(m)
                        state=4
                    elif state==4:
                        H1.append(m)
                        state=2
                    else:
                        print("f...")
                else:
                    raise ValueError('The values of level should be 0s or 1s.')
                m=[]
                k+=1
    #we crop the sets so every sample are same length

    lref=len(P1[0])
    for i in range(len(P1)):
        if len(P1[i])<lref:
            lref=len(P1[i])
            for j in range(i):
                P1[j].pop()
        if len(P1[i])>lref:
            P1[i].pop()
    lref=len(P2[0])
    for i in range(len(P2)):
        if len(P2[i])<lref:
            lref=len(P2[i])
            for j in range(i):
                P2[j].pop()
        if len(P2[i])>lref:
            P2[i].pop()
    lref=len(H1[0])
    for i in range(len(H1)):
        if len(H1[i])<lref:
            lref=len(H1[i])
            for j in range(i):
                H1[j].pop()
        if len(H1[i])>lref:
            H1[i].pop()
    lref=len(H2[0])
    for i in range(len(H2)):
        if len(H2[i])<lref:
            lref=len(H2[i])
            for j in range(i):
                H2[j].pop()
        if len(H2[i])>lref:
            H2[i].pop()
    return P1,P2,H1,H2
