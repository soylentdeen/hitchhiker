
class Contract( object ):
    """A contract."""

    def adjudicate( self, trick, player, play ):
        """Determine the result of the specified play in the specified trick."""

    def identify( self, trick, bone ):
        """Identifies the suit and trump status of the specified bone in the specified trick."""

class TrumpContract( Contract ):
    """A trumps contract."""

    def __init__( self, trump ):
        """Constructor."""

        self.trump = trump

    def adjudicate( self, trick, player, play ):
        """Determine the result of the specified play in the specified trick."""

        trump, winner = self.trump, trick.winning_play
        if play.trump:
            if trick.suit is trump:
                play.role = 'suit'
                if trump.higher( play.bone, winner.bone ):
                    trick.winning_play, trick.winning_player = play, player
            else:
                play.role = 'trump'
                if not winner.trump or trump.higher( play.bone, winner.bone ):
                    trick.winning_play, trick.winning_player = play, player
        elif play.suit is trick.suit:
            play.role = 'suit'
            if trick.suit.higher( play.bone, winner.bone ):
                trick.winning_play, trick.winning_player = play, player
        else:
            play.role = 'off'
        
    def identify( self, trick, bone ):
        """Identifies the suit and trump status of the specified bone in the specified trick."""

        if bone in self.trump.bones:
            return self.trump, True
        elif trick.suit and bone in trick.suit.bones:
            return trick.suit, False
        else:
            return bone.suits[ 0 ], False

class NoTrumpContract( Contract ):
    """A no trump contract."""

    def __init__( self, doubles = 'high' ):
        """Constructor."""

        self.doubles = doubles

    def adjudicate( self, trick, player, play ):
        """Determine the result of the specified play in the specified trick."""

        winner = trick.winning_play
        if play.suit in trick.suit:
            play.role = 'suit'
            if trick.suit.higher( play.bone, winner.bone ):
                trick.winning_play, trick.winning_player = play, player
        else:
            play.role = 'off'

    def identify( self, trick, bone ):
        """Identifies the suit and trump status of the specified bone in the specified trick."""

        if trick.suit and bone in trick.suit.bones:
            return trick.suit, False
        else:
            return bone.suits[ 0 ], False

