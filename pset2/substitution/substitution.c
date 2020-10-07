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
    // declare a variable to check for the arguments if all alphabits and their length
    int check_digit = 0;
    // vaiable to store the length of the plain text as we iterate through it
    int check_length = 0;
    // variable called similar to check if there is any repeated letter in the key stream
    int count_similar = 0;

    // second make sure that the argument is all alphabits and with an appropriate length
    for (int f = 0; argv[1][f] ; f++)
    {
        if (!((argv[1][f] >= 'a' && argv[1][f] <= 'z') || (argv[1][f] >= 'A' && argv[1][f] <= 'Z')))
        {
            check_digit += 1;
        }

        for (int v = f + 1; argv[1][v] ; v++)
        {
            if (tolower(argv[1][f]) == tolower(argv[1][v]))
            {
                count_similar += 1;
            }
        }

        check_length = f + 1;
    }

    // if passes the above alpha test and length test continue the program
    if (check_digit == 0 && check_length == 26 && count_similar == 0)
    {
        // prompting the user for plaintext
        string str = get_string("plaintext: ");
        // this variable will store the index of the letter (alphabetical order) in plaintext
        int index = 0;

        // this block of code will loop the string
        for (int i = 0; str[i]; i++)
        {
            if ((str[i] >= 'a' && str[i] <= 'z') || (str[i] >= 'A' && str[i] <= 'Z'))
            {
                // if the letter in the string is lower case
                if islower(str[i])
                {
                    index = str[i] - 97;
                    str[i] = tolower(argv[1][index]);
                }
                // if the letter in the string is upper case
                else if isupper(str[i])
                {
                    index = str[i] - 65;
                    str[i] = toupper(argv[1][index]);
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
        printf("Key must contain 26 characters.\n");
        return 1;
    }


}