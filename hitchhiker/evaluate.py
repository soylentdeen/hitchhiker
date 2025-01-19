from hitchhiker.bones import Suits


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

class playEvaluation( object ):
    ''' This obejct can be used by any player to calculate legal/winning plays from their hand '''
    def __init__(self, trump, objective):
        self.trump = trump
        self.played = []   #Dominoes which are already out

    def findLegalPlays(self, hand, suit):
        trickSuit = suit
        #find if we have any of the suit
        legalPlays = []
        #If suit is NOT trump
        if (self.trump.value != trickSuit.value):
            for b in hand:
                if trickSuit.includes(b) and not(self.trump.includes(b)):
                    legalPlays.append(b)
            # If we don't have any dominoes of the suit, we can play trump, so look for trump
            if len(legalPlays) == 0:
                for b in hand:
                    if self.trump.includes(b):
                        legalPlays.append(b)
        else:
            for b in hand:
                if self.trump.includes(b):
                    legalPlays.append(b)

        return self.self.legalPlays

    def findWinningPlays(self, suit):
        trickSuit = suit

    def addPlayedDomino(self, bone):
        self.played.append(bone)


class bidEvaluation( object ):
    def __init__(self, hand, trump):
        self.hand = hand
        self.trump = trump

    def evaluate(self):
        self.trumpControl = self.controlProbability(self.trump)
        print(self.trumpControl)
        self.calculateOffs()
        print(self.offs)
        self.calculateLeadingOffs()
        print(self.leadingOffs)
        
    def distribute(self, bones, h1, h2, h3, nleads, trumps):
        """ Calculates all possible hands with the remaining trumps, figuring out which hands can wrest control from the bidder's hand. """
        # case A: studied hand CONTROLS the trumps
        # case B: studied hand has MORE trumps than any other player
        # total : counter for total number of possible hands
        if (len(bones) > 0):
            control = 0
            more = 0
            total = 0
            hand = h1[:]
            dominoes = bones[:]
            bone = dominoes.pop()
            hand.append(bone)
            result = self.distribute(dominoes, hand, h2, h3, nleads, trumps)
            control += result[0]
            more += result[1]
            total += result[-1]
            hand = h2[:]
            hand.append(bone)
            result = self.distribute(dominoes, h1, hand, h3, nleads, trumps)
            control += result[0]
            more += result[1]
            total += result[-1]
            hand = h3[:]
            hand.append(bone)
            result = self.distribute(dominoes, h1, h2, hand, nleads, trumps)
            control += result[0]
            more += result[1]
            total += result[-1]
            return [control, more, total]
        else:
            #print h1, h2, h3
            A = 1
            B = 1
            T = 1
            ntrumps = len(trumps)
            if (nleads < len(h1)):
                if ( ( ntrumps > nleads) ):
                    if ( max(h1) > trumps[nleads]):
                        A = 0
                    else:
                        A = 0
                        B = 0
            if (nleads < len(h2)):
                if ( ntrumps > nleads):
                    if (max(h2) > trumps[nleads]):
                        A = 0
                else:
                    A = 0
                    B = 0
            if (nleads < len(h3)):
                if (ntrumps > nleads):
                    if (max(h3) > trumps[nleads]):
                        A = 0
                else:
                    A = 0
                    B = 0
            if ((ntrumps<=len(h1))or(ntrumps<=len(h2))or(ntrumps<=len(h3))):
                B = 0
            return [A, B, T]

    def controlProbability(self, suit):
        """Returns the probability that the given hand controls a suit given a trump suit"""
        '''
            inputs:
            hand = list[] of bone objects
            suit = the suit in question
            trump = the trump to assume for this calculation
    
            bone is a structure containing
                bone.t - integer representing the top suit
                bone.b - integer representing the bottom suit

            returns:
                a list of normalized probabilities that the given hand
                0) controls (i.e. will be able to draw remaining trumps
                   with at least one trump left in the player's hand)
                   the given suit. Denoted P_control
                1) or has the most of any player at the table of
                   the given suit. Denoted P_majority

                return syntax [P_control, P_majority]
        '''

        # How many dominos of the suit does the hand contain?
        hand_rank = []
        # List containing ranks of the dominoes in the hand within the suit

        if (suit.value == self.trump.value):
            for b in self.hand.bones:
                if self.trump.includes(b):
                    hand_rank.append(b.rank[self.trump.value])
        else:
            for b in self.hand.bones:
                if (suit.includes(b) and not(self.trump.includes(b))):
                    hand_rank.append(b.rank[suit.value])

        hand_rank.sort()
        hand_rank.reverse()
        #How many trumps do we have?
        n_trumps = len(hand_rank)

        #Which trumps are we missing
        all_rank = [6, 5, 4, 3, 2, 1, 0]
        if (suit.value != self.trump.value):
            if suit.value > self.trump.value:
                junk = all_rank.pop(suit.value-1)
            else:
                junk = all_rank.pop(suit.value)

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

        probability =  self.distribute(missing_rank, h1, h2, h3, n_leads, hand_rank)

        P_control = float(probability[0])/float(probability[-1])
        P_majority = float(probability[1])/float(probability[-1])

        #if P_control < 0.001

        return (P_control, P_majority)

    def calculateOffs(self):
        """ Returns a dictionary list of the numbers of offs for the non-trump suits. """
        '''

        input:
            hand : list of bones in the player's hand
            trump : trump suit

        output:
            offs : { 0:#0, 1:#1, 2:#2, 3:#3, 4:#4, 5:#5, 6:#6 }
                    where #n = the number of offs in the suit of n
                    #trump == 0
                    how do we handle covered offs? (i.e. the 5:1 underneath the 5:5)
        '''
        offs = {}
        for s in [Suits['blanks'], Suits['ones'], Suits['twos'], Suits['threes'], Suits['fours'], Suits['fives'], Suits['sixes']]:
            off = 0
            for b in self.hand.bones:
                if (s.includes(b) and not(self.trump.includes(b))):
                    off += 1
            if s.value == self.trump.value:
                off = 0
            offs[s.value] = off
        self.offs = offs

    def calculateLeadingOffs(self):
        """ Returns a list of the numbers of leading offs for the non-trump suits. """
        '''

        input:
            hand : list of bones in the player's hand
            trump : trump suit

        output:
            offs : { 0:#0, 1:#1, 2:#2, 3:#3, 4:#4, 5:#5, 6:#6 }
                    where #n = the number of leading offs in the suit of n
                        A leading off is the suit an off will lead to if it
                        is played first in a trick (i.e. 5:3 leads to the fives)
                    #trump == 0
                    how do we handle covered offs? (i.e. the 5:1 underneath the 5:5)
        '''
        offs = {}
        for s in [Suits['blanks'],Suits['ones'],Suits['twos'],Suits['threes'],Suits['fours'],Suits['fives'],Suits['sixes']]:
            off = 0
            for b in self.hand.bones:
                if (s.includes(b) and not(self.trump.includes(b))):
                    if (b.rank[s.value] <= s.value):
                        off += 1
            if s.value == self.trump.value:
                off = 0
            offs[s.value] = off
        self.leadingOffs = offs

    def calcVulnerability(self, trump, bone):
        totalWays = 0
        leadingWays = 0
        if not(trump.includes(bone)):
            for s in [Suits['blanks'], Suits['ones'], Suits['twos'], Suits['threes'], Suits['fours'], Suits['fives'], Suits['sixes']]:
                if (s.includes(bone)):
                    totalWays += self.offs[s.value]
                    leadingWays += self.leadingOffs[s.value]

        return [totalWays, leadingWays]

    def calculateLeadProbability(self, hand, suit):
        """Returns a list corresponding to the probabilities that each domino in HAND will be able to used as a winning lead, assuming SUIT is trump"""

    def calculateOffProbability(self, hand, suit):
        """Returns a list corresponding to the probabilities that each domino in HAND will be vulnerable as a off.  Probably should factor in the 'dangerousness' of each suit.  (i.e. ThreeOne is a less dangerous off than FiveFour)"""
