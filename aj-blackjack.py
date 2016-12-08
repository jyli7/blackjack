
#!/usr/bin/python3
import itertools
import random
import sys

nums = ('2','3','4','5','6','7','8','9','10','J','Q','K','A')
suits = ('♠','♥','♦','♣')

try:
    num_players = int(sys.argv[1])
except:
    num_players = 1

class Card():
    def __init__(self, num, suit):
        self.num = num
        self.suit = suit

    def __str__(self):
        return "%s%s" % (self.num, self.suit)

    def add_value(self, val):
        if self.num == 'A':
            return [val + 1, val + 11]
        return [val + min(nums.index(self.num) + 2, 10)]

class Player():
    def __init__(self, name):
        self.name = name
        self.hand = []

    def values(self):
        vals = [ 0 ]
        for h in self.hand:
            # Set instead of list because multiple aces can yield duplicate values.
            vals = set(itertools.chain.from_iterable(map(lambda v: h.add_value(v), vals)))
        return sorted(vals)

    def deal(self, card):
        self.hand.append(card)

    def max_valid(self):
        return max(filter(lambda x: x <= 21, self.values()), default=-1)

    def __str__(self):
        return "%-10s %-20s %s" % (self.name, " ".join(map(str, self.hand)), self.values())

def deal_hand(player, hitfunc):
    print()
    print(player)
    while True:
        if player.max_valid() < 0:
            print("Busted!")
            break
        elif 21 in player.values():
            print("Blackjack!")
            break
        elif not hitfunc(player):
            break
        player.deal(deck.pop())
        print(player)

def player_func(p):
    while True:
        a = input("Enter 'h' to hit or 's' to stay: ").lower()
        if a in ('h', 's'):
            break
    return a == 'h'

deck = [ Card(n, s) for n, s in itertools.product(nums, suits) ]
random.shuffle(deck)

players = [ Player("Player " + str(n+1)) for n in range(num_players) ]
dealer = Player("Dealer")

for p in (players + [dealer]) * 2:
    # For now, we ignore the case where there are so many players
    # and/or hits that we run out of cards in the deck.
    p.deal(deck.pop())

print("Dealer shows %s" % dealer.hand[0])

for p in players:
    deal_hand(p, player_func)

# Dealer has to go until 17+ or bust. Adjust the hitfunc to look for
# aces if you want the dealer to hit on a soft 17.
deal_hand(dealer, lambda p: p.max_valid() < 17)

print()
for p in players:
    if p.max_valid() >= 0 and p.max_valid() >= dealer.max_valid():
        print("%s wins!" % p.name)
    else:
        print("%s loses!" % p.name)
