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

    print hand_rank
    #How many trumps do we have?
    n_trumps = len(hand_rank)

    #Which trumps are we missing
    all_rank = [6, 5, 4, 3, 2, 1, 0]
    # N.B. : This list represents the rank of the dominoes
    # NOT the number of dots! i.e. 6 = double, 5 = next highest

    # Assuming the "critical" domino is in an opposing hand, what is
    # number of possible hands from the remaining 20 dominos?
    total_hands = Combination(20, 6)
    
    # Finds the ranks of the missing trumps NOT in the player's hand
    missing_rank = [b for b in all_rank if not b in hand_rank]
    n_missing_trumps = len(missing_rank)

    # Based on number of trumps still out, figure out the
    # minimum cover, assuming even distribution
    # i.e.  if player only has double (6-6), there are 6 dominos
    # still out.  Even distribution -> 2 trumps in each hand
    # 6-5 will be covered by at least 1.  Unrealistic to look at case
    # with no cover for 6-5, as if 6-5 is uncovered, another hand will
    # have covered dominoes.

    # This needs to be improved... [double, blank] still gives non-zero probability 
    # Sometimes gives Prob > 1
    min_cover = max((n_missing_trumps / 3)-1, 0)

    # Probability of each "Off" in missing_rank being "safe" for bidder
    Probability = []
    for crit_rank in missing_rank:
        # Crit_rank is the rank of the "critical" domino
        # which can wrest control if it not drawn out with
        # higher dominoes from the player's hand.
        
        # Add new probability
        Probability.append(0.0)
        
        winning_trumps = [b for b in hand_rank if b > crit_rank]

        # Calculate how many 'cover' dominos the posessor of the critical
        # domino needs in order to retain the critical domino until
        # it is the high trump
        #necessary_cover = 6 - crit_rank
        necessary_cover = len(winning_trumps)
        
        #print "Critical Ranking :"+str(crit_rank)
        #print "Necessary Cover :"+str(necessary_cover)

        # probably need to do multiple hands... if 6-5 is bare, that means 6-4 will be doubled up
        
        for trmp in range(min_cover, necessary_cover):
            #print trmp
            offs_prob = Combination(20-n_missing_trumps, 6-trmp)
            #print offs_prob.frac.num
            #print offs_prob.frac.denom
            trmp_prob = Combination(n_missing_trumps, trmp)
            #print trmp_prob.frac.num
            #print trmp_prob.frac.denom
            prob = offs_prob.frac
            prob * trmp_prob.frac
            prob / total_hands.frac
            #print prob.eval()
            Probability[-1] += prob.eval()
            #raw_input()
        print crit_rank, winning_trumps, necessary_cover, min_cover, Probability[-1]

    prob = 1.0 if Probability else 0.0
    for p in Probability:
        prob *= p

    return prob

    # How many winning leads does the hand contain?

    # How many dominoes must a potential "spoiler" have to protect his/her high domino?

    # What is the probability for each potential "spoiler"?

    # What is the aggregate probability?
    
def calculateLeadProbability(hand, suit):
    """Returns a list corresponding to the probabilities that each domino in HAND will be able to used as a winning lead, assuming SUIT is trump"""

def calculateOffProbability(hand, suit):
    """Returns a list corresponding to the probabilities that each domino in HAND will be vulnerable as a off.  Probably should factor in the 'dangerousness' of each suit.  (i.e. ThreeOne is a less dangerous off than FiveFour)"""
