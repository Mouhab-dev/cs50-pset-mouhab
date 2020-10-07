/*
###################################################################

###########                                             ###########
###########                                             ###########
###########                                             ###########
                             This Is CS50
                     CODED BY: MOHAB TAHER EL-BANNA
                              From EGYPT
###########
###########                                             ###########
###########                                             ###########
###########                                             ###########

###################################################################
*/


// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 65535; // the more we increase N the more memory (space) we take but with less time searching

// Hash table
node *table[N];

unsigned int words_count = 0; // global variable which stores the size of dictionary (number of words)

// Returns true if word is in dictionary else false
bool check(const char *word)
{

    int n = strlen(word);

    char cpy_word[LENGTH + 1];

    for (int i = 0; i < n; i++)
    {
        cpy_word[i] = tolower(word[i]);
    }

    // Adds null terminator to end string
    cpy_word[n] = '\0';

    unsigned int value = hash(cpy_word);

    node *tmp = table[value];

    while (tmp != NULL)
    {
        // check if the word is found in the dictionary and return true if found
        if (strcasecmp(tmp->word, cpy_word) == 0)
        {
            return true;
        }
        tmp = tmp->next;
    }
    free(tmp);
    // We have break out the for loop that means we have reached the end of the linked list
    // (Condition: tmp == NULL) so return false
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash = 0;

    for (int i = 0, n = strlen(word); i < n; i++)
    {
        hash = (hash << 2) ^ word[i];
    }

    return hash % N; // We use mod N to make sure we stay in the valid range of N
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file != NULL)
    {
        // temporary variable to store in the word which will be read from the dictionary
        char word[LENGTH + 1];
        // loop which ends when we reach to the end of dictionary file
        while (fscanf(file, "%s", word) != EOF)
        {
            // allocates a memory place for a single node
            node *n = malloc(sizeof(node));
            // if there is any error while allocating memory of size node
            if (n == NULL)
            {
                printf("Not Enough Memory");
                unload(); // very important to not leak memory
                return 0;
            }
            // copy the word if passed the previous check
            strcpy(n->word, word);
            n->next = NULL; // this was my error for memory errors in valgrind

            // find the index first using the hash function
            int index = hash(word);

            // intial node like the one called "lists" in the lecture
            node *start = table[index];

            // checks if the index has already been assigned to a node then connect these nodes together
            if (start != NULL)
            {
                n->next = table[index]; // make the new node point to what the first node in the index points at
                table[index] = n;      // then make the first node in the index point at the new node to be added to this index
                words_count += 1; // increment the words as we load them in memory
            }
            else // if the index is still not assigned to any linked lists yet
            {
                table[index] = n;
                words_count += 1; // increment the words as we load them in memory
            }
        }
        // close the opened file and return true for successful loading
        fclose(file);
        return true;
    }
    // if there is any error while opening the dictionary then exit
    printf("File cannont be opend or maybe not found: %s\n", dictionary);
    return false;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return words_count; // return the global variable which will be edited by the load function
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // iterate over the array of linked lists N times
    for (int i = 0; i < N ; i++)
    {
        // assign the first node in the [i]th index to a temp node
        node *cursor = table[i];

        // if the index contains no linked lists inside of it then skip it
        // if the index contains linked lists then free them one by one till we reach to NULL
        while (cursor != NULL)
        {
            // creates a temp node which will then be a temp variable to store in the value of cursor
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
