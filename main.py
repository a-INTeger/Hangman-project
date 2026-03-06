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

# ALL DEFAULT VALUES GO HERE
# define the default file for whenever no file argument is provided
DEFAULT_FILE = "WORDBANK.txt"

# Hangman ASCII art
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

# Line size for sperating barriers
LINE_SIZE = 64
def mainMenu():
    '''Outputs the main menu and returns the users choice of value'''
    print("-"*LINE_SIZE +"\nMAIN MENU\n" + "1. Play game\n2. View high Scores\n3. Quit\n" + "-" * LINE_SIZE)
    flag = False
    # validate whether the choice is numeric
    while not flag:
        # try to catch a keyboard interrupt to exit gracefully
        try:
            choice = input("What would you like to do? (Input number corresponding to main menu)\n>> ")
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
    '''Obscures a word with asterisks'''
    return "*" * len(word)

def playerGuess(word, priorGuess):
    '''Handles player guess inputs'''

    # flag for input validation
    flag = False
    while not flag:
        # catch keyboard interrupts if they occur mid-input
        try:
            guess = input("What is your guess? (Single letter or full word)\n>> ")
        except KeyboardInterrupt:
            print("\nSee you next time!")
            sys.exit(0)

        # check whether the guess only contains characters
        if not guess.isalpha():
            print("\nThat was not a letter or a word!\nPlease try again.\n")
        # check whether guess is not a letter or a word guess
        elif len(guess) != 1 and len(guess) != len(word):
            print("\nThat was not a single letter nor a word guess\nPlease try again.\n")
        # check if the guess has already been guessed
        elif guess in priorGuess:
            print("\nYou've already guessed that letter/word!\nPlease try again.\n")
        else:
            # trip flag and progress
            flag = True
    
    # add to prior guesses
    priorGuess.append(guess)
    return guess

def updateWord(chosenWord, maskedWord, guess, incorrectGuesses, score):
    '''Updates a given word when a guess has been made and returns the new masked word and score'''

    # check whether guess is word
    if len(guess) != len(chosenWord):
        # check if guess is in the word
        if guess in chosenWord:
            # count all indices with guess 
            idxs = [i for i, v in enumerate(chosenWord) if v == guess]
            maskedWordList = list(maskedWord)
            #  updates the masked word
            for i in idxs:
                maskedWordList[i] = guess
                # add our 5 points per letter occurance correct
                score += 5
            return "".join(maskedWordList), incorrectGuesses, score
        else:
            # incorrect guess add to incorrect guesses
            print("Sorry", guess, "is not part of the word")
            incorrectGuesses += 1
            return maskedWord, incorrectGuesses, score
    else:
        # correct word guess
        if guess == chosenWord:
            # complete the whole thing
            return chosenWord, incorrectGuesses, score
        else:
            # incorrect full word guess
            print("Sorry", guess, "is not the word")
            incorrectGuesses += 1
            return maskedWord, incorrectGuesses, score

def playGame(wordbank):
    '''Core game loop function'''
    # track total score
    score = 0
    
    # try again flag to keep replaying
    tryAgain = True

    while tryAgain:
        # choose random number to select word from wordbank
        randomIndex = random.randint(0, len(wordbank) - 1)
        chosenWord = wordbank[randomIndex]
        incorrectGuesses =  0
        
        # setup game displays
        priorGuesses = []
        maskedWord = obscureWord(chosenWord)
        # failure conditions for guess loop
        while (maskedWord != chosenWord) and incorrectGuesses < 7:
            # print the current game stat for the user
            print("-"*LINE_SIZE)
            print(HANGMANPICS[incorrectGuesses])
            print("WORD TO GUESS:",  maskedWord)
            print("Past Guesses:", ", ".join(priorGuesses))
            print("-"*LINE_SIZE)
            guess = playerGuess(maskedWord, priorGuesses)
            maskedWord, incorrectGuesses, score = updateWord(chosenWord, maskedWord, guess, incorrectGuesses, score)

        # once out of the core game loop
        if incorrectGuesses < 7:
            # add bonus score for getting the word correct
            score += int(100 / (1 + E ** (0.2 * (len(priorGuesses) - 13))))

            # allow the user to try again for more score
            print()
            print("You got the word right! The word was:", chosenWord)
            print("Your current score is:", score)
            print("Want to keep going for more score?")
            print()

            try:
                choice = input("(Y/y = yes, otherwise no)>> ")
            except KeyboardInterrupt:
                print("See you next time!")
            
            # set the try again flag to restart game
            if choice.lower() == "y":
                tryAgain = True
            else:
                tryAgain = False
        else:
            # player lost forcefully terminate main game loop
            print()
            print("Sorry you got too many guesses wrong and your run has ended")
            print("The word was", chosenWord)
            print("Your final score is:", score)
            print()
            tryAgain = False
        
    return score

def saveScore(score):
    '''Saves score to a results.txt file'''
    # allow user to give their name to save it in the txt file
    print()
    print("Congrats you got a new score! Enter your name to save it")
    try:
        username = input("Enter your name>> ")
    except KeyboardInterrupt:
        print("See you next time! Your score has not been saved")
    print()
    # write to the results file (will create the file if it doesn't exist)
    if args.file:
        with open(f"results-{args.file}.txt", "a") as f:
            f.write(username + "," + str(score) + "\n")
    else:
        with open("results.txt", "a") as f:
            f.write(username + "," + str(score) + "\n")
    
    # let the user know that it has been saved successfully
    print("Result saved successfully!")
    print()

def printScores():
    '''Displays the top 3 scores to the user'''
    # temp data var for later output
    data = []

    # ensure that the file we are trying to read exists
    try:
        if args.file:
            with open(f"results-{args.file}.txt", "r") as f:
                data = f.readlines()
        else:
            with open("results.txt", "r") as f:
                data = f.readlines()
    except:
        # tell the user that the file doesnt exist if they try to run this before saving any scores
        print("-" * LINE_SIZE + "\n\nNO RESULTS FILE DETECTED\n\n" + "-" * LINE_SIZE)

    # check if we have no data either no file or no data lines
    if len(data) > 0:
        # preprocess the data, each line needs characters stripped and then split by comma
        properScores = [line.strip().split(",") for line in data]
        # then our score part needs to be casted to int
        properScores = list(map(lambda x: [x[0], int(x[1])], properScores))
        # sort the values in descending order
        properScores.sort(key=lambda x: x[1], reverse=True)
        # print out the top 3 results or fewer whichever is less
        print()
        print("-"*LINE_SIZE)
        for i in range(3 if len(data) >= 3 else len(data)):
            print(f"{i+1}. {properScores[i][0]:<20} Score: {properScores[i][1]:>4}")
        print("-"*LINE_SIZE)
        print()
    else:
        # let the user know there are no scores detected
        print("-" * LINE_SIZE + "\n\nNO SCORES DETECTED\n\n" + "-" * LINE_SIZE)

def main():
    '''Entry point for the entire hangman game'''
    choice = mainMenu()
    # keep looping if we dont want to quit
    while choice != 3:
        if choice == 1:
            # setup the wordBank
            wordbank = setupWordbank()
            # Start the game
            finalScore = playGame(wordbank)
            # allow the user to save the score
            saveScore(finalScore)
        elif choice == 2:
            printScores()
        
        choice = mainMenu()
    else:
        # print clean exit message
        print("See you next time!")
        sys.exit(0)

# run only main() on python execution
if __name__ == "__main__":
    main()