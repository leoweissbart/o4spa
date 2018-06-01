import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

#takes the filtered data and the trigger signal for entire SCM and the 2 model of pattern to return levels detected on the trace
def correlation_vs_model_v2_2(data,trigger,modelH,modelL):
    i,it=0,0
    allseg,seg=[],[]
    while trigger[it]<3.5:#we use the trigger to find the beginning of ML algorithm
        it+=1
    j=it
    n_points=0
    while trigger[j]>3.5:
        n_points+=1
        j+=1
    i=int(it)
    for k in range(256):
        for j in range(len(modelH)):
            i=int(it)
            seg.append(data[i])
            it+=1
        it+=(n_points/256)-len(modelH)#during ML algorithm n_points are captured and there is 256 laddersteps
        seg-=np.mean(seg)
        allseg.append(seg)
        seg=[]

    array_corrH,array_corrL=[],[]
    t=np.linspace(0,len(modelH)-1,len(modelH))
    for i in range(len(allseg)):
        # if i>202:
        # plt.figure()
        # plt.plot(t,allseg[i],'#1f77b4')

        # plt.figure()
        # plt.plot(t,allseg[i],t,modelH,'b',t,modelL,'r')
        # plt.show()
        corrL=np.correlate(allseg[i],modelL)
        corrH=np.correlate(allseg[i],modelH)
        array_corrL.append(corrL)
        array_corrH.append(corrH)

    t=np.linspace(0,len(array_corrH)-1,len(array_corrH))
    plt.figure()
    plt.title('Correlation')
    plt.plot(t,array_corrL,'or',t,array_corrH,'ob',t,array_corrL,'r',t,array_corrH,'b')
    plt.xlabel('Time (in Second)')
    plt.ylabel('Correlation level')
    plt.grid()
    plt.legend(('Correlation with model A','Correlation with model B'),loc='best')

    array_corrH-=np.mean(array_corrH)
    array_corrL-=np.mean(array_corrL)

    t=np.linspace(0,len(array_corrH)-1,len(array_corrH))
    fig=plt.figure()
    ax = fig.gca()
    ax.set_xticks(np.arange(0, 256, 1))
    plt.title('Correlation')
    plt.scatter(t,array_corrL)
    plt.scatter(t,array_corrH)
    plt.plot(t,array_corrL,'#1f77b4',t,array_corrH,'#ff7f0e')
    plt.xlabel('Number of ladderstep')
    plt.ylabel('Correlation level')
    plt.legend(('Correlation with model A','Correlation with model B'),loc='best')

    ax = subplot(111)

    ax.xaxis.set_major_locator(MultipleLocator(50))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.xaxis.grid(True,'minor')
    ax.xaxis.grid(True,'major',linewidth=2)

    level=[]
    for i in range(len(array_corrH)):
        if array_corrH[i]>array_corrL[i]:
            level.append(1)
        elif array_corrH[i]<array_corrL[i]:
            level.append(0)
        else:
            level.append(2)#if there is problem with comparaison
    print(level)
    return level
