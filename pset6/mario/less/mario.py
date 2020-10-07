from cs50 import get_int

# we use get_int to make sure the user inputs a int,
# also to convert it from string to int.
height = get_int("Height: ")

# while loop to keep asking the user for a valid positive integer between (1-8)
while (height <= 0 or height > 8):
    height = get_int("Height: ")

for i in range(height):
    print(" " * (height - 1 - i), end = "")
    print("#" * (i + 1))