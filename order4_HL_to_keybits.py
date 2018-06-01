def order4_HL_to_keybits(level,coord):
    state=[0,1,2,3]#0:(0,P), 1:(P,2P), 2:(P,0), 3:(2P,P)
    cstate=0#indicate the current state
    keybits=[]
    if coord=='z':
        for el in level:
            if el==0:
                if cstate==state[0]:
                    keybits.append(0)
                    cstate=state[0]
                elif cstate==state[1]:
                    keybits.append(1)
                    cstate=state[2]
                elif cstate==state[2]:
                    keybits.append(1)
                    cstate=state[2]
                elif cstate==state[3]:
                    keybits.append(0)
                    cstate=state[0]
                else:
                    raise ValueError('The state of the algorithm is indeterminate please check function : order4_HL_to_keybits')
            elif el==1:
                if cstate==state[0]:
                    keybits.append(1)
                    cstate=state[1]
                elif cstate==state[1]:
                    keybits.append(0)
                    cstate=state[3]
                elif cstate==state[2]:
                    keybits.append(0)
                    cstate=state[3]
                elif cstate==state[3]:
                    keybits.append(1)
                    cstate=state[1]
                else:
                    raise ValueError('The state of the algorithm is indeterminate please check function : order4_HL_to_keybits')
            else:
                raise ValueError('Values of level should be 0 or 1s.')

    elif coord=='x':
        for el in level:
            if el==0:
                if cstate==state[0]:
                    keybits.append(1)
                    cstate=state[1]
                elif cstate==state[1]:
                    keybits.append(0)
                    cstate=state[3]
                elif cstate==state[2]:
                    keybits.append(0)
                    cstate=state[3]
                elif cstate==state[3]:
                    keybits.append(1)
                    cstate=state[1]
                else:
                    raise ValueError('The state of the algorithm is indeterminate please check function : order4_HL_to_keybits')
            elif el==1:
                if cstate==state[0]:
                    keybits.append(0)
                    cstate=state[0]
                elif cstate==state[1]:
                    keybits.append(1)
                    cstate=state[2]
                elif cstate==state[2]:
                    keybits.append(1)
                    cstate=state[2]
                elif cstate==state[3]:
                    keybits.append(0)
                    cstate=state[0]
                else:
                    raise ValueError('The state of the algorithm is indeterminate please check function : order4_HL_to_keybits')
            else:
                raise ValueError('Values of level should be 0 or 1s.')

    else:
        raise ValueError('You should enter x or z for coord.')
    return keybits