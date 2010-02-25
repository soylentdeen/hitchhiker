
from random import SystemRandom

Bones = {}
Deck = []
Suits = {}

class Bone( object ):
    """A bone."""

    class __metaclass__( type ):
        def __repr__( cls ):
            return "%s(%dpt)" % ( cls.__name__, cls.value )

    identity = ()
    rank = {}
    suits = ()
    value = 0
    terms = ( 'Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six' )

    def __lt__( self, other ):
        return self.identity > other.identity

    def __repr__( self ):
        return '%d:%d' % self.identity

    @classmethod
    def construct( cls, t, b ):
        """Constructs a version of this class for the specified bone."""

        return type( '%s%s' % ( cls.terms[ t ], cls.terms[ b ] ), ( cls, ), {
            'identity': ( t, b ),
            'rank': ( { t: 7 } if t == b else { t: b, b: t } ),
            'value': ( t + b if ( t + b ) % 5 == 0 else 0 ),
        } )

for t in range( 6, -1, -1 ):
    for b in range( t, -1, -1 ):
        bone = Bones[ ( t, b ) ] = Bones[ ( b, t ) ] = Bone.construct( t, b )
        Deck.append( bone )

def suit( suit ):
    """Constructs a suit implementation."""

    suit.bones = tuple([ Bones[ bone ] for bone in suit.bones ])
    if suit.value is not None:
        for bone in suit.bones:
            if bone.suits:
                if bone.suits[ 0 ].value > suit.value:
                    bone.suits = ( bone.suits[ 0 ], suit )
                else:
                    bone.suits = ( suit, bone.suits[ 0 ] )
            else:
                bone.suits = ( suit, )

    Suits[ suit.identity ] = suit
    return suit

class Suit( object ):
    """A suit."""

    bones = ()
    identity = None
    value = None

    @classmethod
    def higher( cls, first, second ):
        """Indicates if the first bone is higher than the second bone within this suit."""

        return cls.bones.index( type( first ) ) < cls.bones.index( type( second ) )

@suit
class Sixes( Suit ):
    bones = ( (6,6), (6,5), (6,4), (6,3), (6,2), (6,1), (6,0) )
    identity = 'sixes'
    value = 6

@suit
class Fives( Suit ):
    bones = ( (5,5), (5,6), (5,4), (5,3), (5,2), (5,1), (5,0) )
    identity = 'fives'
    value = 5

@suit
class Fours( Suit ):
    bones = ( (4,4), (4,6), (4,5), (4,3), (4,2), (4,1), (4,0) )
    identity = 'fours'
    value = 4

@suit
class Threes( Suit ):
    bones = ( (3,3), (3,6), (3,5), (3,4), (3,2), (3,1), (3,0) )
    identity = 'threes'
    value = 3

@suit
class Twos( Suit ):
    bones = ( (2,2), (2,6), (2,5), (2,4), (2,3), (2,1), (2,0) )
    identity = 'twos'
    value = 2

@suit
class Ones( Suit ):
    bones = ( (1,1), (1,6), (1,5), (1,4), (1,3), (1,2), (1,0) )
    identity = 'ones'
    value = 1

@suit
class Blanks( Suit ):
    bones = ( (0,0), (0,6), (0,5), (0,4), (0,3), (0,2), (0,1) )
    identity = 'blanks'
    value = 0

@suit
class Doubles( Suit ):
    bones = ( (6,6), (5,5), (4,4), (3,3), (2,2), (1,1), (0,0) )
    identity = 'doubles'
    value = None

class RandomDeck( object ):
    """A deck of bones."""

    def __init__( self, handsize = 7, handcount = 4, multiplier = 1, deck = Deck ):
        """Constructor."""

        self.deck = deck
        self.handcount = handcount
        self.handsize = handsize
        self.multiplier = multiplier

    def deal( self, shuffle = SystemRandom().shuffle ):
        """Deals hands in random order."""

        # shuffle a new deck of bones
        deck = list( self.deck ) * self.multiplier
        shuffle( deck )

        # create and return the proper number of hands
        hands, handsize = [], self.handsize
        for i in range( self.handcount ):
            offset = i * handsize
            hands.append( tuple( sorted( bone() for bone in deck[ offset:offset + handsize ] ) ) )
        else:
            return tuple( hands )

