from cs50 import get_int

# we use get_int to make sure the user inputs a int,
# also to convert it from string to int.
height = get_int("Height: ")

# while loop to keep asking the user for a valid positive integer between (1-8)
while (height <= 0 or height > 8):
    height = get_int("Height: ")

# loop height times to build the pyramid shape
for i in range(height):
    # First we print spaces only and end the print statment with nothing
    print(" " * (height - 1 - i), end = "")
    # Second we print our hash to represent a block in the pyramid and we end it with two spaces
    print("#" * (i + 1) , end = "  ")
    # Third Step is to print hashes equal to the (i)th column.
    print("#" * (i + 1))