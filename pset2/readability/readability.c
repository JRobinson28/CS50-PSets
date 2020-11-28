#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <string.h>

int  main(void)
{
    // Ask for text
    string text = get_string("Text: ");

    // Count number of letters
    float l = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if ((text[i] >= 'a' && text[i] <= 'z') ||
            (text[i] >= 'A' && text[i] <= 'Z'))
        {
            l++;
        }
    }
    //printf("Letter(s): %.0f\n", l);

    // Count number of words
    float w = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 32)
        {
            w++;
        }
    }
    //printf("Word(s): %.0f\n", w);

    // Count number of sentences
    float s = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 46 || text[i] == 33 || text[i] == 63)
        {
            s++;
        }
    }
    //printf("Sentence(s): %.0f\n", s);

    // Calculate average number of letters & sentences per 100 words
    float L = 100 * (l / w);
    float S = 100 * (s / w);

    // Calculate Coleman-Liau index
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Return result
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}