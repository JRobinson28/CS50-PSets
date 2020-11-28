#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Get Height
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n > 8 || 1 > n);

    // Print hash pattern
    for (int i = 0; i < n; i++)
    {
        // Initial Spaces
        for (int j = 1 ; j < n - i; j++)
        {
            printf(" ");
        }

        // Left hashes
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        // Gap
        printf("  ");

        // Right hashes
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        // New line
        printf("\n");
    }

}