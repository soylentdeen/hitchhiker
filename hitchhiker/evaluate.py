from hitchiker.gameplay import Player

def controlProbability(hand, suit):
    """Returns the probability that the given hand controls the given trump suit"""
    '''
        inputs:
        hand = list[] of bone objects
        suit = integer representing the trump suit in question

        bone is a structure containing
            bone.t - integer representing the top suit
            bone.b - integer representing the bottom suit

        returns:
            normalized probability that the given hand controls (i.e. will be able to draw remaining trumps with at least one left over) the given suit.
    '''

   # How many dominos of the suit does the hand contain?

   ntrumps = 0
   trumps = []

   for bone in hand:
       if ((bone.t == suit) or (bone.b == suit)):
           ntrumps += 1
           trumps.append(bone)


   # How many winning leads does the hand contain?

   suit_rank = []
   for b in trumps:
       if ( b.t == b.b ):   # it's the double
           suit_rank.append(7)
       elif (b.t == suit):
           suit_rank.append(b.b)
       else:
           suit_rank.append(b.t)

   rank = suit_rank.argsort()

   # How many dominoes must a potential "spoiler" have to protect his/her high domino?

   # What is the probability for each potential "spoiler"?

   # What is the aggregate probability?
    
def calculateLeadProbability(hand, suit):
    """Returns a list corresponding to the probabilities that each domino in HAND will be able to used as a winning lead, assuming SUIT is trump"""

def calculateOffProbability(hand, suit):
    """Returns a list corresponding to the probabilities that each domino in HAND will be vulnerable as a off.  Probably should factor in the 'dangerousness' of each suit.  (i.e. ThreeOne is a less dangerous off than FiveFour)"""
