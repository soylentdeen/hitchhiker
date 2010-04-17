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
            normalized probability that the given hand controls (i.e. will be able to draw remaining trumps with at least one left over) the given suit.
    '''

    # How many dominos of the suit does the hand contain?
    hand_rank = []    # List containing ranks of the dominoes in the hand within the suit

    for b in hand.bones:
        if trump.includes(b):
            hand_rank.append(b.rank[trump.value])

    #How many trumps do we have?
    n_trumps = len(hand_rank)

    #Which trumps are we missing
    all_rank = [6, 5, 4, 3, 2, 1, 0]   # N.B. : This list represents the rank of the dominoes
                                       # NOT the number of dots!
                                       # i.e. 6 = double, 5 = next highest

    missing_rank = [b for b in all_rank if not b in hand_rank]

    print missing_rank
    print max(missing_rank)
    return 0.0
    # How many winning leads does the hand contain?

    #suit_rank = []
    #for b in trumps:
    #    if ( b.t == b.b ):   # it's the double
    #        suit_rank.append(7)
    #    elif (b.t == suit):
    #        suit_rank.append(b.b)
    #    else:
    #        suit_rank.append(b.t)

    #suit_rank.sort(reverse=True)
    #:
    #for b in suit_rank:
    #    b

    # How many dominoes must a potential "spoiler" have to protect his/her high domino?

    # What is the probability for each potential "spoiler"?

    # What is the aggregate probability?
    
def calculateLeadProbability(hand, suit):
    """Returns a list corresponding to the probabilities that each domino in HAND will be able to used as a winning lead, assuming SUIT is trump"""

def calculateOffProbability(hand, suit):
    """Returns a list corresponding to the probabilities that each domino in HAND will be vulnerable as a off.  Probably should factor in the 'dangerousness' of each suit.  (i.e. ThreeOne is a less dangerous off than FiveFour)"""
