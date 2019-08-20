# Riddler Express:
	# From Freddie Simmons, a guessing game:
	# Take a standard deck of cards, and pull out the numbered cards from one suit (the cards 2 through 10). Shuffle them, and then lay them face down in a row. Flip over the first card. Now guess whether the next card in the row is bigger or smaller. If you’re right, keep going.
	# If you play this game optimally, what’s the probability that you can get to the end without making any mistakes?
	# Extra credit: What if there were more cards — 2 through 20, or 2 through 100? How do your chances of getting to the end change?
	# pseudocode:
	# make list 2 thru 10
	# randomize list
	# define expectation_value as mean(cards)
	# if card > expectation_value, guess cards[n+1] is less
	# else guess higher
	# if correct, repeat loop
	# if incorrect record as loss, update win rate
	# repeat 10k times or until win rate converges
import random
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
it_max = 10**5
converges = 10**-4
fail_flag = True #convert to false if guess is wrong
suit = list(range(2, 11)) #the cards that are played with, to be shuffled later
i = 0 #iteration counter
c = 1 #convergance counter
win_tally = [] #update with 0 for a loss and 1 for a win
win_rate = 2 #pick ranom int to make convergence check work
game_length_tally = [] #stores the flipped deck after a succesful game 
# code to test deck randomizer:
	# cards = random.sample(suit, len(suit))
	# for card in range(9):
	# 	print("card = %s" %card)
	# 	print("cards[card] = %s" %cards[card])
# while i <= it_max and c > converges:
while i <= it_max:
	print("beginning game number %s" %i)
	cards = random.sample(suit, len(suit)) #shuffles cards
	expectation_value = sum(cards)/len(cards) #guess high if card < mean, low if card > mean
	drawn_cards = [] #list to hold drawn cards
	print("%s | %s" %(drawn_cards, cards))
	#while len(cards) > 0 and fail_flag == True:
		# fail_flag = True
	while len(cards) > 1:
		expectation_value = sum(cards)/len(cards) #guess high if card < mean, low if card > mean
		if cards[0] < expectation_value: #guess high
			high = 1
		elif cards[0] > expectation_value: #guess low
			high = 0
		else: #flip a coin
			coin = random.randint(1, 2)
			if coin == 1:
				high = 1
			else:
				high = 0
		print("step: %s, card: %s, guess: %s, next card: %s," %(len(drawn_cards), cards[0], expectation_value, cards[1]))
		if high == 1: #guesing next card is higher 
			print("guessing high")
			if cards[0] < cards[1]: #succesful guess high
				print("correctly guessed next card to be higher!")
				drawn_cards.append(cards[0])
				cards.pop(0)
			else: #unsuccesful guess high
				print("incorrectly guessed next card to be higher, GAME OVER!")
				win_tally.append(0)
				break
				#fail_flag = False
				#game over, break for loop
		else: #guessing next card is lower 
			print("guessing low")
			if cards[0] > cards[1]: #succesful guess low
				print("correctly guessed next card to be lower!")
				drawn_cards.append(cards[0])
				cards.pop(0)
			else: #unsuccseful gyess low
				print("incorrectly guessed next card to be lower, GAME OVER!")
				win_tally.append(0)
				break
		win_rate_prev = win_rate
		if len(cards) == 1: #update tallies if end of deck is reached
			print("epic!")
			drawn_cards.append(cards[0])
			game_length_tally.append(len(drawn_cards))
			win_tally.append(1)
			win_rate = sum(win_tally) / len(win_tally)
			# c = abs(win_rate - win_rate_prev)
			# print("convergence is at %s" %c)
		print("%s | %s" %(drawn_cards, cards))
	i += 1
print(win_rate)
num_bins = 10
n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
plt.show()