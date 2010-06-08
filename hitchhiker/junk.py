def distribute(bones, h1, h2, h3, nleads, trumps):
    if (len(bones) > 0):
        ngood = 0
        ntot = 0
        a = h1[:]
        b = bones[:]
        bone = b.pop()
        a.append(bone)
        #print 'Hand 1 : ', a
        c, d = distribute(b, a, h2, h3, nleads, trumps)
        ngood += c
        ntot += d
        a = h2[:]
        a.append(bone)
        #print 'hand 1 : ', h1
        #print 'Hand 2 : ', a
        c, d = distribute(b, h1, a, h3, nleads, trumps)
        ngood += c
        ntot += d
        a = h3[:]
        a.append(bone)
        c, d = distribute(b, h1, h2, a, nleads, trumps)
        ngood += c
        ntot += d
        return ngood, ntot
    else:
        print h1, h2, h3
        if (nleads < len(h1)):
            if ( ( len(trumps) > nleads) ):
                if ( max(h1) > trumps[nleads]):
                    print 'set by h1!'
                    return 0, 1
            else:
                return 0, 1
        if (nleads < len(h2)):
            if ( len(trumps) > nleads):
                if (max(h2) > trumps[nleads]):
                    print 'set by h2!'
                    return 1, 1
            else:
                return 1, 1
        if (nleads < len(h3)):
            if (len(trumps) > nleads):
                if (max(h3) > trumps[nleads]):
                    print 'set by h3!'
                    return 0, 1
            else:
                return 0, 1
        return 1, 1
            
        '''    
            
            and (nleads >= len(h2)) and (nleads >= len(h3))):
            #print "Yep!"
            #print h1, h2, h3
            #raw_input()
            return 1, 1
        else:
            #print "Nope!"
            #print h1, h2, h3
            #raw_input()
            return 0, 1
        '''

hand_rank = [6, 5, 3]
all_rank = [6, 5, 4, 3, 2, 1, 0]
missing_rank = [b for b in all_rank if not b in hand_rank]

n_trumps = len(hand_rank)
n_missing_trumps = len(missing_rank)

n_leads = 6-max(missing_rank)

h1 = []
h2 = []
h3 = []

success, total =  distribute(missing_rank, h1, h2, h3, n_leads, hand_rank)

print success, total
print float(success)/float(total)

print asdf
