
from random import SystemRandom

bones = {}
deck = []
shuffle = SystemRandom().shuffle

class Bone( object ):
    """A bone."""

    class __metaclass__( type ):
        def __repr__( cls ):
            return "%s(%dpt)" % ( cls.__name__, cls.value )

    identity = ()
    rank = {}
    value = 0
    terms = ( 'Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six' )

    @classmethod
    def construct( cls, t, b ):
        """Constructs a version of this class for the specified bone."""

        return type( '%s%s' % ( cls.terms[ t ], cls.terms[ b ] ), ( cls, ), {
            'bone': ( t, b ),
            'rank': ( { t: 7 } if t == b else { t: b, b: t } ),
            'value': ( t + b if ( t + b ) % 5 == 0 else 0 ),
        } )

class Deck( object ):
    """A deck of bones."""

    def deal( self ):
        """Deals four hands of bones."""

        shuffled = list( deck )
        shuffle( shuffled )
        return shuffled[ 0:7 ], shuffled[ 7:14 ], shuffled[ 14:21 ], shuffled[ 21:28 ]

for t in range( 6, -1, -1 ):
    for b in range( t, -1, -1 ):
        bone = bones[ ( t, b ) ] = bones[ ( b, t ) ] = Bone.construct( t, b )
        deck.append( bone )

