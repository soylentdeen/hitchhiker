
from hitchhiker.bones import RandomDeck, Suits, Bones
from hitchhiker.contract import Bid, TrumpContract
from hitchhiker.util import reorder, shuffle
from hitchhiker.evaluate import *
#from hitchhiker.evaluate import controlProbability, calculateOffs, calculateLeadingOffs, calcBid

class Player( object ):
    """A player in a particular game."""

    def __init__( self, team, name, controller ):
        """Constructor."""

        self.controller = controller    #
        self.hand = None                #
        self.name = name                #  Name of player
        self.team = team                #
        self.trick_evaluation = None    #  trick_evaluation object

    def __repr__( self ):
        return 'Player(%s)' % self.name

    def __str__( self ):
        return self.name

    def offer( self, round ):
        """Offer a bid for the specified round."""

        print
        print '%s has: %s' % ( self.name, self.hand.dump() )
        print '                             : CONTROL : MAJORITY'
        evaluation = []
        for s in [Suits['blanks'], Suits['ones'], Suits['twos'], Suits['threes'], Suits['fours'], Suits['fives'], Suits['sixes']]:
            evaluation.append(bidEvaluation(self.hand, s))
            evaluation[-1].evaluate()

            '''
            print '5:5 vulnarability : ', calcVulnerability(offs, leadingOffs, s, Bones[(5, 5)]())
            print '6:4 vulnerability : ', calcVulnerability(offs, leadingOffs, s, Bones[(6, 4)]())
            print controlProbability(self.hand, Suits['fours'], s)
            print controlProbability(self.hand, Suits['sixes'], s)
            print '4:1 vulnerability : ', calcVulnerability(offs, leadingOffs, s, Bones[(4, 1)]())
            print '3:2 vulnerability : ', calcVulnerability(offs, leadingOffs, s, Bones[(3, 2)]())
            print '5:0 vulnerability : ', calcVulnerability(offs, leadingOffs, s, Bones[(5, 0)]())
            '''
        #bid = []
        #for e in evaluation:
        #    bid.append(e[0], calcBid(e))
        bid = raw_input( 'Bid (enter to pass): ' )
        if bid:
            trump = raw_input( 'Trump: ' )
            return Bid( self, TrumpContract( Suits[ trump ] ), int( bid ) )

    def play( self, trick ):
        """Plays a bone in the specified trick."""

        print
        print 'trick is: %s' % ( trick.dump() )
        print '%s has: %s' % ( self.name, self.hand.dump() )
        #print 'legal moves are %s' % ( self.
        identity = eval( raw_input( 'Play: ' ) )

        bone = self.hand.play( identity )
        return bone       

class Team( object ):
    """A team in a particular game."""

    def __init__( self, name ):
        """Constructor."""

        self.name = name
        self.players = []

    def __repr__( self ):
        return 'Team( %s: %s )' % ( self.name, ', '.join([ str( player ) for player in  self.players ]) )

    def __str__( self ):
        return self.name

    @property
    def shuffled_players( self ):
        """A list of players for this team in random order."""

        players = list( self.players )
        shuffle( players )
        return players

    def add( self, name, controller ):
        """Adds a player to this team."""

        self.players.append( Player( self, name, controller ) )

class Hand( object ):
    """A hand of bones for a particular round."""

    def __init__( self, round, player, hand ):
        """Constructor."""

        self.bones = hand
        self.hand = dict( ( bone.identity, bone ) for bone in hand )
        self.player = player
        self.round = round

    def __repr__( self ):
        """String representation."""

        bones = ' '.join([ repr( bone ) for bone in self.bones ])
        return 'Hand( %s %s )' % ( self.player, bones )

    def dump( self ):
        """ Prints a String representation for the bones left in the hand. """
        return ' '.join([ repr( bone ) for bone in self.hand.itervalues() ])

    def play( self, identity ):
        """Plays a bone from this hand."""

        bone = self.hand.pop( identity, None )
        if bone:
            return bone
        else:
            raise KeyError( 'invalid bone' )

class Play( object ):
    """A played bone in a particular trick."""

    def __init__( self, trick, id, player, bone, suit, trump ):
        """Constructor."""

        self.bone = bone
        self.id = id
        self.player = player
        self.role = 'unknown'
        self.suit = suit
        self.trick = trick
        self.trump = trump

    def __repr__( self ):
        """String representation."""

        return 'Play( r%d:t%d:p%d %r %s by %s )' % ( self.trick.round.id, self.trick.id,
            self.id, self.bone, self.role, self.player )

class Trick( object ):
    """A trick in a particular round."""

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

    def dump( self ):
        return ' '.join([ repr( play.bone ) for play in self.plays ])

    def play( self, player, bone ):
        """Plays the specified bone in this trick."""

        # construct the play and associate it with the trick
        suit, trump = self.round.bid.contract.identify( self, bone )
        play = Play( self, len( self.plays ) + 1, player, bone, suit, trump )
        self.plays.append( play )

        # determine the effects of the play
        self.value += bone.value
        if self.winning_play:                # If this NOT is the first bone in the trick, figure out if it is a winner
            self.round.bid.contract.adjudicate( self, player, play )
            print 'bone is a %s' % play.role
        else:                                # else, THIS is the winning play, by default, as it is the first bone in the trick
            play.role = 'suit'
            self.suit, self.winning_play, self.winning_player = play.suit, play, player
            print 'trick suit is %s' % self.suit.identity

class Round( object ):
    """A round in a particular game."""

    def __init__( self, game, id, players, bid = None ):
        """Constructor."""
    
        self.bid = bid
        self.game = game
        self.hands = []
        self.id = id
        self.marks = 1
        self.players = players
        self.points_made = 0
        self.points_set = 0
        self.status = 'unknown'
        self.tricks = []

    @property
    def points_to_make( self ):
        """Indicates the points remaining for this bid to be made."""
        return self.bid.bid - self.points_made

    @property
    def points_to_set( self ):
        """Indicates the points remaining for this bid to be set."""
        return ( 43 - self.bid.bid ) - self.points_set

    def deal( self ):
        """Deals a hand to each player in this round."""

        hands = self.game.deck.deal()
        for hand, player in zip( hands, self.players ):
            player.hand = Hand( self, player, hand )
            self.hands.append( player.hand )

    def run( self ):
        """Runs this round."""

        # deal a hand to each player, then collect the bids
        print '%r vs. %r' % ( self.game.home, self.game.away )
        self.deal()
        for player in self.players:
            bid = player.offer( self )
            if bid:
                self.bid = bid
        else:
            if not self.bid:
                return None
            else:
                for player in self.players:
                    player.trick_evaluation = evaluate.playEvaluation(

        # identify the number of marks for this hand, then normalize the bid value
        target = self.bid.bid
        if bid > 42:
            self.marks, target = target / 42, 42

        # play tricks until the round is complete
        player = self.bid.player
        while True:

            # create the next trick and request a play from each player
            trick = Trick( self, len( self.tricks ) + 1, reorder( self.players, player ) )
            for player in trick.players:
                trick.play( player, player.play( trick ) )

            # reference the winning player and update the points totals
            player = trick.winning_player
            if player.team is self.bid.player.team:
                self.points_made += trick.value
            else:
                self.points_set += trick.value

            # associate the trick with this round and determine if the round is over
            self.tricks.append( trick )
            if self.points_made >= target:
                print 'BID WAS MADE'
                self.status = 'made'
                break
            elif self.points_set >= ( 43 - target ):
                print 'BID WAS SET'
                self.status = 'set'
                break

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

