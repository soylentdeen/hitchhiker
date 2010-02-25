
from random import SystemRandom

StandardBones = {}
StandardDeck = []

class Bone( object ):
    """A bone."""

    class __metaclass__( type ):
        def __repr__( cls ):
            return "%s(%dpt)" % ( cls.__name__, cls.value )

    identity = ()
    rank = {}
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

class Hand( object ):
    """A hand of bones."""

    def __init__( self, hand ):
        """Constructor."""

        self.hand = hand

class Deck( object ):
    """A deck of bones."""

    def __init__( self, handsize = 7, handcount = 4, multiplier = 1, deck = StandardDeck ):
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

for t in range( 6, -1, -1 ):
    for b in range( t, -1, -1 ):
        bone = StandardBones[ ( t, b ) ] = StandardBones[ ( b, t ) ] = Bone.construct( t, b )
        StandardDeck.append( bone )

