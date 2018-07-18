import numpy as np
import matplotlib.pyplot as plt
from pylab import subplot
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

#takes the filtered data and the trigger signal for entire SCM and the 2 model of pattern to return levels detected on the trace
def correlation_vs_model(data,trigger,modelH1,modelH2,modelL):
    i,it=0,0
    allseg,seg=[],[]
    while trigger[it]>-2:#we use the trigger to find the beginning of ML algorithm
        it+=1
    it+=3263#to don't consider the  part before the laddersteps (3243 seems to be better than 3263 for some reason by looking at the correlation level that is not "constant")
    j=it
    n_points=0
    while trigger[j]<-2:
        n_points+=1
        j+=1
    i=int(it)
    # print(n_points/256,len(modelH1))
    #we separate all the laddersteps in the dataset into 'allseg'
    for k in range(256):
        for j in range(len(modelH1)):
            i=int(it)
            seg.append(data[i])
            it+=1
        it+=1.13#weighting to always fit with the laddersteps
        seg=(seg-np.mean(seg))/(np.std(seg))#normalization by Z-score of the segments
        allseg.append(seg)
        seg=[]

    #compute correlation for every models
    array_corrH1,array_corrH2,array_corrL=[],[],[]
    t=np.linspace(0,len(modelH1)-1,len(modelH1))
    for i in range(len(allseg)):
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
    return level


#with 4 patterns
def correlation_vs_model_v2(data,trigger,modelH1,modelH2,modelL1,modelL2):
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
    # print(n_points/256,len(modelH1))
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

    #compute correlation for every models
    array_corrH1,array_corrH2,array_corrL1,array_corrL2=[],[],[],[]
    t=np.linspace(0,len(modelH1)-1,len(modelH1))
    for i in range(len(allseg)):
        corrL1=np.correlate(allseg[i],modelL1)
        corrL2=np.correlate(allseg[i],modelL2)
        corrH1=np.correlate(allseg[i],modelH1)
        corrH2=np.correlate(allseg[i],modelH2)
        array_corrL1.append(corrL1)
        array_corrL2.append(corrL2)
        array_corrH1.append(corrH1)
        array_corrH2.append(corrH2)

    t=np.linspace(0,len(array_corrH1)-1,len(array_corrH1))
    plt.figure()
    plt.title('Correlation')
    plt.plot(t,array_corrL1,'or',t,array_corrL2,'og',t,array_corrH1,'ob',t,array_corrH2,'ok',t,array_corrL1,'r',t,array_corrL2,'g',t,array_corrH1,'b',t,array_corrH2,'k')
    plt.xlabel('Time (in Second)')
    plt.ylabel('Correlation level')
    plt.grid()
    plt.legend(('A1','A2','B1','B2'),loc='best')


    # t=np.linspace(0,len(array_corrH1)-1,len(array_corrH1))
    # fig=plt.figure()
    # ax = fig.gca()
    # ax.set_xticks(np.arange(0, 256, 1))
    # plt.title('Correlation')
    # plt.scatter(t,array_corrL)
    # plt.scatter(t,array_corrH1)
    # plt.scatter(t,array_corrH2)
    # plt.plot(t,array_corrL,'#1f77b4',t,array_corrH1,'#ff7f0e',t,array_corrH2,'#009900')
    # plt.xlabel('Number of ladderstep')
    # plt.ylabel('Correlation level')
    # plt.legend(('Correlation with model L','Correlation with model H1','Correlation with model H2'),loc='best')

    # ax = subplot(111)

    # ax.xaxis.set_major_locator(MultipleLocator(50))
    # ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    # ax.xaxis.set_minor_locator(MultipleLocator(1))
    # ax.xaxis.grid(True,'minor')
    # ax.xaxis.grid(True,'major',linewidth=2)

    level=[]
    #getting level v2, the assumption is that when corr is higher for H1 or H2 it cannot be the same next point, so we take the next higher level of correlation
    #wasH1 raise when H1 is higher than the TWO other patterns and raise down when H2 is the higher level. H2 respectively with H1
    wasH1,wasH2=False,False
    for i in range(len(array_corrH1)):
        if array_corrH1[i]==max([array_corrH1[i],array_corrH2[i],array_corrL1[i],array_corrL2[i]]):
            if wasH1==False:
                level.append(1)
                wasH1=True
                wasH2=False
            elif array_corrH2[i]==max([array_corrH2[i],array_corrL1[i],array_corrL2[i]]):
                if wasH2==False:
                    level.append(1)
                    wasH1=False
                    wasH2=True
            else:
                level.append(0)
        elif array_corrH2[i]==max([array_corrH1[i],array_corrH2[i],array_corrL1[i],array_corrL2[i]]):
            if wasH2==False:
                level.append(1)
                wasH1=False
                wasH2=True
            elif array_corrH1[i]==max([array_corrH1[i],array_corrL1[i],array_corrL2[i]]):
                if wasH1==False:
                    level.append(1)
                    wasH1=True
                    wasH2=False
            else:
                level.append(0)
        elif array_corrL1[i]==max([array_corrH1[i],array_corrH2[i],array_corrL1[i],array_corrL2[i]]):
            level.append(0)
        elif array_corrL2[i]==max([array_corrH1[i],array_corrH2[i],array_corrL1[i],array_corrL2[i]]):
            level.append(0)
    return level
