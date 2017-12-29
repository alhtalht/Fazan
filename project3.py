import sys
import select
import time
import random

score = 0
count = 0
difficulty = 30

def wordcheck(word, used):
    #Dictionary file already in computer.  Very useful!
    infile = open('/usr/share/dict/words', 'r')
    words = infile.readlines()
    infile.close()
    return word + '\n' in words and word not in used

def wordfind(letter):
    infile = open('/usr/share/dict/words', 'r')
    words = infile.readlines()
    infile.close()
    condition = False
    playable = False
    finalword = ""
    n = 0
    while condition == False and playable == False and n <= 1000000:
        n += 1
        myword = words[random.randint(0, len(words)-1)]
        if myword[-3:-1] == "'s":
            finalword = myword[:-3]
        else:
            finalword = myword[:-1]
        if finalword[0:2] == letter and len(finalword) >= 3 and finalword.find("'") == -1 and finalword[0] != finalword[0].upper():
            condition = True
        if condition == True:
            teststring = finalword[len(finalword)-2:len(finalword)]
            for word in words:
                if word[0:2] == teststring[0:2] and len(word[:-1]) >= 3:
                    playable = True
    if n < 1000000:
        return finalword
    else:
        return False
    

def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False

def alphabet(n):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return alphabet[n]

def start():
    n = 0
    print("")
    print("Start!")
    input("Press enter to end the random letter generation!")
    #Key Listener
    while heardEnter() == False:
        print(alphabet(n))
        n += 1
        if n == 26:
            n = 0
    print("Your letter is " + str(alphabet(n-1)).lower() + "!")
    return str(alphabet(n-1)).lower()

def instructions():
    print("This game is called Chained Words, or “Fazan” in Romanian. The computer will cycle through the alphabet. Then, the user presses enter to stop it. The user then must type a word that starts with the letter that the computer stopped on. The word has to be at least 3 letters long. In the game there are not allowed any proper nouns or prepositions and each word is to be used only once. The first 2 words after choosing a letter must not be dead-ends. A dead end word ends with two letters that doesn't correspond with another word.  An example of this would be the word BLUNT, because no word starts with NT. The first player says a word like HOUSE, and the computer will say a word that starts with the last two letters of the last word, like SENTENCE. The game continues like that until either the computer or the user can't continue the chain. The user has five lives, that spell out the word FAZAN.  Good luck!")
    input("Press enter to exit. ")

def settings():
    n = 0
    while n != 1 and n != 2 and n != 3:
        print("Input 1 for easy")
        print("Input 2 for medium")
        print("Input 3 for hard")
        n = int(input())
    return n

def game(letter):
    lose = False
    win = False
    n = 0
    y = 1
    initial = True
    used = []
    elapsed = 0
    m = 0
    global score #number of wins
    global count #number of losses
    while lose == False and win == False and elapsed < difficulty:
        start = time.time()
        n += 1
        userword = str(input("What is your word? ")).lower()
        #Time checker
        elapsed = time.time() - start
        if n != 1:
            letter = computerword[len(computerword)-2:len(computerword)]
            #Y is used for the index of a word and is only 1 for the initial condition.  Any other time it is two.
            y = 2
            intial = False
        if userword[0:y] == letter and wordcheck(userword, used) == True:
            used.append(userword)
            if wordfind(userword[len(userword)-2:len(userword)]) == False:
                win = True
                if n == 1:
                    print("You lose!")
                    lose = True
                    count += 1
                else:
                    print("You win!")
                    score += 1
                    win = True
            else:
                computerword = str(wordfind(userword[len(userword)-2:len(userword)]))
                if initial == True:
                    #Computer must find a word that is playable on for the initial case.
                    #M is used as a sort of timer for the computer.  If m gets over 25, there are DEFINITELY no words in the dictionary that will work.
                    m = 0
                    while (wordfind(computerword[len(computerword)-2:len(computerword)]) == False or wordcheck(computerword, used) == False) and m <= 25:
                        computerword = str(wordfind(userword[len(userword)-2:len(userword)]))
                        m += 1
                else:
                    m = 0
                    while wordcheck(computerword, used) == False and m <= 25:
                        computerword = str(wordfind(userword[len(userword)-2:len(userword)]))
                        m += 1
                if m >= 25:
                    #If the computer takes too long to find a word
                    win = True
                    score += 1
                    print("You win!")
                if elapsed < difficulty and m < 25:
                    print("The computer's word is " + computerword)
                    used.append(computerword)
        else:
            lose = True
            count += 1
            if wordcheck(userword, used) == False:
                print("You lose! Your word was either repeated or not a word!")
            elif userword[0:y] != letter:
                if y == 1:
                    print("You lose! You didn't start with the random letter!")
                else:
                    print("You lose! Your word didn't start with the first two letters of the last word!")
            else:
                print("You lose!")
    if elapsed >= difficulty:
        print("You lose!  Took too long!")

def main():
    n = 0
    global count
    global score
    global difficulty
    count = 0
    while n != 1 and n != 2 and n != 3 and n != 4:
        print("FAZAN!")
        print("Input 1 to start!")
        print("Input 2 for instructions")
        print("Input 3 for settings")
        print("Input 4 to exit")
        n = int(input())
        if n == 1:
            while count < 5:
                letter = start()
                if difficulty == 1000:
                    difficulty = 30
                game(letter)
                if count == 0:
                    print("Letters:")
                elif count == 1:
                    print("Letters: F")
                elif count == 2:
                    print("Letters: FA")
                elif count == 3:
                    print("Letters: FAZ")
                elif count == 4:
                    print("Letters: FAZA")
                elif count == 5:
                    print("Letters: FAZAN")
                    print("Score: " + str(score))
        elif n == 2:
            instructions()
            main()
        elif n == 3:
            difficulty = int(settings())
            if difficulty == 1:
                difficulty = 30
            elif difficulty == 2:
                difficulty = 20
            elif difficulty == 3:
                difficulty = 10
            main()

main()
