#!/usr/bin/env python3

from enum import Enum
from functools import cmp_to_key
import random
import re

from deck import Deck, Rank, Suit, Card

class Numeral(Enum):
	SINGLES = 1
	DOUBLES = 2
	TRIPLES = 3

class Trick:
	def __init__(self, numeral, initial):
		self.numeral = numeral
		self.cards = []
		for card in initial:
			self.cards.append(card)


class Simulator:

	def __init__(self, options = {}):
		self.deck = Deck()
		self.num_players = 6
		hands = []
		for i in range(self.num_players):
			hands.append([])
		random.shuffle(self.deck.cards)
		for i in range(52):
			hands[i % 6].append(self.deck.cards[i])
		self.players = []
		for i in range(self.num_players):
			self.players.append(Player(hands[i]))
		self.curent_player_idx = 0
		for player in self.players:
			if player.can_start():
				break
			self.curent_player_idx += 1
		
		print("Current player: %d" % ((self.curent_player_idx % self.num_players) + 1))
		self.current_trick = self.players[self.curent_player_idx].begin_trick()
		self.tricks = []
		self.curent_player_idx += 1
		self.play_trick()


	def play_trick(self):
		last_play = 0
		while True:
			print("Current player: %d" % ((self.curent_player_idx % self.num_players) + 1))
			cards = self.players[self.curent_player_idx % self.num_players].play()
			if not cards is None:
				if cards[0].rank == Rank.TWO:
					break
				last_play = 0
				if self.current_trick.numeral == Numeral.SINGLES:
					if cards[0].rank == self.current_trick.cards[-1].rank:
						print("Skipping the next player")
						self.curent_player_idx += 1
				self.current_trick.cards += cards
			else:
				last_play += 1
				if last_play == self.num_players - 1:
					break
			self.curent_player_idx += 1
		self.tricks.append(self.current_trick)
		

		

class Player:

	play_re = re.compile("(\d+,)*\d+")

	def __init__(self, hand):
		self.index = {}
		for card in hand:
			if card.rank in self.index:
				self.index[card.rank].append(card)
			else:
				self.index[card.rank] = [card]


	def complete(self):
		play = raw_input("Complete y/n?")
		if play == "y":
			return True
		else:
			return False



	def play(self):
		self.print_hand()
		sorted_hand = self.get_sorted_hand()

		play_as_text = input("What cards would you like to play? enter a newline if you wish to skip\n>")
		while True:
			if Player.play_re.match(play_as_text):
				card_indices = play_as_text.split(",")
				break
			elif play_as_text == "":
				return None
			else:
				print("Play invalid, please enter a comma-separated list of cards, no spaces")
		cards_to_play = []
		for idx in range(len(card_indices) - 1, -1, -1):
			card = sorted_hand[int(card_indices[idx]) - 1]
			cards_to_play.append(card)
			self.index[card.rank].remove(card)
		return cards_to_play

	def can_start(self):
		if Rank.THREE in self.index:
			for three in self.index[Rank.THREE]:
				if three.suit == Suit.CLUBS:
					return True
		return False


	def begin_trick(self):
		cards = self.play()
		if len(cards) == 1:
			return Trick(Numeral.SINGLES, cards)
		elif len(cards) == 2:
			return Trick(Numeral.DOUBLES, cards)
		elif len(cards) == 3:
			return Trick(Numeral.TRIPLES, cards)


	def get_sorted_hand(self):
		singles = []
		doubles = []
		triples = []
		quads = []
		for rank in self.index:
			amt = len(self.index[rank])
			for card in self.index[rank]:
				if amt == 1 or rank == Rank.TWO or rank == Rank.JOKER:
					singles.append(card)
				elif amt == 2:
					doubles.append(card)
				elif amt == 3:
					triples.append(card)
				elif amt == 4:
					quads.append(card)
		sorted_singles = sorted(singles, key=cmp_to_key(Card.card_compartor))
		sorted_doubles = sorted(doubles, key=cmp_to_key(Card.card_compartor))
		sorted_triples = sorted(triples, key=cmp_to_key(Card.card_compartor))
		sorted_quads = sorted(quads, key=cmp_to_key(Card.card_compartor))
		sorted_hand = sorted_singles + sorted_doubles + sorted_triples + sorted_quads
		return sorted_hand


	def print_hand(self):
		sorted_hand = self.get_sorted_hand()
		for i in range(len(sorted_hand)):
			print("%d: %s" % (i + 1, sorted_hand[i]))

if __name__ == "__main__":
	simulator = Simulator()
