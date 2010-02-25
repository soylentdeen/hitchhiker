
class Player( object ):
    """A player."""

    def __init__( self, name ):
        """Constructor."""

        self.name = name

class Team( object ):
    """A team."""

    def __init__( self, name, players ):
        """Constructor."""

        self.name = name
        self.players = players

