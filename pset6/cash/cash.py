from cs50 import get_float

# Declaring two variables for sotring the total amount of coins and the change
change = 0.0
total = 0

# prompt the user to enter amount of change
change = get_float("Change owed: ")

# Keep asking the user till he colaborates
while (change < 0 or change == 0.0):
    change = get_float("Change owed: ")

# Round up the number the user has inputted to be easy while working on it
cents = round(change * 100)

# Loop for which we work on the change to subtract from it every time untill it reaches zero
while (cents != 0):

    # subtract 25 if the cents larger than or equal to 25
    # increment total count of coins after every subtraction
    if (cents >= 25):
        cents -= 25
        total += 1

    # subtract 10 if the cents larger than or equal to 10
    elif (cents >= 10):
        cents = cents - 10
        total += 1

    # subtract 5 if the cents larger than or equal to 5
    elif (cents >= 5):
        cents = cents - 5
        total += 1

    # subtract 1 if the cents larger than or equal to 1
    else:
        cents = cents - 1
        total += 1

# print out the total minimum number of coins needed for the change
print(f"{total}")
