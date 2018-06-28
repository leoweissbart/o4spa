import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

#takes the filtered data and the trigger signal for entire SCM and the 2 model of pattern to return levels detected on the trace
def correlation_vs_model_v3(data,trigger,modelH1,modelH2,modelL):
    i,it=0,0
    allseg,seg=[],[]
    while trigger[it]>-2:#we use the trigger to find the beginning of ML algorithm
        it+=1
    it+=3243#to don't consider the  part before the laddersteps (3243 seems to be better than 3263 for some reason by looking at the correlation level that is not "constant")
    j=it
    n_points=0
    while trigger[j]<-2:
        n_points+=1
        j+=1
    i=int(it)
    print(n_points/256,len(modelH1))
    #we separate all the laddersteps in the dataset into 'allseg'
    for k in range(256):
        for j in range(len(modelH1)):
            i=int(it)
            seg.append(data[i])
            it+=1
        it+=(n_points/256)-len(modelH1)+(2*(3263-3243)/256)#weighting to always fit with the laddersteps
        seg=(seg-np.mean(seg))/(np.std(seg))#normalization by Z-score of the segments
        allseg.append(seg)
        seg=[]
    
    # ti=np.linspace(0,len(allseg[0]-1),len(allseg[0]))
    # plt.figure()
    # for i in range(len(allseg)):
    #     plt.plot(ti,allseg[i])
    # plt.show()

    #compute correlation for every models
    array_corrH1,array_corrH2,array_corrL=[],[],[]
    t=np.linspace(0,len(modelH1)-1,len(modelH1))
    for i in range(len(allseg)):
        # if i>202:
        # plt.figure()
        # plt.plot(t,allseg[i],'#1f77b4')
        # plt.show()

        # plt.figure()
        # plt.plot(t,allseg[i],t,modelH1,'b',t,modelL,'r')
        # plt.show()
        corrL=np.correlate(allseg[i],modelL)
        corrH1=np.correlate(allseg[i],modelH1)
        corrH2=np.correlate(allseg[i],modelH2)
        array_corrL.append(corrL)
        array_corrH1.append(corrH1)
        array_corrH2.append(corrH2)

    t=np.linspace(0,len(array_corrH1)-1,len(array_corrH1))
    plt.figure()
    plt.title('Correlation')
    plt.plot(t,array_corrL,'or',t,array_corrH1,'ob',t,array_corrH2,'ok',t,array_corrL,'r',t,array_corrH1,'b',t,array_corrH2,'k')
    plt.xlabel('Time (in Second)')
    plt.ylabel('Correlation level')
    plt.grid()
    plt.legend(('Correlation with model L','Correlation with model H1','Correlation with model H2'),loc='best')

    # array_corrH1-=np.mean(array_corrH1)
    # array_corrH2-=np.mean(array_corrH2)
    # array_corrL-=np.mean(array_corrL)

    t=np.linspace(0,len(array_corrH1)-1,len(array_corrH1))
    fig=plt.figure()
    ax = fig.gca()
    ax.set_xticks(np.arange(0, 256, 1))
    plt.title('Correlation')
    plt.scatter(t,array_corrL)
    plt.scatter(t,array_corrH1)
    plt.scatter(t,array_corrH2)
    plt.plot(t,array_corrL,'#1f77b4',t,array_corrH1,'#ff7f0e',t,array_corrH2,'#009900')
    plt.xlabel('Number of ladderstep')
    plt.ylabel('Correlation level')
    plt.legend(('Correlation with model L','Correlation with model H1','Correlation with model H2'),loc='best')

    ax = subplot(111)

    ax.xaxis.set_major_locator(MultipleLocator(50))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.xaxis.grid(True,'minor')
    ax.xaxis.grid(True,'major',linewidth=2)

    level=[]
    #getting level v2, the assumption is that when corr is higher for H1 or H2 it cannot be the same next point, so we take the next higher level of correlation
    #wasH1 raise when H1 is higher than the TWO other patterns and raise down when H2 is the higher level. H2 respectively with H1
    wasH1,wasH2=False,False
    for i in range(len(array_corrH1)):
        if array_corrH1[i]>array_corrL[i]:
            if wasH1==False:
                level.append(1)
                wasH1=True
                wasH2=False
            else:
                if array_corrH2[i]>array_corrL[i]:
                    level.append(1)
                    wasH2=True
                    wasH1=False
                else:
                    level.append(0)
        elif array_corrH2[i]>array_corrL[i]:
            if wasH2==False:
                level.append(1)
                wasH2=True
                wasH1=False
            else:
                if array_corrH1[i]>array_corrL[i]:
                    level.append(1)
                    wasH1=True
                    wasH2=False
                else:
                    level.append(0)
        elif array_corrL[i]>array_corrH2[i]:
            level.append(0)
        elif array_corrL[i]>array_corrH1[i]:
            level.append(0)
        else:
            level.append(2)#if there is problem with comparaison
    print(level)
    return level
