# Dmitrii Obideiko
# Suraj Janakiraman 

import sys
import chapter8config as config
import os
import pickle
from nltk import word_tokenize
from nltk.util import ngrams
import program2 as pg2

# read the file, remove new lines, combine all lines into text and return it
def read_file(fileName):
    # open the file and get rid of the newlines 
     with open(os.path.join(config.cur_directory, fileName), 'r') as f:
        lines = []
        # read from the file line by line until there's no line  
        while True: 
            line = f.readline()
            line = line.strip() # remove leading and trailing characters
            lines.append(line)
            if not line:
             break
        # join all lines into one string
        text = ''.join(lines)
        return text

# return dictionaries for unigrams and biagrams where key is ngram and value is count
def lang_model(x):
    unigrams = word_tokenize(x)
    bigrams = list(ngrams(unigrams, 2))
    # counts the frequency of each unigram and saves it as a value in a dictionary where the key is a unigram
    unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}
    # counts the frequency of each bigram and saves it as a value in a dictionary where the key is a bigram
    bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}
    return unigram_dict,bigram_dict
   
def main(data_dir_path):
    # store the names of the files from the config file 
    english_file  = config.lang_eng
    french_file   = config.lang_french
    italian_file  = config.lang_italian
    
    # read files and store their content
    english_text = read_file(english_file)
    french_text  = read_file(french_file)
    italian_text = read_file(italian_file)
    
    # store unigram and bigram frequency dictionaries for every language
    eng_unigram_dict, eng_bigram_dict         = lang_model(english_text)
    fr_unigram_dict, fr_bigram_dict           = lang_model(french_text)
    italian_unigram_dict, italian_bigram_dict = lang_model(italian_text)
    
    # pickle English unigram and bigram frequency dictionaries
    eng_unigram_pickle = pickle.dump(eng_unigram_dict,open(os.path.join(data_dir_path, config.lang_eng_unigram_dict), 'wb'))
    eng_bigram_pickle  = pickle.dump(eng_bigram_dict,open(os.path.join(data_dir_path, config.lang_eng_bigram_dict), 'wb'))
    
    # pickle French unigram and bigram frequency dictionaries
    fr_unigram_pickle = pickle.dump(fr_unigram_dict,open(os.path.join(data_dir_path, config.lang_french_unigram_dict), 'wb'))
    fr_bigram_pickle = pickle.dump(fr_bigram_dict,open(os.path.join(data_dir_path, config.lang_french_bigram_dict), 'wb'))
    
    # pickle Italian unigram and bigram frequency dictionaries
    italian_unigram_pickle = pickle.dump(italian_unigram_dict,open(os.path.join(data_dir_path, config.lang_italian_unigram_dict), 'wb'))
    italian_bigram_pickle = pickle.dump(italian_bigram_dict,open(os.path.join(data_dir_path, config.lang_italian_bigram_dict), 'wb'))
        
    # call program 2
    pg2.main(english_text, french_text, italian_text, data_dir_path)
    
# take in 2 arguments for running purposes
if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('Please enter a filename as a system argument')
        sys.exit(1)
    data_dir_path = sys.argv[1]
    # save the current directory to get access to any file within the current directory
    config.cur_directory = data_dir_path
    main(data_dir_path)