# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Assignment 1

"""
Suraj Janakiraman
Net ID: sxj170022
Date: 09-04-2022
Class: CS 4395.001 Human Language Technologies
Professor: Dr.Karen Mazidi
"""
import os
import sys
import re
import pickle

import homework1_config as config
from PersonClass import Person
"""
1. Description of the program
A) Description: This program processes text within a csv file using Python. 
(B) data.csv is the file that the program will process. data.csv is an input file with 5 fields (last name, first name, middle initial, ID, and Office Phone). 
The program is supposed to modify the invalid fields so that they become valid. Examples of modification of fields include: 
  (B1) Modify the first character of first and last names to have a capital letter followed by lowercase (i.e. Jake Jason)
  (B2) Modify the middle initial such that it is a capital letter. If there is no middle initial, make sure to replace the empty middle initial string with 'X'
  (B3) Modify the ID: An ID is supposed to have 2 letters followed by 4 digits. The program uses regular expressions to check if an ID is valid or not. 
  (B4) Modify the phone number: A phone number is supposed to be in the following format 123-456-7890. The program should use regular expressions to check and see whether the
	phone number is valid or not. 

(C) How does the program work?
(C1) When the user runs Homework1_sxj170022.py, the program process information within the data.csv, and looks for invalid fields. 
(C2) If an invalid field is found, the console will print a message (i.e. ID invalid: 54454. ID is two letters followed by 4 digits. Please enter a valid ID: ). 
In the example,the user is asked to enter a valid ID after being told that the ID is invalid. 
If the invalid field is a phone number, the console prints the following message (i.e. Phone 555-877.4321 is invalid. Enter phone number in form 123-456-7890). 
The user is asked to enter a phone number in the form 123-456-7890. 
(C3) All the invalid fields will be flagged by the console until the user enters in the correct information for all Person objects. 

(D) File structure: 
(D1) Homework1_sxj170022.py: This program is responsible for reading in information from the data.csv file, performing the regular expression operations for the fields in 
the data.csv file, and outputting the information to a command line terminal.The program uses a dictionary to store all the fields from the data.csv file. 
(D2) PersonClass.py: This program is responsible for creating a Person object with the following fields as listed in data.csv file 
(last name, first name, middle initial, ID, and phone number). This program also has a method to display the Person objects. 
(D3) homework1_config.py: This program is used to store the file names in variables so that the file names do not have to be hardcoded every time they need to be referenced. 

"""

"""
read_data file downloads a file, reads the file line by line and processes it through
the usage of regular expressions. 
"""
def read_data_file(data_dir_path):
   # create a dictionary to store each object
    person_dict = {}
   # open the file
    with open(os.path.join(data_dir_path, config.input_file), 'r') as f:
        #skip the first line
        line = f.readline()
        #parse the fields in the remaining lines.
        while (line):
            line = f.readline()
            if (line):
                line = line.strip('\n')
                last, first, mi, id, phone = line.split(',') #split on the comma
                #Before displaying the persons we need to do regular expressions.

                #first start with the id'
                while (True):
                    if (re.match('^[A-Za-z]{2}[0-9]{4}', id)):
                        break
                    print("ID invalid: ", id, "\nID is two letters followed by 4 digits")
                    id = input("Please enter a valid id: ")

                #focus on regex for the phone numbers in the form 123-456-7890
                while (True):
                    if (re.match('\d{3}-\d{3}-\d{4}', phone)):
                        break
                    print("Phone ", phone, " is invalid\nEnter phone number in form 123-456-7890")
                    phone = input("Enter phone number: ")

                #focus on making the first letter of the first name capitalized
                first = first.capitalize()

                #do the same thing for the last name
                last = last.capitalize()

                #check for middle name
                if not mi or mi == '':
                    mi = 'X'
                else:
                    mi = mi[0].capitalize()
                # check for  duplicate persons or duplicate fields for multiple person objects
                if (person_dict.get(id, None)):
                    # duplicate entry
                    print("Person with this id(%s) already exists" % id)
                else:
                    person = Person(last, first, mi, id, phone)
                    person_dict[id] = person

    return person_dict
# the main of the program
#the main creates a pickle for each person in the dictionary
# the main also displays the program
def main(data_dir_path):
    person_dict = read_data_file(data_dir_path)

    # pickle persons
    pickle.dump(person_dict, open(os.path.join(data_dir_path, config.output_file), 'wb'))

    # read from pickle
    person_dict = pickle.load(open(os.path.join(data_dir_path, config.output_file), 'rb'))

    # display persons
    print("Employee List: ")
    for id in person_dict.keys():
        person = person_dict[id]
        person.display()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

#the call to the main.
# make sure that the user runs the program in a command line terminal
# the user should be careful to include a dot after python main.py
# HOW TO RUN COMMAND: python main.py .
if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("usage: %s <relative path to data/data.csv" % sys.argv[0])
        sys.exit(1)
    data_dir_path = sys.argv[1]
    main(data_dir_path)