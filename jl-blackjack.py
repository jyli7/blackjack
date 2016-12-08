"""
This is the code for a blackjack game.
"""

from random import shuffle
from time import sleep


def get_valid_response(query, valid_responses):
    while True:
        response = raw_input(query).lower()

        if response in [r.lower() for r in valid_responses]:
            return response
        else:
            print "That is not a valid response. Try again."


class Player(object):
    def __init__(self, name, game):
        self.cards = []
        self.name = name
        self.busted = False
        self.game = game

    def __str__(self):
        return "{:10} {:>20} {:>4}".format(self.name, " ".join([str(card) for card in self.cards]), self.points())

    def receive_card(self, card, is_face_up=True):
        card.is_face_up = is_face_up
        self.cards.append(card)

    def cards_string(self):
        return [card.to_string() for card in self.cards]

    def raw_points(self):
        return sum(card.points() for card in self.cards)

    def points(self):
        total = self.raw_points()
        # Check if we should reduce the value of aces
        if total > 21:
            ace_indices = [index for index, card in enumerate(self.cards) if card.rank == 'A']
            for ace_index in ace_indices:
                self.cards[ace_index].secondary_value = True
                if self.raw_points() <= 21:
                    return self.raw_points()

        return total

    def ask_for_decision(self):
        print(self)
        return get_valid_response("Would you like to 'hit' or 'stay'?",
                                  ["hit", "stay"])

    def bust(self):
        print "\n{}, you have busted with {}. This totals {}!\n".format(self.name, self.cards_string(), self.points())
        self.busted = True

    def hit(self):
        self.game.deck.deal_card_to(self)
        if self.points() <= 21:
            self.play()
        else:
            self.bust()

    def stay(self):
        print "{} is staying with {}".format(self.name, self.points())

    def play(self):
        response = self.ask_for_decision().lower()

        while response != 'hit' and response != 'stay':
            print "Not an acceptable response. You must 'hit' or 'stay'"
            response = self.ask_for_decision()

        if response == 'hit':
            self.hit()
        else:
            self.stay()


class Dealer(Player):
    def __init__(self, game):
        Player.__init__(self, "Dealer", game)

    def play(self):
        print "\nDealer is playing..."
        sleep(0.5)
        self.cards[0].is_face_up = True
        print "Dealer has {} for a total of {}".format(self.cards_string(), self.points())
        if self.points() <= 17:
            print "Dealer is hitting..."
            sleep(0.5)
            self.hit()
        else:
            print "Dealer is staying..."
            sleep(0.5)
            self.stay()


class Deck(object):
    def __init__(self):
        self.suits = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
        self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]

    def shuffle_cards(self):
        shuffle(self.cards)

    def deal_card_to(self, player, is_face_up=True):
        card = self.cards.pop()
        player.receive_card(card, is_face_up)


class Card(object):
    score_mapping = {
        'A': [11, 1],
        'K': [10],
        'Q': [10],
        'J': [10],
        '10': [10],
        '9': [9],
        '8': [8],
        '7': [7],
        '6': [6],
        '5': [5],
        '4': [4],
        '3': [3],
        '2': [2]
    }

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.is_face_up = None
        self.secondary_value = False

    def __str__(self):
        return "{}{}".format(self.rank, self.suit)

    def points(self):
        if self.secondary_value:
            return Card.score_mapping[self.rank][-1]
        else:
            return Card.score_mapping[self.rank][0]


class Game(object):
    def __init__(self, num_players):
        self.players = []
        for i in range(0, num_players):
            player = Player("Player {}".format(i + 1), self)
            self.players.append(player)

        self.dealer = Dealer(self)
        self.deck = Deck()
        self.deck.shuffle_cards()

    def deal_initial_pair(self):
        # Deal one card face up to each player, deal one card face DOWN to himself
        self.deal_card_to_all(first_card=True)
        self.deal_card_to_all()

    def deal_card_to_all(self, first_card=False):
        for player in self.players:
            self.deck.deal_card_to(player, is_face_up=True)

        self.deck.deal_card_to(self.dealer, is_face_up=not first_card)

    def play_round(self):
        for player in [player for player in self.players if not player.busted]:
            player.play()

        self.dealer.play()

    def resolve(self):
        print "\n ---GAME RESULTS--- \n"
        sleep(0.5)

        if self.dealer.busted:
            print "Dealer has busted, so all non-busted players win!"
            print "Winners: {}".format(", ".join([player.name for player in self.players if not player.busted]))
            print "Busted players: {}".format(", ".join([player.name for player in self.players if player.busted]))

        else:
            for player in self.players:
                if player.busted:
                    print "Loser! {} has busted".format(player.name)
                elif player.points() < self.dealer.points():
                    print "Loser! {} has {} points. This is less than the dealer's total of {}.".format(player.name, player.points(), self.dealer.points())
                elif player.points() == self.dealer.points():
                    print "Tie! {} has {} points. This ties the dealer's total of {}.".format(player.name, player.points(), self.dealer.points())
                else:
                    print "Winner! {} has {} points. This is more than the dealer's total of {}. Congrats!".format(player.name, player.points(), self.dealer.points())

def play_game():
    num_players = get_num_players()
    print "Great! Let's play with {} players.".format(num_players)

    game = Game(num_players)
    game.deal_initial_pair()
    game.play_round()
    game.resolve()

    response = get_valid_response("Would you like to play again? ('yes' or 'no'): ", ['yes', 'no']).lower()
    if response == "yes":
        play_game()
    else:
        print "Thanks for playing!"


def get_num_players():
    num_players_char = get_valid_response("How many players are playing today? (Please enter a number between 1 and 6): ",
                                         ['1', '2', '3', '4', '5', '6'])

    return int(num_players_char)

if __name__ == "__main__":
    play_game()
