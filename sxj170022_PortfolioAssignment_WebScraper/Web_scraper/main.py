from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import re
import config_webscraping as config
import requests
from nltk import word_tokenize
from nltk.corpus import stopwords

# check whether the html element is visible or not
def visible(element):
    if (element.parent.name in ['style','script','[document]','head','title'] or
        re.match('<!--.*-->',str(element.encode('utf-8')))):
        return False
    return True


# deletes new lines & unneeded spaces from the text 
def clean_up_file(text):
    lines = text.split('\n')
    # remove spaces at the beginning and at the end of each line
    lines = [line.strip() for line in lines]
    # get rid of lines that are empty
    lines = [line for line in lines if len(line) > 0]
    # join all lines into one big text
    text = '\n'.join(lines)
    return text

# read a file filled with uril links
# put the text of each website into a file 
def read_file(fileName):
    texts = []
    # read the urls.txt file
    with open(fileName, 'r') as f:
        # take the contents of the file, split the lines, and save them in a list
        urls = f.read().splitlines()
    # grab text from every html file and put it into a file
    i = 1 # index of the url
    for u in urls:
        html = requests.get(u).text.encode("utf-8")
        soupObj = BeautifulSoup(html, features = "html.parser")
        # finds all text data
        data = soupObj.findAll(text = True)
        # returns an iterator which is then converted into a list
        result = filter(visible, data)
        text_lines = list(result)
        # join all lines into one text
        text = ' '.join(text_lines)
        text = clean_up_file(text)
        texts.append(text)
        createfile(text, i)
        i += 1
    return texts

# create a txt file where the name is the number of the file (i)
def createfile(text, i):
    with open('files/' + str(i) + '.txt','w', encoding = "utf-8") as f:
        f.write(text)

# creates a search dict for 1 webstie only 
def build_searchable_knowledge_base(texts):
    searchDict = defaultdict(set)
    for text in texts:
        # break the text into lines
        lines = text.split('\n')
        for line in lines:
            # break the line into words   
            words = word_tokenize(line.lower())
            for word in words:
                searchDict[word].add(line)
        
    return searchDict

# returns top n frequent token from text
def extract_most_freq_terms(texts, n):
    texts = ' '.join(texts)    
    tokens = word_tokenize(texts.lower())
    # removes all tokens whose length is <= 2
    tokens = [token for token in tokens if len(token) > 2]
    # remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [w for w in tokens if w not in stop_words]
    # create a frequency dictionary where the key is a word and the value if the frequency 
    freqDict = {token : texts.count(token) for token in set(filtered_tokens)}
    # sort the frequency dictionary in ascending order and return n most frequent words 
    sortedFreqDict = sorted(freqDict.items(), key = lambda x: x[1], reverse=True)
    return [el[0] for el in sortedFreqDict[:n]]

def main():
    # send a get request to starer_url
    respObj = requests.get(config.starter_url)
    page_content = respObj.text
    soup = BeautifulSoup(page_content)

    # write urls to a file
    with open('urls.txt', 'w') as f:
        # find all html elements with <a> tags and go through every element
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            # if it's a valid link, write it to the file
            if link_str.startswith('http') and 'google' not in link_str: # why do we check if the word google is't in the link???????
                f.write(link_str + '\n')
    
    # create text files f        
    texts = read_file('urls.txt')
    print('\n\n\n',extract_most_freq_terms(texts, 40))
    searchDict = build_searchable_knowledge_base(texts)
    
    # creates a file where knowledge base is used on 10 chosen words
    with open('knowledge_base.txt', 'w') as f:
        f.write('form - ' + ' '.join(searchDict['form']) + '\n\n')
        f.write('act - ' + ' '.join(searchDict['act']) + '\n\n')
        f.write('work - ' + ' '.join(searchDict['work']) + '\n\n')
        f.write('sign - ' + ' '.join(searchDict['sign']) + '\n\n')
        f.write('app - ' + ' '.join(searchDict['app']) + '\n\n')
        f.write('age - ' + ' '.join(searchDict['age']) + '\n\n')
        f.write('end - ' + ' '.join(searchDict['end']) + '\n\n')
        f.write('able - ' + ' '.join(searchDict['able']) + '\n\n')
        f.write('format - ' + ' '.join(searchDict['format']) + '\n\n')
        f.write('read - ' + ' '.join(searchDict['read']) + '\n\n')
    

if __name__ == '__main__':
    main()