#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Get card number
    long n;
    {
        n = get_long("Number: ");
    }

    // Count length
    int i = 0;
    long cc = n;
    while (cc > 0)
    {
        cc = cc / 10;
        i++;
    }

    // Check if length is valid
    if (i != 13 && i != 15 && i != 16)
    {
        printf("INVALID\n");
        return 0;
    }

    // Calculate checksum
    int sum1 = 0;
    int sum2 = 0;
    long x = n;
    int total = 0;
    int mod1;
    int mod2;
    int d1;
    int d2;
    do
    {
        // Remove last digit and add to sum
        mod1 = x % 10;
        x = x / 10;
        sum1 = sum1 + mod1;
        // Remove second last digit
        mod2 = x % 10;
        x = x / 10;
        // Double second last digit and add digits to sum
        mod2 = mod2 * 2;
        d1 = mod2 % 10;
        d2 = mod2 / 10;
        sum2 = sum2 + d1 + d2;
    }
    while (x > 0);
    total = sum1 + sum2;

    // Get starting digits
    long start = n;
    do
    {
        start = start / 10;
    }
    while (start > 100);


    // Next check Luhn's Algorithm
    if (total % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }

    // Next check starting digits for card type
    if ((start / 10 == 5) && (0 < start % 10 && start % 10 < 6))
    {
        printf("MASTERCARD\n");
    }

    else if ((start / 10 == 3) && (start % 10 == 4 || start % 10 == 7))
    {
        printf("AMEX\n");
    }

    else if (start / 10 == 4)
    {
        printf("VISA\n");
    }

    else
    {
        printf("INVALID\n");
    }
}