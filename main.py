# import necessary libraries
import argparse, sys, random
from math import e as E


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
       
       
      
      
      
      
         ''',r'''
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

LINE_SIZE = 64
def mainMenu():
    '''Outputs the main menu and returns the users choice of value'''
    print("-"*LINE_SIZE +"\nMAIN MENU\n" + "1. Play game\n2. View high Scores\n3. Quit\n" + "-" * LINE_SIZE)
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

def updateWord(chosenWord, maskedWord, guess, incorrectGuesses, score):
    # check whether guess is word
    if len(guess) != len(chosenWord):
        # check if guess is in the word
        if guess in chosenWord:
            # count all indices with guess 
            idxs = [i for i, v in enumerate(chosenWord) if v == guess]
            maskedWordList = list(maskedWord)
            for i in idxs:
                maskedWordList[i] = guess
                score += 5
            return "".join(maskedWordList), incorrectGuesses, score
        else:
            print("incorrect guess")
            incorrectGuesses += 1
            return maskedWord, incorrectGuesses, score
    else:
        if guess == chosenWord:
            return chosenWord, incorrectGuesses, score
        else:
            print("Incorrect Guess, score lost")
            incorrectGuesses += 1
            return maskedWord, incorrectGuesses, score

def playGame(wordbank):
    totalScore = 0
    tryAgain = True
    while tryAgain:
        # choose random number to select word from wordbank
        randomIndex = random.randint(0, len(wordbank))
        chosenWord = wordbank[randomIndex]
        incorrectGuesses, score = 0, 0
        
        priorGuesses = []
        maskedWord = obscureWord(chosenWord)
        while (maskedWord != chosenWord) and incorrectGuesses < 7:
            print("-"*LINE_SIZE)
            print(HANGMANPICS[incorrectGuesses])
            print("WORD TO GUESS:",  maskedWord)
            print(chosenWord)
            print("Past Guesses:", ", ".join(priorGuesses))
            print("-"*LINE_SIZE)
            guess = playerGuess(maskedWord, priorGuesses)
            maskedWord, incorrectGuesses, score = updateWord(chosenWord, maskedWord, guess, incorrectGuesses, score)

        
        if incorrectGuesses < 7:
            score += int(100 / (1 + E ** (0.2 * (len(priorGuesses) - 13))))
            print("YOU WIN!!!! want to try again?")
            print("Your current score is:", score)
            try:
                choice = input("(Y/y = yes, otherwise no)>> ")
            except KeyboardInterrupt:
                print("See you next time!")
            if choice.lower() == "y":
                tryAgain = True
            else:
                tryAgain = False
        else:
            print("YOU LOST!!!")
            print("Your current score is:", score)
            tryAgain = False
        
        totalScore += score
    return totalScore

def saveScore(score):
    '''Saves score to a results.txt file'''
    print("Congrats you got a new score! Enter your name to save it")
    try:
        username = input("Enter your name>> ")
    except KeyboardInterrupt:
        print("See you next time! Your score has not been saved")

    with open("results.txt", "a") as f:
        f.write(username + "," + str(score) + "\n")
    
    print("Result saved successfully!")
    main()


    


def main():
    choice = mainMenu()
    if choice == 1:
        # setup the wordBank
        wordbank = setupWordbank()
        # Start the game
        finalScore = playGame(wordbank)

        saveScore(finalScore)
    elif choice == 2:
        pass
    else:
        print("See you next time!")
        sys.exit(0)

# MAIN GAME LOOP
if __name__ == "__main__":
    main()