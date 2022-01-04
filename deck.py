from enum import Enum

from colorama import init, Fore, Back, Style

init()

class Rank(Enum):
	ACE		= 0
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
	JOKER	= 14

	def __str__(self):
		if self == Rank.ACE:
			return "A"
		elif self == Rank.JACK:
			return "J"
		elif self == Rank.QUEEN:
			return "Q"
		elif self == Rank.KING:
			return "K"
		elif self == Rank.JOKER:
			return "W"
		else:
			return str(self.value)


	def __repr__(self):
		return self.__str__()

	def rank_sort_order(self):
		if self == Rank.ACE:
			return Rank.KING.value + .3
		elif self == Rank.TWO:
			return Rank.KING.value + .6
		else:
			return self.value


class Color(Enum):
	RED = 1
	BLACK = 2

	def getCode(self):
		if self == Color.RED:
			return Fore.RED
		return Fore.WHITE


class Suit(Enum):
	SPADES		= 0
	HEARTS		= 1
	DIAMONDS	= 2
	CLUBS			= 3 

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
		if True:
			if self.suit is None:
				return "%s_%s%s" % (self.color.getCode(), str(self.rank), Style.RESET_ALL)
			return "%s%s%s%s" % (self.color.getCode(), str(self.suit), str(self.rank), Style.RESET_ALL)
		else:
			if self.rank == Rank.JOKER:
				unicode_char = "\U0001f0df"
			else:
				base_card = ord("\U0001f0a0")
				rank_offset = self.rank.value
				suit_offset = self.suit.value * 16
				unicode_char = chr(base_card + rank_offset + suit_offset)
			return "%s%s%s" % (self.color.getCode(), unicode_char, Style.RESET_ALL)


	def __repr__(self):
		return self.__str__()


	def card_compartor(card1, card2):
		c1SortValue = card1.rank.rank_sort_order()
		c2SortValue = card2.rank.rank_sort_order()
		if c1SortValue != c2SortValue:
			return c1SortValue - c2SortValue
		elif card1.suit is None:
			return card1.color.value - card2.color.value
		else:
			return card1.suit.value - card2.suit.value


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
