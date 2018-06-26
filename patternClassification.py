import numpy as np
import matplotlib.pyplot as plt
#returns High and Low with the traces of respectively non-zero and zero multiplication
#data is the complete power trace
#ladderstep is high for every calculation and is used to cut traces
#level is the list of levels 1 for high and 0 for low

#this version of the function evaluate the length of one ladderstep and cut the signal in 256. The length of the 256 laddersteps is given by the trigger and then we divide 
#the number of points for the total time the trigger is ON by 256 and define this number as the length of one ladderstep.
def patternClassification(data,trigger,level):
    alt=False
    m=[]#temporary trace constructed to be stored in High or Low
    A,B=[],[]
    for i in range(len(data)):
        if trigger[i] < -2:
            m.append(data[i])
    del m[:3263]#remove the points before laddersteps. This nb have been adjusted regarding the curves obtained after patternclassification
    
    tm=np.linspace(0,len(m)-1,len(m))
    plt.figure()
    plt.plot(tm,m)

    High1,High2,Low=[],[],[]
    ladderstep=[]
    k=0
    j=0
    run=1
    # for i in range(100):
    # del m[:num]
    len_ladderstep=len(m)/256
    # print("loop= ",loop)

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
                # plt.figure()
                # plt.plot(t,ladderstep)
                # plt.show()
                Low.append(ladderstep)
                ladderstep=[]
            elif level[k]==1:
                alt=not alt
                if alt==True:
                    High1.append(ladderstep)
                else:
                    High2.append(ladderstep)
                # High.append(ladderstep)
                ladderstep=[]
            else:
                raise ValueError('The values of level should be 0s or 1s.')
            k+=1
    if k<256:#important if the last ladderstep is shorter than len_ladderstep else we would lost the last bit
        meanm=np.mean(ladderstep)
        while len(ladderstep)<len_ladderstep-1:#artifficial padding with the mean value of the signal but the best would be to add the values from data
            ladderstep.append(meanm)
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
            # High.append(ladderstep)
            # ladderstep=[]
        else:
            raise ValueError('The values of level should be 0s or 1s.')
    k=0

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
        
        # A=High
        # B=Low
        # ta=np.linspace(0,len(A[0])-1,len(A[0]))
        # colors=['k','g','r','y','b']
        # j=0
        # fig=plt.figure()
        # for i in range(len(A)):
        #     j=(i%5)
        #     plt.plot(ta,A[i],colors[j])
        #     plt.title('A')
        # fig.savefig('C:/Users/Leo/Documents/VSworkspace/o4spa/models_3233_3488/A%d.png' % loop)
        # plt.close(fig)
        # tb=np.linspace(0,len(B[0])-1,len(B[0]))
        # fig2=plt.figure()
        # for i in range(len(B)):
        #     j=i%5
        #     plt.plot(tb,B[i],colors[j])
        #     plt.title('B')
        # fig2.savefig('C:/Users/Leo/Documents/VSworkspace/o4spa/models_3233_3488/B%d.png' % loop)
        # plt.close(fig2)
        # A=[]
        # B=[]
        
        # model_low=np.mean(Low,axis=0)
        # model_high=np.mean(High,axis=0)
        # model_low-=np.mean(model_low)
        # model_high-=np.mean(model_high)
        # t=np.linspace(0,(len(model_low)-1)*5e-10,len(model_low))
        # fig = plt.figure()
        # plt.title('Model A,B for filtered trace (model_low, model_high)')
        # plt.plot(t,model_low,'r',t,model_high,'b')
        # plt.xlabel('Time (in Second)')
        # plt.ylabel('Tension (in Volt)')
        # plt.legend(('A','B'),loc='best')
        # fig.savefig('C:/Users/Leo/Documents/VSworkspace/o4spa/models16000pts/%d.png' % loop)
        # plt.close(fig)

    return Low,High1,High2
