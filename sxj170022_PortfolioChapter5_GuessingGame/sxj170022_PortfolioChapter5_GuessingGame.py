
#Name: Suraj Janakiraman
#Date: 09-25-2022
# Subject: CS 4395.001 Human Language Technologies
# Instructor: Dr. Karen Mazidi

#Description: The purpose of the python project is to create a guessing game from
# a text file. The Python Program reads in the text file anat19.txt, stores the contents of the file in a list,
# processes each token of the file, lemmatizes the tokens to create unique lemmas, gathers all the nouns,
# stores the nouns in the dictionary, and creates a guessing game based upon the 50 most common nouns in the dictionary.

#How to run: Donwload the files on eLearning PortfolioChapter5_GuessingGame_config.py,
#sxj170022_PortfolioChapter5_GuessingGame.py, as well as the data folder containing anat19.txt
# make sure to input the following command when running:
# python sxj170022_PortfolioChapter5_GuessingGame.py data/anat19.txt
# This is a sample Python script.
from nltk import word_tokenize, pos_tag

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import PortfolioChapter5_GuessingGame_config as config
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import sys
from random import seed
from random import randint

#preprocess the file further
# open the file and store the contents of the anat19.txt into a list
#make sure that everything is in lower case.
def preprocess_file(data_dir_path):
    #create a data structure to store the contents of the file, maybe a list
    list=[]
    f=open(config.anatomy_txt,'r')
    while True:
        line=f.readline()
        text = re.sub(r'[.?!,:;()\-\n\d]',' ',line.lower())
        list.append(text)
        if not line:
            break;
   # print(list)
    str=''.join(list)
    tokens=word_tokenize(str)
    set_text=set(tokens)
    #lexical diversity
    print("\nLexical diversity: %.2f" % (len(set_text)/len(tokens)))
    return tokens;


#function to preprocess the tokens  after preprocessing the file.
# This is step 2 in preprocessing the words in the file after lower casing all the letters
def preprocess_tokens_and_nouns(data_dir_path):
   tokens=preprocess_file(data_dir_path)
   #lemmatize the tokens
   wnl=WordNetLemmatizer()
   lemmas=[wnl.lemmatize(t) for t in tokens]
   #make the lemmas unique
   lemmas_unique=list(set(lemmas))
   #print the 1st 20 tags that you see.
   first_20_tags=nltk.pos_tag(lemmas_unique[:20])
   print(first_20_tags)
   #new list of nouns
   tags=nltk.pos_tag(lemmas_unique)
   nouns=[pos_tag[0] for pos_tag in tags if (pos_tag[1].startswith('N'))]
   print("# of tokens=",len(tokens), "# of nouns= ",len(nouns))
   return tokens,nouns

#make a dictionary consisting of nouns
#return the top 50 nouns
def dictionary_of_nouns(numberofnouns):
    tokens,nouns=preprocess_tokens_and_nouns(data_dir_path)
    noun_dict={n:tokens.count(n) for n in nouns}
    #use a list comprehension
    sorted_dict=sorted(noun_dict.items(), key=lambda x:x[1], reverse=True)
    #print(sorted_dict)
    if(len(sorted_dict)>numberofnouns):
            sorted_dict=sorted_dict[:numberofnouns]
            top50nouns=[t[0] for t in sorted_dict]
    return top50nouns

#prints out the word for the guessing game
def print_word(guess,letters_guessed):
    for i in guess:
        print('_' if (i not in letters_guessed) else i, ' ', end='')
        print()

#begin the guessing game with the top 50 most common nouns.
# treat the guessing game like hangman in which the user guesses one letter at a time
#reduce the score by 1 if the user gets the wrong letter
#increase the score by 1 if the user gets the right letter.
#do not change the score if the users guesses the same letter more than once.
def guessing_game(top50,total_count_nouns):
    score=5
    exit=False
    while(not exit):
        i=randint(0,total_count_nouns-1)
        guess=top50[i]
        letters_guessed=[] #create a new list to store all letters of word guessed.
        print("Let's play a word guessing game!")
        while (True):
            #print guess with letters masked except those letters_guessed
            print_word(guess,letters_guessed)
            letter_guessed=input("Guess a letter: ")
            if(letter_guessed=='!'):
                exit=True;
                break;
            if(letter_guessed in letters_guessed):
                pass
            elif(letter_guessed not in guess):
                score-=1; # subtract 1 from the score
                print('Sorry, guess again. Score is ',score)
                if (score <0):
                    exit=True
                    break;
            else:
                score+=1; # add 1 to the score
                print('Right! Score is ',score)
                letters_guessed.append(letter_guessed)
                #check if all letters are guessed
                guessed=True
                for i in guess:
                    if (i not in letters_guessed):
                        guessed=False
                        break
                if (guessed):
                    print_word(guess,letters_guessed)
                    print('You solved it ')
                    break;

#the main function
def main(data_dir_path):
    top50=dictionary_of_nouns(50)
    print(top50)
    seed(1234)
    guessing_game(top50,50)

# Press the green button in the gutter to run the script.
#provide system arguments so that the user can run the code from the command line
if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("usage: %s <relative path to data/anatomy.txt" % sys.argv[0])
        sys.exit(1)
    data_dir_path = sys.argv[1]
    main(data_dir_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
