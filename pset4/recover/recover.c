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

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{


    if (argc != 2)
    {
        printf("Usage: ./recover [Forensic Image]");
        return 1;
    }

    if (fopen(argv[1], "r") == NULL)
    {
        printf("File cannont be opend or maybe not found: %s\n", argv[1]);
        return 1;
    }

    uint8_t buffer[512];
    char filename[8];
    FILE *outputfile = NULL;
    int count_jpgs = 0;


    // open memorycard file
    FILE *inputfile = fopen(argv[1], "r");

    while (fread(buffer, sizeof(uint8_t), 512, inputfile) || feof(inputfile) == 0)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0))
        {
            // if the outputfile is opened close it to write a new one
            if (outputfile != NULL)
            {
                fclose(outputfile);
            }
            // open a file with a different name each time depends on the number of jpgs found
            sprintf(filename, "%03i.jpg", count_jpgs);
            outputfile = fopen(filename, "w");
            count_jpgs++;
        }

        // write to the file which has been opened.
        if (outputfile != NULL)
        {
            fwrite(buffer, sizeof(buffer), 1, outputfile);
        }

    }

    // close any opened files

    // close input file
    if (inputfile == NULL)
    {
        fclose(inputfile);
    }

    // close the output file
    if (outputfile == NULL)
    {
        fclose(outputfile);
    }
    return 0;
}
