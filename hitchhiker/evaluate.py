class Combination( object ):
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.frac = Fraction([i+1 for i in range(n)], [i+1 for i in range(k)]+[i+1 for i in range(n-k)])
        self.frac.cancel()
        self.frac.eval()
        
class Fraction( object ):
    def __init__(self, num, denom):
        self.num = num
        self.denom = denom
        self.cancel()
        self.value = 0.0
        
    def __div__(self, other):
        """Divides the fraction by another fraction"""
        self.num += other.denom
        self.denom += other.num
        self.cancel()

    def __mul__(self, other):
        """ Multiplies the fraction by another fraction """
        self.num += other.num
        self.denom += other.denom
        self.cancel()
        
    def cancel(self):
        """ Cancels common terms in the numerator and denominator, until no common terms remain """
        common = [i for i in self.num if i in self.denom]
        while len(common) > 0:
            for i in common:
                self.num.remove(i)
                self.denom.remove(i)
            common = [i for i in self.num if i in self.denom]
            
    def eval(self):
        """ Evaluates the fraction by separately multiplying the factors in the numerator and denominator, and dividing the results """
        num = 1.0
        for i in self.num:
            num *= i
        denom = 1.0
        for i in self.denom:
            denom *= i
        self.value = num/denom
        return self.value


def distribute(bones, h1, h2, h3, nleads, trumps):
    """ Calculates all possible hands with the remaining trumps, figuring out which hands can wrest control from the bidder's hand. """
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
        #print h1, h2, h3
        if (nleads < len(h1)):
            if ( ( len(trumps) > nleads) ):
                if ( max(h1) > trumps[nleads]):
                    #print 'set by h1!'
                    return 0, 1
            else:
                return 0, 1
        if (nleads < len(h2)):
            if ( len(trumps) > nleads):
                if (max(h2) > trumps[nleads]):
                    #print 'set by h2!'
                    return 0, 1
            else:
                return 0, 1
        if (nleads < len(h3)):
            if (len(trumps) > nleads):
                if (max(h3) > trumps[nleads]):
                    #print 'set by h3!'
                    return 0, 1
            else:
                return 0, 1
        #print h1, h2, h3, trumps
        return 1, 1

def controlProbability(hand, trump):
    """Returns the probability that the given hand controls the given trump suit"""
    '''
        inputs:
        hand = list[] of bone objects
        suit = integer representing the trump suit in question

        bone is a structure containing
            bone.t - integer representing the top suit
            bone.b - integer representing the bottom suit

        returns:
            normalized probability that the given hand controls (i.e. 
            will be able to draw remaining trumps with at least one
            trump left in the player's hand) the given suit.
    '''

    # How many dominos of the suit does the hand contain?
    hand_rank = []
    # List containing ranks of the dominoes in the hand within the suit

    for b in hand.bones:
        if trump.includes(b):
            hand_rank.append(b.rank[trump.value])

    hand_rank.sort()
    hand_rank.reverse()
    #How many trumps do we have?
    n_trumps = len(hand_rank)

    #Which trumps are we missing
    all_rank = [6, 5, 4, 3, 2, 1, 0]
    # N.B. : This list represents the rank of the dominoes
    # NOT the number of dots! i.e. 6 = double, 5 = next highest

    # Assuming the "critical" domino is in an opposing hand, what is
    # number of possible hands from the remaining 20 dominos?
    #total_hands = Combination(20, 6)
    
    # Finds the ranks of the missing trumps NOT in the player's hand
    missing_rank = [b for b in all_rank if not b in hand_rank]
    n_missing_trumps = len(missing_rank)

    n_leads = 6 - max(missing_rank)

    h1 = []
    h2 = []
    h3 = []

    success, total =  distribute(missing_rank, h1, h2, h3, n_leads, hand_rank)

    prob = float(success)/float(total)

    return prob

def calculateMostTrumpsProbabiliity(hand, suit):
    """ Returns the probability of having the most trumps (irrespective of control). Good thing to know if you're leading low..."""

def calculateLeadProbability(hand, suit):
    """Returns a list corresponding to the probabilities that each domino in HAND will be able to used as a winning lead, assuming SUIT is trump"""

def calculateOffProbability(hand, suit):
    """Returns a list corresponding to the probabilities that each domino in HAND will be vulnerable as a off.  Probably should factor in the 'dangerousness' of each suit.  (i.e. ThreeOne is a less dangerous off than FiveFour)"""
