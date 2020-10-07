#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string);
int count_words(string);
int count_sentences(string);

int main(void)
{
    int letters = 0;
    int sentences = 0;
    int words = 0;

    int grade = 0;

    string phrase = get_string("Text: ");

    //convert text to lowercase first
    for (int i = 0; phrase[i]; i++)
    {
        phrase[i] = tolower(phrase[i]);
    }

    //printf("%s\n", phrase);
    //calling count_letters function to return its value in variable called letters
    letters = count_letters(phrase);

    printf("Letters: ");
    printf("%i\n", letters);
    

    //calling count_words function to return its value in variable called words
    words = count_words(phrase);

    /*
    printf("Words: ");
    printf("%i\n", words);
    */

    //calling count_sentences function to return its value in variable called sentences
    sentences = count_sentences(phrase);
    /*
    printf("Sentences: ");
    printf("%i\n", sentences);
    */

    grade = round((0.0588 * ((float) letters * 100 / (float) words)) - (0.296 * ((float) sentences * 100 / (float) words)) - 15.8);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade ");
        printf("%i\n", grade);
    }

}


//function to count letters in a text
int count_letters(string phrase)
{

    int letters_count = 0;

    for (int i = 0; phrase[i]; i++)
    {
        if ((phrase[i] >= 'a' && phrase[i] <= 'z'))
        {
            letters_count += 1;
        }
    }

    return letters_count;

}

//function to count words in a text
int count_words(string phrase)
{
    int words_count = 0;
    int length = strlen(phrase);
    for (int i = 0; i <= length ; i++)
    {
        if (phrase[i] == ' ' || phrase[i] == '\0')
        {
            words_count += 1;
        }
    }

    return words_count;

}

//funtion that calculates number of words in a text
int count_sentences(string phrase)
{
    int sentences_count = 0;

    for (int i = 0; phrase[i] ; i++)
    {
        if (phrase[i] == '.' || phrase[i] == '!' || phrase[i] == '?')
        {
            sentences_count += 1;
        }
    }

    return sentences_count;

}


