def printHex256bits(keybits):
    res=[]
    i,j=0,0
    for l in range(32):
        res.append(hex(keybits[i]*128+keybits[i+1]*64+keybits[i+2]*32+keybits[i+3]*16+keybits[i+4]*8+keybits[i+5]*4+keybits[i+6]*2+keybits[i+7]))
        j+=1
        i+=8
    print(res)
    return res