import os
import numpy as np

# get the hangman picture as a string given 
# the number of wrong guesses
def get_hangman_picture(num_wrong_guesses) :
    Stickmen = [
r'''
     _____
    |/    |
    |     O
    |    /|\ 
    |    / \
    |_______          

''', r'''
     _____
    |/    |
    |     O
    |    /|\ 
    |    / 
    |_______

''', r'''
     _____
    |/    |
    |     O
    |    /|\ 
    |    
    |_______

''', r'''
     _____
    |/    |
    |     O
    |    /| 
    |     
    |_______

''', r'''
     _____
    |/    |
    |     O
    |     | 
    |     
    |_______

''', r'''
     _____
    |/    |
    |     O
    |    
    |     
    |______

''', r'''
     _____
    |/    |
    |     
    |     
    |    
    |_______

''', r'''
     _____
    |/    
    |     
    |     
    |    
    |_______

''', r'''
     
    |/    
    |     
    |     
    |    
    |_______

''', r'''
     
    |
    |     
    |     
    |    
    |_______

''', r'''
     
    
         
         
        
     _______

''', r'''







''']
    stickmen_last_index = len(Stickmen) - 1
    if (num_wrong_guesses > stickmen_last_index) :
        return (None, None)
    num_guesses_left = stickmen_last_index - num_wrong_guesses
    stickmen_picture_str = Stickmen[ num_guesses_left ]
    return (stickmen_picture_str, num_guesses_left)

def clear_screen():
    if os.name == 'nt': # for windows
        os.system('cls')
    else: # for mac and linux
        os.system('clear')

# check if provided input is a letter
def is_letter(s) :
    return (len(s) == 1) and (s.lower() in "abcdefghijklmnopqrstuvwxyz")
                       
# get game difficulty level from the user   
def get_game_difficulty() :
    while True:
        clear_screen()
        print("Welcome to Hangman!\n\n")
        print("What game difficulty would you like to play?\n")
        print("1. Easy")
        print("2. Hard")
        print("3. Very Hard\n")

        #Game_difficulty = sys.stdin.read(1)
        game_difficulty = input("Please press 1, 2 or 3: ")
        if (len(game_difficulty) == 1 and game_difficulty in "123") : break
    return game_difficulty

def get_word_for_game(game_difficulty) :
    # read all available words
    words = open('words.txt')
    allWords = list(words)

    # determine word difficulty score per
    # word by combining word length
    # and whether infrequent letters are present
    wordDifficultyList = []
    for i in range(len(allWords)) :
        word = allWords[i].strip()
        wordDifficulty = len(word)
        # j,x,q,z are the least frequent letters in English
        # add 2 points to difficulty to the score if present
        wordDifficulty += ('j' in word) * 2
        wordDifficulty += ('x' in word) * 2
        wordDifficulty += ('q' in word) * 2
        wordDifficulty += ('z' in word) * 2
        # b,v,k are the next set of infrequent letters in English
        # add 1 point of difficulty to the score if present
        wordDifficulty += ('b' in word)
        wordDifficulty += ('v' in word)
        wordDifficulty += ('k' in word)
        # append word difficulty score to the list
        wordDifficultyList.append(wordDifficulty)
    
    wordDifficultyArray = np.array(wordDifficultyList)
    # calculate the 33d and 66th percentile for the 
    # difficulty scores:
    # 1. Percentile 0-33   = Easy
    # 2. Percentile 33-66  = Hard
    # 3. Percentile 66-100 = Very Hard
    easyDifficulty = np.percentile(wordDifficultyArray, 33)
    hardDifficulty = np.percentile(wordDifficultyArray, 66)

    # collect indices of words that fall into the
    # Easy, Hard or Very Hard category depending on user's choice
    wordIndexList = []
    for i in range(len(allWords)) :
        if (wordDifficultyArray[i] <= easyDifficulty) :
            if (game_difficulty == '1') : wordIndexList.append(i)
        elif (wordDifficultyArray[i] <= hardDifficulty) :
            if (game_difficulty == '2') : wordIndexList.append(i)
        elif (wordDifficultyArray[i] > hardDifficulty) :
            if (game_difficulty == '3') : wordIndexList.append(i)
    
    # chose a word based on a random choice of index of words with 
    # specified difficulty
    word_for_game = allWords[ np.random.choice(wordIndexList) ].strip()
    return word_for_game

# get a list of indices where a letter is present in the word
def get_indices_all_occurences(letter, word):
    return [index for index in range(len(word)) if word[index] == letter]

# let user make one guess at a letter
def one_guess(guess_str, msg, word, correct_guesses, wrong_guesses):    
    # start by clearing the screen
    clear_screen()
    # print correctly/incorrectly guessed letters and hangman picture
    print("Welcome to Hangman!\n\n")
    print('Correctly guessed letters : ' + ' '.join(correct_guesses))
    print('Incorrctly guessed letters: ' + ' '.join(wrong_guesses))
    print('\n')
    print(guess_str)
    print('\n')
    (hangman_picture, guesses_left) = get_hangman_picture(len(wrong_guesses))
    print(hangman_picture)
    print('\n')

    game_over = False
    if (not '_' in guess_str) :
        print("\nBob Survived :) Great Job! The word was '" + word + "'")
        print("You won! Please restart the program to try again.\n")
        game_over = True
    
    if (guesses_left == 0):
        print("\nBob Died :( The word was '" + word + "'")
        print("You lost! Please restart the program to try again.\n")
        game_over = True

    # if the game is already finished, return immediately
    if (game_over) :
        return (game_over, guess_str, '', word, correct_guesses, wrong_guesses)
    
    # print a message to the user (e.g. Guess was correct or incorrect)
    print(msg + '\n')

    # get a one guess letter input from the user
    letter = input("Please guess a letter in the word: ").lower()
    if (letter in wrong_guesses) or (letter in correct_guesses):
        return (game_over, guess_str, "Letter '" + letter + "' was alread guessed",
                word, correct_guesses, wrong_guesses)
    elif (not is_letter(letter)):
        return (game_over, guess_str, "Input '" + letter + "' is invalid",
                word, correct_guesses, wrong_guesses)
    elif (not letter in word):
        wrong_guesses.append(letter)
        msg = "Unfortunately '" + letter + "' is wrong. Please don't let Bob die!"
        return (game_over, guess_str, msg, word, correct_guesses, wrong_guesses)

    # guessed letter is correct
    correct_guesses.append(letter)    
    indices = get_indices_all_occurences(letter, word)
    guess_letter_list = guess_str.split(' ')
    for index in indices:
        guess_letter_list[index] = letter
    
    guess_str = ' ' . join(guess_letter_list)
    
    msg = "Letter '" + letter + "' is correct! Bob now has some hope!"
    return (game_over, guess_str, msg, word, correct_guesses, wrong_guesses)

def run_game() :
    word = get_word_for_game(get_game_difficulty()) 
    guess_str = '_ ' * len(word)
    correct_guesses = []
    wrong_guesses = []
    game_over = False
    msg = "Bob needs your help! Please save him by guessing the word!"
    
    while not game_over:
        # let the user guess one letter
        result = one_guess(guess_str, msg, word, 
                           correct_guesses, wrong_guesses)
        # update the values of the game related variables
        (game_over, guess_str, msg, word, 
         correct_guesses, wrong_guesses) = result

run_game()
