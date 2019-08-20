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
it_max = 10**4
converges = 10**-4
fail_flag = True #convert to false if guess is wrong
suit = list(range(2, 11)) #the cards that are played with, to be shuffled later
i = 0 #iteration counter
c = 1 #convergance counter
# code to test deck randomizer:
	# cards = random.sample(suit, len(suit))
	# for card in range(9):
	# 	print("card = %s" %card)
	# 	print("cards[card] = %s" %cards[card])
while i < it_max and c > converges and fail_flag == true:
	cards = random.sample(suit, len(suit)) #shuffles cards
	expectation_value = mean(cards) #guess high if card < mean, low if card > mean
	drawn_cards = [] #list to hold drawn cards
	for card in range(9):
		if cards[card] > expectation_value and cards[card+1] < cards[card]: #if the current card is above the mean, and the next is below this one a correct guess
			fail_flag = true #we didn't lose
			drawn_cards.add(cards[card]) #puts the card into the drawn deck
			cards.remove(cards[card]) #take the card out of the deck
			print("%s | %s" %(drawn_cards, cards))
		elif cards[card] > expectation_value and cards[card+1] > cards[card]: #if the current card is above the mean, and the next is above this one, an incorrect guess
			#exit for loop, update win rate, record number cards revealed
			fail_flag = false #we guessed wrong
		if cards[card] < expectation_value and cards[card+1] > cards[card]: #if the current card is below the mean, and the next is above this one a correct guess
			fail_flag = true #we didn't lose
			cards.remove(cards[card]) #take the card out of the deck
		elif cards[card] < expectation_value and cards[card+1] < cards[card]: #if the current card is below the mean, and the next is below this one, an incorrect guess
			#exit for loop, update win rate, record number cards revealed
			fail_flag = false #we guessed wrong
	i += 1