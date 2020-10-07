from cs50 import get_int

# Prompt the user to enter a credit-card number
number = get_int("Number: ")
# copy the user input in another variable to work out its length untill it reaches zero
credit_number = str(number)
# counter to count the length of the credit-card number
length = 0
# declare a variable called sum to store the sum in it
total_sum = 0
# declare a variable called digit to split a number if it consists of two digits
digit = 0
# declare a variable to get the first two values of the credit-card number
f_2digits = 0

# this block of code calculates length of credit-card number
length = len(credit_number)

# this block of code represents luhn's algorithm
for i in range(length):

    # take sum of the numbers outside luhn's algorithm
    if (i % 2 == 0):
        total_sum += number % 10
        number = int(number / 10)

    # take sum of the numbers envolved in luhn's algorithm
    if (i % 2 != 0):
        digit = (number % 10) * 2

        # divide two-digit number into two separate numbers
        while (digit > 0):
            total_sum += digit % 10
            digit = int(digit / 10)

        number = int(number / 10)

    # grab the first two values from the left of the credit-card number
    if (i == length - 3):
        f_2digits = number

# determine the type of the credit-card
if (total_sum % 10 == 0):

    if (length == 15 and (f_2digits == 34 or f_2digits == 37)):
        print("AMEX")

    elif (length == 16 and (f_2digits >= 51 and f_2digits <= 55)):
        print("MASTERCARD")

    elif ((length == 13 or length == 16) and (int(f_2digits / 10) == 4)):
        print("VISA")

    else:
        print("INVALID")

else:
    print("INVALID")
