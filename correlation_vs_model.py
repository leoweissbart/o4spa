import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

#takes the filtered data and the trigger signal for entire SCM and the 4 model of pattern to return levels detected on the trace
def correlation_vs_model_v3(data,trigger,modelP1,modelP2,modelH1,modelH2):
    i,it=0,0
    allseg,seg=[],[]
    ###################################################################################
    ##    counting the number of points during the Montgomery ladder                 ##
    ###################################################################################
    while trigger[it]<3.5:#we use the trigger to find the beginning of ML algorithm
        it+=1
    j=it
    n_points=0
    while trigger[j]>3.5:
        n_points+=1
        j+=1
    ###################################################################################

    ###################################################################################
    ##    cut the attack trace in 256 segments representing the laddersteps          ##
    ###################################################################################
    i=int(it)
    for k in range(256):
        for j in range(len(modelH1)):
            i=int(it)
            seg.append(data[i])
            it+=1
        it+=(n_points/256)-len(modelH1)#during ML algorithm n_points are captured and there is 256 laddersteps (n_points/256 is float while len(modelH) is int)
        seg=(seg-np.mean(seg))/(np.std(seg))
        allseg.append(seg)
        seg=[]
    ###################################################################################

    ###################################################################################
    ##    compute correlation with models                                            ##
    ###################################################################################
    array_corrH1,array_corrH2,array_corrP1,array_corrP2=[],[],[],[]
    t=np.linspace(0,len(modelH1)-1,len(modelH1))
    for i in range(len(allseg)):
        corrP1=np.correlate(allseg[i],modelP1)
        corrP2=np.correlate(allseg[i],modelP2)
        corrH1=np.correlate(allseg[i],modelH1)
        corrH2=np.correlate(allseg[i],modelH2)
        array_corrP1.append(corrP1)
        array_corrP2.append(corrP2)
        array_corrH1.append(corrH1)
        array_corrH2.append(corrH2)
    ###################################################################################

    ###################################################################################
    ##    print Correlation plot                                                     ##
    ###################################################################################
    t=np.linspace(0,len(array_corrH1)-1,len(array_corrH1))
    plt.figure()
    plt.title('Correlation')
    plt.plot(t,array_corrP1,'or',t,array_corrP2,'ob',t,array_corrH1,'ok',t,array_corrH2,'og',t,array_corrP1,'r',t,array_corrP2,'b',t,array_corrH1,'k',t,array_corrH2,'g')
    plt.xlabel('Time (in Second)')
    plt.ylabel('Correlation level')
    plt.grid()
    plt.legend(('Correlation with model P1','Correlation with model P2','Correlation with model H1','Correlation with model H2'),loc='best')
    ###################################################################################
    
    ###################################################################################
    ##    construct level array                                                      ##
    ###################################################################################
    level=[]
    for i in range(len(array_corrH1)):
        if array_corrH1[i]>array_corrP1[i]:
            level.append(1)
        elif array_corrH1[i]>array_corrP2[i]:
            level.append(1)
        elif array_corrH2[i]>array_corrP1[i]:
            level.append(1)
        elif array_corrH2[i]>array_corrP2[i]:
            level.append(1)
        elif array_corrP1[i]>array_corrH1[i]:
            level.append(0)
        elif array_corrP1[i]>array_corrH2[i]:
            level.append(0)
        elif array_corrP2[i]>array_corrH1[i]:
            level.append(0)
        elif array_corrP2[i]>array_corrH2[i]:
            level.append(0)
        else:
            level.append(2)#if there is problem with comparaison
    print(level)
    ###################################################################################
    return level