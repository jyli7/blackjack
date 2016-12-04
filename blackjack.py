"""
This is the code for a blackjack game.

Objects in this game:

Deck
Card

Player
Dealer(Player)

GameManager?
"""

def play_game(num_players):
    pass

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