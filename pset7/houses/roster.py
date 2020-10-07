'''
        THIS IS CS50
    MOHAB TAHER EL-BANNA
        FROM: EGYPT
'''

from sys import argv, exit
import cs50

# Command line arguments check
if (len(argv) != 2):
    print("ERROR: Command line arguments: roster.py housename")
    exit(1)

# Open database file for sqlite
db = cs50.SQL("sqlite:///students.db")

# SQL query the students table in the students.db database for all of the students in the specified house.
# Students should be ordered by last name. For students with the same last name, they should be ordered by first name.
rows = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", argv[1])

# for every item in rows which is a list of dictionaries
for item in rows:
    # Print first name followed by space
    print(item["first"], end=" ")
    # If only middle name exists print it, to avoid None appearing between first and last if middle name does not exist
    if item["middle"] != None :
        print(item["middle"], end=" ")
    # print last name followed by comma and born followed by space
    print(item["last"], end=", born ")
    # print value of the birth key in the dictionary
    print(item["birth"])