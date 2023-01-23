import random
import time
#Number Guessing Game Objectives:

# Include an ASCII art logo.
# Allow the player to submit a guess for a number between 1 and 100.
# Check user's guess against actual answer. Print "Too high." or "Too low." depending on the user's answer. 
# If they got the answer correct, show the actual answer to the player.
# Track the number of turns remaining.
# If they run out of turns, provide feedback to the player. 
# Include two different difficulty levels (e.g., 10 guesses in easy mode, only 5 guesses in hard mode).



attempts_count=False
thinked_number=random.randint(1,100)
game_over=False


while not attempts_count:
	print("Let's play a number gessing game!\nI'm thinking of a number between 1 and 100\n")
	mode=input("Select easy/normal/hard mode: ")
	if mode.lower()=="easy":
		attempts_count=10
	elif mode.lower()=="normal":
		attempts_count=7
	elif mode.lower()=="hard":
		attempts_count=5
	else:
		print("___________________________")
		print("Invalid input, Try again: ")



def start():
	global attempts_count
	global thinked_number
	global game_over
	
	if attempts_count:
		time.sleep(0.3)
		print(f"You have {attempts_count} attempts to guess the number.")
		guess=int(input("Make a guess: "))
		if guess > thinked_number:
			print("Too high.\nGuess again\n")
			attempts_count-=1
			start()
		elif guess < thinked_number:
			print("Too low.\nGuess again\n")
			attempts_count-=1
			start()
		elif guess==thinked_number:
			print(f"You guessed correct! The guessed number was: {guess}")
			game_over=True
	else:
		print("You've run out of attempts. You loose.")
		return
start()

