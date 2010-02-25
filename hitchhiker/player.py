
from hitchhiker.util import shuffle

class Player( object ):
    """A player."""

    def __init__( self, name ):
        """Constructor."""

        self.name = name

    def __repr__( self ):
        return 'Player(%s)' % self.name

    def __str__( self ):
        return self.name

class Team( object ):
    """A team."""

    def __init__( self, name, players ):
        """Constructor."""

        self.name = name
        self.players = players

    def __repr__( self ):
        return 'Team(%s)' % self.name

    def __str__( self ):
        return self.name

    @property
    def shuffled_players( self ):
        """A list of players for this team in random order."""

        players = list( self.players )
        shuffle( players )
        return players

