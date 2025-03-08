def getHandRankFromFiveCards(fC, fS): # given 5 cards, determine what the rank of the hand is and add kicker info to it
    if fS.count(fS[0])==len(fS): fC.append(8) if ((fC[0]==fC[1]-1==fC[2]-2==fC[3]-3) and (fC[4]-1==fC[3] or fC[4]-12==fC[0])) else fC.append(5)
    elif ((fC[0] == fC[1]-1 == fC[2]-2 == fC[3]-3) and (fC[4]-1 == fC[3] or fC[4]-12 == fC[0])): fC.append(4) # straight
    elif fC[1]==fC[2]==fC[3] and (fC[0]==fC[1] or fC[3]==fC[4]): fC.extend([7, fC[0], fC[4]]) if fC[0]==fC[1] else fC.extend([7, fC[4], fC[0]]) # quads
    elif fC[0]==fC[1]==fC[2] and fC[3]==fC[4]: fC.extend([6, fC[0], fC[4]]) # boat, high set full of low pair
    elif fC[0] == fC[1] and fC[2] == fC[3] == fC[4]: fC.extend([6, fC[4], fC[0]]) # boat, low set full of high pair
    elif fC[0]==fC[1]==fC[2]: fC.extend([3, fC[0], fC[4], fC[3]]) # trips, both kickers higher; other kicker-types of trips in next line
    elif fC[2]==fC[3] and (fC[1]==fC[2] or fC[3]==fC[4]): fC.extend([3, fC[1], fC[4], fC[0]]) if fC[1]==fC[2] else fC.extend([3, fC[2], fC[1], fC[0]])
    elif (fC[0]==fC[1] and (fC[2]==fC[3] or fC[3]==fC[4])) or (fC[1]==fC[2] and fC[3]==fC[4]): # two pair
        if fC[0]==fC[1] and fC[2]==fC[3]: fC.extend([2, fC[3], fC[1], fC[4]]) # kicker higher than both pairs
        else: fC.extend([2, fC[4], fC[1], fC[2]]) if fC[0]==fC[1] and fC[3]==fC[4] else fC.extend([2,fC[4],fC[1],fC[0]])
    elif fC[0]==fC[1] or fC[1]==fC[2]: fC.extend([1, fC[0], fC[4], fC[3], fC[2]]) if fC[0]==fC[1] else fC.extend([1, fC[1], fC[4], fC[3], fC[0]])
    elif fC[2]==fC[3] or fC[3]==fC[4]: fC.extend([1, fC[2], fC[4], fC[1], fC[0]]) if fC[2]==fC[3] else fC.extend([1, fC[3], fC[2], fC[1], fC[0]])
    return fC if len(fC) > 5 else fC + [0] # return hand, but first if we haven't appended anything else note that it's just a high card hand

def firstHandIsBetter(h1, h2): # given two hands, with the 5 cards + rank + relevant kicker details, say which wins
    if h1[5] != h2[5]: return h1[5] > h2[5] # different ranks
    if h1[5]==8 or h1[5]==4: return h1[2] > h2[2] if h1[2] != h2[2] else None # SF or straight: check middle card
    if h1[5]==5 or h1[5]==0: # flush or high card: check all five cards
        for wooper in range(5):
            if h1[4 - wooper] != h2[4 - wooper]: return h1[4 - wooper] > h2[4 - wooper]
        return None # chop
    for scromp in range(6,10):
        if h1[scromp] != h2[scromp]: return h1[scromp] > h2[scromp] # one is higher, so that one wins
        if len(h1) == scromp+1: return None # all were the same, so it's a chop