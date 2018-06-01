#converts the key bits order into high/low levels of power trace
def order4_keybits_to_HL(keybits):
    state=[0,1,2,3]#0:(0,P), 1:(P,2P), 2:(P,0), 3:(2P,P)
    cstate=0#indicate the current state
    X,Z=[],[]#lists of the outputs with x and z levels

    for i in range(len(keybits)):
        if cstate==0:
            if keybits[i]==0:
                X.append(1)
                Z.append(0)
                cstate=state[0]
            elif keybits[i]==1:
                X.append(0)
                Z.append(1)
                cstate=state[1]
            else:
                raise ValueError('The values of keybits should be 0s or 1s.')
        elif cstate==1:
            if keybits[i]==0:
                X.append(0)
                Z.append(1)
                cstate=state[3]
            elif keybits[i]==1:
                X.append(1)
                Z.append(0)
                cstate=state[2]
            else:
                raise ValueError('The values of keybits should be 0s or 1s.')
        elif cstate==2:
            if keybits[i]==0:
                X.append(0)
                Z.append(1)
                cstate=state[3]
            elif keybits[i]==1:
                X.append(1)
                Z.append(0)
                cstate=state[2]
            else:
                raise ValueError('The values of keybits should be 0s or 1s.')
        elif cstate==3:
            if keybits[i]==0:
                X.append(1)
                Z.append(0)
                cstate=state[0]
            elif keybits[i]==1:
                X.append(0)
                Z.append(1)
                cstate=state[1]
            else:
                raise ValueError('The values of keybits should be 0s or 1s.')
        else:
            raise ValueError('The state of the algorithm is indeterminate please check function : order4_keybits_to_HL')
    return X,Z