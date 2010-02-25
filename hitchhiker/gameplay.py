
class Play( object ):
    """A played bone."""

    def __init__( self, trick, id, player, bone ):
        """Constructor."""

        self.bone = bone
        self.id = id
        self.player = player
        self.role = 'unknown'
        self.trick = trick
        self.trump = False

        trump = trick.round.trump
        if trump and bone in trump.bones:
            self.suit, self.trump = trump, True
        elif trick.suit and bone in trick.suit.bones:
            self.suit = trick.suit
        else:
            self.suit = bone.suits[ 0 ]

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
        self.value += bone.value

        # determine the effects of the play
        trump, winner = self.round.trump, self.winning_play
        if winner:
            if play.trump:
                if self.suit is trump:
                    play.role = 'suit'
                    if trump.higher( play.bone, winner.bone ):
                        self.winning_play, self.winning_player = play, player
                else:
                    play.role = 'trump'
                    if not winner.trump or trump.higher( play.bone, winner.bone ):
                        self.winning_play, self.winning_player = play, player
            elif play.suit is self.suit:
                play.role = 'suit'
                if self.suit.higher( play.bone, winner.bone ):
                    self.winning_play, self.winning_player = play, player
            else:
                play.role = 'off'
        else:
            play.role = 'suit'
            self.suit, self.winning_play, self.winning_player = play.suit, play, player

class Round( object ):
    """A round."""

    def __init__( self, game, id, players, bid = None, trump = None ):
        """Constructor."""

        self.bid = bid
        self.game = game
        self.id = id
        self.players = players
        self.trick = 0
        self.tricks = []
        self.trump = trump

class Game( object ):
    """A game."""

    def __init__( self, players ):
        """Constructor."""

        self.players = players
        self.rounds = []


if __name__ == '__main__':
    from deck import Suits, Bones
    r = Round( None, 1, ( 1, 2, 3, 4 ), trump = Suits['sixes'] )
    t1 = Trick( r, 1, ( 1, 2, 3, 4 ) )
    t1.play( 1, Bones[(6,4)]() )
    t1.play( 2, Bones[(5,3)]() )
    t1.play( 3, Bones[(6,3)]() )
    t1.play( 4, Bones[(6,6)]() )
    print t1
