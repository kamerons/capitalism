from enum import Enum

from colorama import init, Fore, Back, Style

init()

class Rank(Enum):
	TWO		= 2
	THREE	= 3
	FOUR	= 4
	FIVE	= 5
	SIX		= 6
	SEVEN	= 7
	EIGHT	= 8
	NINE	= 9
	TEN		= 10
	JACK	= 11
	QUEEN	= 12
	KING	= 13
	ACE		= 14
	JOKER	= 15

	def __str__(self):
		if (self.value <= 10):
			return str(self.value)
		elif self == Rank.JACK:
			return "J"
		elif self == Rank.QUEEN:
			return "Q"
		elif self == Rank.KING:
			return "K"
		elif self == Rank.ACE:
			return "A"
		else:
			return "W"


	def __repr__(self):
		return self.__str__()


class Color(Enum):
	RED = 1
	BLACK = 2

	def getCode(self):
		if self == Color.RED:
			return Fore.RED
		return Fore.WHITE


class Suit(Enum):
	CLUBS			= 1
	DIAMONDS	= 2
	HEARTS		= 3
	SPADES		= 4
 

	def getColor(self):
		if self.value % 2 == 0:
			return Color.BLACK
		return Color.RED


	def __str__(self):
		if self == Suit.CLUBS:
			return "\u2663"
		elif self == Suit.DIAMONDS:
			return "\u2662"
		elif self == Suit.HEARTS:
			return "\u2665"
		else:
			return "\u2660"
	

	def __repr__(self):
		return self.__str__()


class Card():

	def __init__(self, rank, suit, color=None):
		self.rank = rank
		if color is None:
			self.suit = suit
			self.color = suit.getColor()
		else:
			self.suit = None
			self.color = color


	def __str__(self):
		if self.suit is None:
			return "%s_%s%s" % (self.color.getCode(), str(self.rank), Style.RESET_ALL)
		return "%s%s%s%s" % (self.color.getCode(), str(self.suit), str(self.rank), Style.RESET_ALL)


	def __repr__(self):
		return self.__str__()


class Deck():

	def __init__(self):
		self.cards = []
		for rank in list(Rank):
			if rank == Rank.JOKER:
				self.cards.append(Card(Rank.JOKER, None, Color.RED))
				self.cards.append(Card(Rank.JOKER, None, Color.BLACK))
			else:
				for suit in list(Suit):
					self.cards.append(Card(rank, suit))
