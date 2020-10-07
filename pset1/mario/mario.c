#include <stdio.h>
#include <cs50.h>
int main(void)
{
    //making a variable to store height
    int height;

    //Prompt the user for height in range (1-8) correctly if wrong we keep asking the user again
    do
    {
        height = get_int("Height in range (1-8): ");
    }
    while (height < 1 || height > 8);

    //Navigating the coloumns with variable i
    for (int i = 0; i < height; i++)
    {
        //adding space s times less than the height based on which coloumn we are working on
        for (int s = 1; s < height - i ; s++)
        {
            printf(" ");
        }
        //adding the hashes
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        //print two spaces
        printf("  ");
        //print the hases again
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        //making a new line for the new coloumn
        printf("\n");
    }
}
