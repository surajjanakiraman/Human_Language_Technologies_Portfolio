import chapter8config as config
import os
import pickle
from nltk import word_tokenize
from nltk.util import ngrams
import chapter8config as config

# reads file and returns a list of lines
def readFile(fileName):
   # open the file and get rid of the newlines 
   # read line by line
   with open(os.path.join(config.cur_directory, fileName), 'r') as f:
      lines=[] # store the contents of the file in a list. 
      #read from the file.  
      while True: 
         line=f.readline()
         line=line.strip()
         lines.append(line)
         if not line:
            break
      return lines

# find the probability for this line for each language and return it
def compute_prob_line(line, unigram_dict, bigram_dict, v):
   p_laplace = 1  # calculate p using Laplace smoothing
   line_unigrams = word_tokenize(line)
   line_bigrams = list(ngrams(line_unigrams, 2))
   for bigram in line_bigrams:
      b = bigram_dict[bigram] if bigram in bigram_dict else 0 # bigram count
      u = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0 # unigram count of the first word in the bigram
      p_laplace = p_laplace * ((b + 1) / (u + v))
   
   return p_laplace

# find probability for each line for each language, and write the language with the highest probability to a file
def computeProb(test_text, 
                v,
                unigram_eng_dict, bigram_eng_dict,
                unigram_fr_dict, bigram_fr_dict,
                unigram_italian_dict, bigram_italian_dict, 
                ):
   f = open('languages.sol', 'w')
   lines = readFile(test_text)
   line_number = 1
   
   # for every line, find the probability for each language, and write the language with the highest probability to a file
   for line in lines:
      english_prob = compute_prob_line(line, unigram_eng_dict, bigram_eng_dict, v)
      french_prob  = compute_prob_line(line, unigram_fr_dict, bigram_fr_dict, v)
      italian_prob = compute_prob_line(line, unigram_italian_dict, bigram_italian_dict, v)
      max_prob = max(english_prob, french_prob, italian_prob)
      
      # write line number and the country with the highest probability to a file 
      f.write(str(line_number))
      if english_prob == max_prob:
         f.write(' English\n')
      elif french_prob == max_prob:
         f.write(' French\n')
      else:
         f.write(' Italian\n')
         
      line_number += 1

# compute accuracy of correctly classified instances in the test set
def find_accuracy():
   linesOutput = readFile('languages.sol')
   linesLangId = readFile('LangId.sol')
   totalLines = len(linesLangId)
   matches = 0    
   mismatch_lines_nbrs = []
   
   # go through the ouput file and test file, count matches, and save the lines where a mismatch occured
   for i in range(len(linesLangId)):
      if linesOutput[i] == linesLangId[i]:
         matches += 1
      else:
         mismatch_lines_nbrs.append(i + 1)
   
   return [matches / totalLines, mismatch_lines_nbrs] 
   
def main(english_text, french_text, italian_text, data_dir_path):
   # unpikle Egnlish unigram and bigram frequency dictionaries
   unigram_eng_dict = pickle.load(open(config.lang_eng_unigram_dict, 'rb'))
   bigram_eng_dict  = pickle.load(open(config.lang_eng_bigram_dict, 'rb'))

   # unpikle French unigram and bigram frequency dictionaries
   unigram_fr_dict = pickle.load(open(config.lang_french_unigram_dict, 'rb'))
   bigram_fr_dict  = pickle.load(open(config.lang_french_bigram_dict, 'rb'))
   
   # unpikle Italian unigram and bigram frequency dictionaries
   unigram_italian_dict = pickle.load(open(config.lang_italian_unigram_dict, 'rb'))
   bigram_italian_dict  = pickle.load(open(config.lang_italian_bigram_dict, 'rb'))

   # get the name of test_file from the config file
   test_file = config.test_file
      
   total_vocab_size = len(unigram_eng_dict) + len(unigram_fr_dict) + len(unigram_italian_dict)
       
   # for each line in the text file, calculate a probability for each language and write the language with the highest
   # probability to a file "languages.sol"
   computeProb(test_file,
               total_vocab_size,
               unigram_eng_dict, bigram_eng_dict,
               unigram_fr_dict, bigram_fr_dict,
               unigram_italian_dict, bigram_italian_dict
               )
   
   # output accuracy as the percentage of correctly classified instances in the test set and 
   # the line numbers of the incorrectly classified items
   accuracy = find_accuracy()[0]
   mismatch_lines_nbrs = find_accuracy()[1]
   accuracy*=100 # get the percentage. 
   print('\nAccuracy: ' + "{:.2f}".format(accuracy) + '%')
   print('Line numbers of the incorrectly classified items:', mismatch_lines_nbrs)