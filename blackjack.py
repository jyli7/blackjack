"""
This is the code for a blackjack game.

Objects in this game:

Deck
Card

Player
Dealer(Player)

GameManager?
"""

from random import shuffle
from time import sleep

class Player:
    def __init__(self, name):
        self.cards = []
        self.name = name

    def receive_card(self, card, is_face_up = True):
        card.is_face_up = is_face_up
        self.cards.append(card)

class Dealer(Player):
    def __init__(self):
        Player.__init__(self, "Dealer")

class Deck:
    def __init__(self):
        self.suits = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
        self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]

    def shuffle_cards(self):
        shuffle(self.cards)

    def deal_card_to(self, player, is_face_up = True):
        card = self.cards.pop()
        player.receive_card(card, is_face_up)

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.is_face_up = None

    def to_string(self):
        if not self.is_face_up:
            return "*"
        else:
            return "{}{}".format(self.rank, self.suit)

class Game:
    def __init__(self, num_players):
        self.players = []
        for i in range(0, num_players):
            player = Player("Player {}".format(i))
            self.players.append(player)

        self.dealer = Dealer()
        self.deck = Deck()

    def print_state(self):
        for player in self.players + [self.dealer]:
            print "{} has cards: {}".format(player.name, [card.to_string() for card in player.cards])
            sleep(1)

        print

def play_game(num_players):
    game = Game(num_players)

    # Deal one card face up to each player, deal one card face DOWN to himself
    print "Dealing first card to players..."
    sleep(2)
    for player in game.players:
        game.deck.deal_card_to(player, is_face_up = True)

    game.deck.deal_card_to(game.dealer, is_face_up = False)

    game.print_state()

    # Deal one card face up to each player, deal one card face UP to himself
    print "Dealing second card to players..."
    sleep(2)

    for player in game.players:
        game.deck.deal_card_to(player, is_face_up = True)

    game.deck.deal_card_to(game.dealer, is_face_up = True)

    sleep(1)
    game.print_state()


    # Now each player gets to decide what to do, either hitting n times and busting or hitting n times and standing
    # After each player is done, but the dealer turns over his hole card. Then, he plays based on a rule. If the dealer has a soft 17 or below, dealer must hit.
    # If dealer busts, all players left in the game win.
    # If dealer does not bust, players left that have higher point totals win, and players left with lower point totals lose. Same point total -> draw.


def get_num_players():
    raw_num_players = raw_input("How many players are playing today? (Please enter a number between 1 and 6): ")

    try:
        num_players = int(raw_num_players)
        if num_players <= 0 or num_players > 6:
            raise TypeError
    except:
        print "That was not a valid input. Please try again."
        get_num_players()
    else:
        return num_players

def main():
    num_players = get_num_players()
    print "Great! Let's play with {} players.".format(num_players)
    play_game(num_players)


if __name__ == "__main__":
	main()