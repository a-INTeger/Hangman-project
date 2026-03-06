# import necessary libraries
import argparse, sys, random


# setup parser for passing terminal parameters
parser = argparse.ArgumentParser(
    prog = "Hangman",
    description="A small game of hangman"
)
parser.add_argument("-f", "--file", help="File containing wordbank, by default will use the provided WORDBANK.txt")
args = parser.parse_args()

# define the default file for whenever no file argument is provided
DEFAULT_FILE = "google-10000-english-no-swears.txt"

HANGMANPICS = [r'''
  +---+
  |   |
      |
      |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']


def mainMenu():
    '''Outputs the main menu and returns the users choice of value'''
    print("-"*32 +"\nMAIN MENU\n" + "1. Play game\n2. View high Scores\n3. Quit\n" + "-" * 32)
    flag = False
    # validate whether the choice is numeric
    while not flag:
        # try to catch a keyboard interrupt to exit gracefully
        try:
            choice = input("What would you like to do?\n>> ")
        except KeyboardInterrupt:
            print("\nSee you next time!")
            sys.exit(0)
        
        # catch any non number errors 
        try:
            choice = int(choice)
        except:
            print("\nThat was not a number!\nPlease try again.\n")
            continue
        # check if any values are outside the expected options
        if 0 < choice < 4:
            flag = True
        else:
            print("\nPlease pick either option 1 or 2\nPlease try again.\n")

    return choice


def setupWordbank():
    '''Imports word bank from the file specified'''
    try:
        # check whether the file was specified....
        if args.file:
            with open(str(args.file), "r") as f:
                words = f.readlines()
                # strip newlines off the words
                words = list(map(lambda x: x.strip(), words))
                # filter out words are less than 5 characters long
                words = [word for word in words if len(word) > 4]
        else:
            # ... if not then choose the default file
            with open(DEFAULT_FILE, "r") as f:
                words = f.readlines()
                # strip newlines off the words
                words = list(map(lambda x: x.strip(), words))
                # filter out words are less than 5 characters long
                words = [word for word in words if len(word) > 4]

        return words
    # catch if the file defined does not exist
    except FileNotFoundError as e:
        print(f"ERROR: THE FILE {args.file} YOU SPECIFIED DOES NOT EXIST")
        sys.exit(-1)


def obscureWord(word):
    return "*" * len(word)

def playerGuess(word, priorGuess):
    flag = False
    while not flag:
        try:
            guess = input("What is your guess? (Single letter or full word)\n>> ")
        except KeyboardInterrupt:
            print("\nSee you next time!")
            sys.exit(0)

        # check whether the guess only contains characters
        if not guess.isalpha():
            print("\nThat was not a letter or a word!\nPlease try again.\n")
        elif len(guess) != 1 and len(guess) != len(word):
            print("\nThat was not a single letter nor a word guess\nPlease try again.\n")
        elif guess in priorGuess:
            print("\nYou've already guessed that letter/word!\nPlease try again.\n")
        else:
            flag = True
    
    priorGuess.append(guess)
    return guess

def updateWord(chosenWord, maskedWord, guess):
    # check whether guess is word
    if len(guess) != len(chosenWord):
        # check if guess is in the word
        if guess in chosenWord:
            # count all indices with guess 
            idxs = [i for i, v in enumerate(chosenWord) if v == guess]
            maskedWordList = list(maskedWord)
            for i in idxs:
                maskedWordList[i] = guess
            return "".join(maskedWordList)
        else:
            print("incorrect guess")
    else:
        if guess == chosenWord:
            print("YOU WIN!!!!")
            maskedWord = chosenWord
        else:
            print("Incorrect Guess, score lost")
    return maskedWord


def playGame(wordbank):
    # choose random number to select word from wordbank
    randomIndex = random.randint(0, len(wordbank))
    chosenWord = wordbank[randomIndex]
    
    priorGuesses = []
    maskedWord = obscureWord(chosenWord)
    while (maskedWord != chosenWord):
        print(chosenWord + "\n" + maskedWord)
        guess = playerGuess(maskedWord, priorGuesses)
        maskedWord = updateWord(chosenWord, maskedWord, guess)


# MAIN GAME LOOP
if __name__ == "__main__":
    choice = mainMenu()
    if choice == 1:
        # setup the wordBank
        wordbank = setupWordbank()
        # Start the game
        playGame(wordbank)
    elif choice == 2:
        pass
    else:
        print("See you next time!")
        sys.exit(0)
