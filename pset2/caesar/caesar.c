/******

 *
 *
 *          CREATED BY MOHAB TAHER EL-BANNA From Egypt @ 2020
 *
 *
 *          THIS IS CS50 <3
 *
 *

*/

#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])
{

    // first check for empty arguments or more than 2 argumnets
    if (argv[1] == '\0' || argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // declare a variable to check for the arguments if all digits
    bool check_digit = 0;

    // second make sure that the argument is all digits
    for (int f = 0; argv[1][f] ; f++)
    {
                                                    // added this condition after submission but both works fine after check50
        if ((argv[1][f] >= 'a' && argv[1][f] <= 'z') || (argv[1][f] >= 'A' && argv[1][f] <= 'Z'))
        {
            check_digit = 0;
        }
        else
        {
            check_digit = 1;
        }
    }


    // if passes the above digits test continue the program
    if (check_digit == 1)
    {
        // Convert input to int type
        int k = atoi(argv[1]);

        if (k >= 0)
        {
            // prompting the user for plaintext
            string str = get_string("plaintext: ");

            // this block of code will loop the string to shift the letters with the value k
            for (int i = 0; str[i]; i++)
            {
                if ((str[i] >= 'a' && str[i] <= 'z') || (str[i] >= 'A' && str[i] <= 'Z'))
                {
                    // if the letter in the string is lower case
                    if islower(str[i])
                    {
                        str[i] = (((str[i] + k) - 97) % 26) + 97;
                    }
                    // if the letter in the string is upper case
                    else if isupper(str[i])
                    {
                        str[i] = (((str[i] + k) - 65) % 26) + 65;
                    }
                    // if neither then just print it as it is
                    else
                    {
                        str[i] = str[i];
                    }
                }

            }
            // print out the whole text after being encrypted
            printf("ciphertext: ");
            printf("%s\n", str);
            return 0;
        }
        else
        {
            printf("key is not a positive value\n");
        }

    }
    else // if it fails the check digits test then execute this code
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

}