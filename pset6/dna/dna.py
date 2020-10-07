'''
        THIS IS CS50
    MOHAB TAHER EL-BANNA
        FROM: EGYPT
'''

from sys import argv, exit
import csv


def main():
    # check for correct no. of command line arguments
    if len(argv) != 3:
        print("Some command line arguments are missing: dna.py CSV file, TXT file")
        exit(1)

    STRs = []  # list to load STRs sequences from database file
    dna_database = {}  # define a dictionary to be a database

    with open(argv[1], "r") as database:
        # read from csv in dictionary method
        reader = csv.DictReader(database)
        # read from csv line by line
        lines = csv.reader(database)
        # Populate list of Short Tandem Repeats (STRs)
        STRs = reader.fieldnames[1:]
        # iterate over lines to make dictionary for database
        for line in lines:
            dna_database.update({line[0]: list(map(int, line[1:]))})

    # put the STRs in a dictionary and itialise the count with 0
    # define a dictionary to store no.of occurances of each pattern
    dna_STRs = dict.fromkeys(STRs, 0)

    # print(dna_STRs)
    # print(dna_database)

    # open sequence file to load the dna sequence
    with open(argv[2], 'r') as txt:
        sequence = txt.read()

    # call search function on each pattern and save their values in the dict
    for i in range(len(STRs)):
        dna_STRs[STRs[i]] = search(sequence, STRs[i])

    # print(dna_STRs)
    # call match function to check for a match
    match(dna_database, dna_STRs)


# search function with two argumnets (string to be searched, pattern)
def search(string, pattern):

    # i've used a window that hovers over the sequence searching for the patter
    length = len(string)
    pat_len = len(pattern)
    counter = 0  # counter to count for consistency in pattern
    stepsize = 1  # stepsize to stretch the window size if any continuous pattern are found
    maximum = 0  # max is the maximum number counter goes to when searching for a pattern

    # loop over the entire length of the dna sequence
    for i in range(0, length, stepsize):
        # if we find the desired pattern we execute the while loop
        if string[i:i + pat_len] == pattern:
            # while loop: keep stretching the window size to count the number of repeats
            while (string[i:i + (stepsize * pat_len)] == pattern * stepsize):
                counter += 1
                stepsize += 1
            # after while loop break, we need to set i to start from the last position of the window
            # to make sure we count only once and forward
            stepsize = stepsize * pat_len
            # if the maximum number we counted was smaller than the current count then update maximum number
            if maximum < counter:
                maximum = counter
            # after assiging the counter to max we reset it back to zero
            counter = 0
        else:
            # we reset back stepsize to 1, untill we find the pattern then we stretch it again
            stepsize = 1

    # return maximum number
    return maximum

# match function to check for a match in database


def match(dna_database, dna_STRs):
    # loop over the database
    for item in dna_database:
        # if found match
        if dna_database[item] == list(dna_STRs.values()):
            # print the name of the match and then return true
            print(item)
            return True

    # if we did not enter the if condition then there is no match
    print("No match")
    return False


# call main function to run the program
main()
