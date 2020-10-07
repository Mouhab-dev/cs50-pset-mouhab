#include <stdio.h>
#include <cs50.h>


int main(void)
{
    //Prompt the user to enter a credit-card number
    long number = get_long("Number: ");
    //copy the user input in another variable to work out its length untill it reaches zero
    long credit_number = number;
    // counter to count the length of the credit-card number
    int length = 0;
    //declare a variable called sum to store the sum in it
    int sum = 0;
    //declare a variable called digit to split a number if it consists of two digits
    int digit = 0;
    //declare a variable to get the first two values of the credit-card number
    int f_2digits = 0;

    //this block of code calculates length of credit-card number
    while (credit_number != 0)
    {
        credit_number /= 10;
        length++;
    }


    //this block of code represents luhn's algorithm
    for (int i = 0 ; i < length ; i++)
    {
        //take sum of the numbers outside luhn's algorithm
        if (i % 2 == 0)
        {
            sum += number % 10;
            number /= 10;
        }


        //take sum of the numbers envolved in luhn's algorithm
        if (i % 2 != 0)
        {
            digit = (number % 10) * 2;

            while (digit > 0)
            {
                sum += digit % 10;
                digit = digit / 10;
            }
            number /= 10;
        }
        //grab the first two values from the left of the credit-card number
        if (i == length - 3)
        {
            f_2digits = number;
        }
    }

    //determine the type of the credit-card
    if (sum % 10 == 0)
    {
        if (length == 15 && (f_2digits == 34 || f_2digits == 37))
        {
            printf("AMEX\n");
        }
        else if (length == 16 && (f_2digits == 51 || f_2digits == 52 || f_2digits == 53 || f_2digits == 54 || f_2digits == 55))
        {
            printf("MASTERCARD\n");
        }
        else if ((length == 13 || length == 16) && ((f_2digits / 10) == 4))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}