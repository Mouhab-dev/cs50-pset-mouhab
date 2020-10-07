/*
###################################################################

###########                                             ###########
###########                                             ###########
###########                                             ###########
                             This Is SC50
                     Created By: MOHAB TAHER EL-BANNA
                              From EGYPT
###########
###########                                             ###########
###########                                             ###########
###########                                             ###########

###################################################################
*/

#include "helpers.h"
#include <math.h>
#include <stdlib.h>
#include <string.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int grayscale = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            grayscale = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.000);
            image[i][j].rgbtBlue = grayscale;
            image[i][j].rgbtGreen = grayscale;
            image[i][j].rgbtRed = grayscale;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    unsigned char temp = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < round(width / 2) ; j++)
        {
            temp = image[i][j].rgbtRed;
            image[i][j].rgbtRed = image[i][width - 1 - j].rgbtRed;
            image[i][width - 1 - j].rgbtRed = temp;

            temp = image[i][j].rgbtGreen;
            image[i][j].rgbtGreen = image[i][width - 1 - j].rgbtGreen;
            image[i][width - 1 - j].rgbtGreen = temp;

            temp = image[i][j].rgbtBlue;
            image[i][j].rgbtBlue = image[i][width - 1 - j].rgbtBlue;
            image[i][width - 1 - j].rgbtBlue = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Temporary storage
    RGBTRIPLE temp[height][width];

    // Copying the image to keep an unaltered version to loop over
    memcpy(temp, image, sizeof(RGBTRIPLE) * height * width);

    // Iterate over every row of the image
    for (int i = 0; i < height; i++)
    {
        // Iterate over every column of the image
        for (int j = 0; j < width; j++)
        {
            // Initiate average counter at 0.0
            // Gotta avoid the truncated integer problem
            float average = 0.0;

            // Initiate RGB values at 0
            int blue = 0;
            int green = 0;
            int red = 0;

            // Iterate over rows around current row
            for (int k = -1; k <= 1; k++)
            {
                // Iterate over columns around current column
                for (int l = -1; l <= 1; l++)
                {
                    // If current row + next row are not bigger than the width of the image or less than the boundary
                    // If current column + next column are not bigger than the height of the image or less than the boundary
                    if (i + k != height && i + k != -1 && j + l != width && j + l != -1)
                    {
                        // Update RGB values to sum them later
                        blue += temp[i + k][j + l].rgbtBlue;
                        green += temp[i + k][j + l].rgbtGreen;
                        red += temp[i + k][j + l].rgbtRed;
                        // Increment average by one for one pixel which will be included in  the sum
                        average += 1;
                    }
                }
            }
            // Set each RGB values to their blurred values
            image[i][j].rgbtBlue = round(blue / average);
            image[i][j].rgbtGreen = round(green / average);
            image[i][j].rgbtRed = round(red / average);
        }
    }
    return;
}

// Function to stop the result if it exceeds 255 (maximum pixel value)
int threshold(int value)
{
    if (value > 255)
    {
        value = 255;
    }
    return value;
}


// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Temporary storage
    RGBTRIPLE temp[height][width];

    // Copying the image to keep an unaltered version to loop over
    memcpy(temp, image, sizeof(RGBTRIPLE) * height * width);

    float tBlueY = 0.0;
    float tGreenY = 0.0;
    float tRedY = 0.0;
    float tBlueX = 0.0;
    float tGreenX = 0.0;
    float tRedX = 0.0;

    float filter_X [3][3] = {{-1.0, 0.0, 1.0},
                            {-2.0, 0.0, 2.0},
                            {-1.0, 0.0, 1.0}};

    float filter_Y [3][3] = {{-1.0, -2.0, -1.0},
                            {0.0, 0.0, 0.0},
                            {1.0, 2.0, 1.0}};

    // Iterate over every coloumn of the image
    for (int i = 0; i < height; i++)
    {
        // Iterate over every row of the image
        for (int j = 0; j < width; j++)
        {
            tBlueY = 0.0;
            tGreenY = 0.0;
            tRedY = 0.0;
            tBlueX = 0.0;
            tGreenX = 0.0;
            tRedX = 0.0;

            // Iterate over rows around current row
            for (int k = -1; k <= 1; k++)
            {
                // Iterate over columns around current coloumn
                for (int l = -1; l <= 1; l++)
                {
                    // If current row + next row are not bigger than the width of the image or less than the boundary
                    // If current column + next column are not bigger than the height of the image or less than the boundary
                    if (i + k != height && i + k != -1 && j + l != width && j + l != -1)
                    {
                        // calculates convolution for vertical borders
                        tBlueX += image[i + k][j + l].rgbtBlue * filter_X[(k + 1)][(l + 1)];
                        tGreenX += image[i + k][j + l].rgbtGreen * filter_X[(k + 1)][(l + 1)];
                        tRedX += image[i + k][j + l].rgbtRed * filter_X[(k + 1)][(l + 1)];

                        // calculates convolution for horizantal borders
                        tBlueY += image[i + k][j + l].rgbtBlue * filter_Y[(k + 1)][(l + 1)];
                        tGreenY += image[i + k][j + l].rgbtGreen * filter_Y[(k + 1)][(l + 1)];
                        tRedY += image[i + k][j + l].rgbtRed * filter_Y[(k + 1)][(l + 1)];
                    }
                }
            }
            temp[i][j].rgbtBlue = threshold(round(sqrt(tBlueX * tBlueX + tBlueY * tBlueY)));
            temp[i][j].rgbtGreen = threshold(round(sqrt(tGreenX * tGreenX + tGreenY * tGreenY)));
            temp[i][j].rgbtRed = threshold(round(sqrt(tRedX * tRedX + tRedY * tRedY)));
        }
    }

    // make a loop again to copy pixel values from temp to image after finishing our work
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }
    }

    return;
}
