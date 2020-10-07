#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    //Declaring two variables for sotring the total amount of coins and the change
    float change;
    int total = 0;
    //prompt the user to enter amount of change
    do
    {
        change = get_float("Change owed: ");
    }
    while (change < 0 || change == 0.0);

    //Round up the number the user has inputted to be easy while working on it
    int cents = round(change * 100);

    //Loop for which we work on the change to subtract from it every time untill it reaches zero
    while (cents != 0)
    {
        //subtract 25 if the cents larger than or equal to 25
        //increment total count of coins after every subtraction
        if (cents >= 25)
        {
            cents = cents - 25;
            total += 1;
        }
        //subtract 10 if the cents larger than or equal to 10
        //increment total count of coins after every subtraction
        else if (cents >= 10)
        {
            cents = cents - 10;
            total += 1;
        }
        //subtract 5 if the cents larger than or equal to 5
        //increment total count of coins after every subtraction
        else if (cents >= 5)
        {
            cents = cents - 5;
            total += 1;
        }
        //subtract 1 if the cents larger than or equal to 1
        //increment total count of coins after every subtraction
        else
        {
            cents = cents - 1;
            total += 1;
        }
    };
    //print out the total minimum number of coins needed for the change
    printf("%i\n", total);
}
