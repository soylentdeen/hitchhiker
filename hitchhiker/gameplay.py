
from hitchhiker.bones import RandomDeck
from hitchhiker.util import shuffle

class Play( object ):
    """A played bone."""

    def __init__( self, trick, id, player, bone ):
        """Constructor."""

        self.bone = bone
        self.id = id
        self.player = player
        self.role = 'unknown'
        self.trick = trick
        self.suit, self.trump = trick.round.contract.identify( trick, bone )

    def __repr__( self ):
        """String representation."""

        return 'Play( r%d:t%d:p%d %r %s by %s )' % ( self.trick.round.id, self.trick.id,
            self.id, self.bone, self.role, self.player )

class Trick( object ):
    """A trick."""

    def __init__( self, round, id, players ):
        """Constructor."""

        self.id = id
        self.players = players
        self.plays = []
        self.round = round
        self.suit = None
        self.value = 1
        self.winning_play = None
        self.winning_player = None

    def __repr__( self ):
        """String representation."""

        plays = ' '.join([ repr( play.bone ) for play in self.plays ])
        return 'Trick( r%d:t%d [ %s ] won by %s with %r for %dpt )' % ( self.round.id,
            self.id, plays, self.winning_player, self.winning_play.bone, self.value )

    def play( self, player, bone ):
        """Plays the specified bone in this trick."""

        # construct the play and associate it with the trick
        play = Play( self, len( self.plays ) + 1, player, bone )
        self.plays.append( play )

        # determine the effects of the play
        self.value += bone.value
        if self.winning_play:
            self.round.contract.adjudicate( self, player, play )
        else:
            play.role = 'suit'
            self.suit, self.winning_play, self.winning_player = play.suit, play, player

class Round( object ):
    """A round."""

    def __init__( self, game, id, players, bid = None, contract = None ):
        """Constructor."""

        self.bid = bid
        self.contract = contract
        self.game = game
        self.id = id
        self.marks = 1
        self.players = players
        self.trick = 0
        self.tricks = []

class Game( object ):
    """A game."""

    DefaultDeck = RandomDeck

    def __init__( self, home, away, deck = None, players = None ):
        """Constructor."""

        self.away = away
        self.deck = deck or self.DefaultDeck()
        self.home = home
        self.players = players or self.seat( home, away )
        self.rounds = []

    def seat( self, home, away ):
        """Determines a suitable seating order for the specified teams."""

        # shuffle the set of players for this game
        players = [ home.shuffled_players, away.shuffled_players ]
        shuffle( players )

        # generate the seating order for this game
        seating = []
        for pair in zip( *players ):
            seating.extend( pair )
        else:
            return seating

