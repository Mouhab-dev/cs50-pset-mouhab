'''
        THIS IS CS50
    MOHAB TAHER EL-BANNA
        FROM: EGYPT
'''

from sys import argv, exit
import csv
import cs50

# Create a databse file called students.db if it does not exist
# If exists it will overwrite it
# we won't run this line because the file has already been created for us
# open("students.db", "w").close()

# Open database file for sqlite
db = cs50.SQL("sqlite:///students.db")

# We do not need to create a table or schema since students.db is already ready to be used
# here is the code if we want to create a table in our database file
# db.execute("CREATE TABLE students (id INT, first VARCHAR(255), middle VARCHAR(255), last VARCHAR(255), house VARCHAR(10), birth INT)")

# Command line arguments check
if (len(argv) != 2):
    print("ERROR: Command line arguments: import.py CSV file")
    exit(1)

# Open csv file to read from it
with open(argv[1], "r") as file:

    # Create DictReader
    reader = csv.DictReader(file)

    # Iterate over each row in the csv file
    for row in reader:

        # Storing each column in the csv to variable with the same name
        name = row["name"]
        house = row["house"]
        birth = int(row["birth"])

        # Count spaces as we iterate over the string called name
        spc_count = 0

        first = ""
        middle = ""
        last = ""

        # Iterate over string extracting every char
        for char in name:
            # If spc_count = 0 and the current char is not a space then we still in the first name's place
            if spc_count == 0 and char != " ":
                first += char
            # If spc_count = 1 and the current char is not a space then are in the middle name's place
            elif spc_count == 1 and char != " ":
                middle += char
            # If spc_count = 2 and the current char is not a space then are in the last name's place
            elif spc_count == 2 and char != " ":
                last += char
            # The only situation that will trigger this else statment is if the char is indeed a space
            else:
                spc_count += 1

        # if spc_count after the for loop is 1 this means that there is only one space in the string
        # thus meaning we need to assign the middle name to the last and leave middle as null
        if spc_count == 1:
            last = middle
            middle = None

        # Add each row to the database before moving to the next row
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                    first, middle, last, house, birth)