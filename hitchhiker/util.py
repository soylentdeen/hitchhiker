
from random import SystemRandom

shuffle = SystemRandom().shuffle

def reorder( sequence, item ):
    """Provides a copy of the specified sequence, in order starting with the specified item."""

    index = sequence.index( item )
    return sequence[ index: ] + sequence[ :index ]

