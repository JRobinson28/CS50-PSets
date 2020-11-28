#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

const int N = 26;
const string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";


int main(int argc, string argv[])
{
    // Check for correct number of args
    if (argc != 2)
    {
        printf("Please provide one command line argument only.\n");
        return 1;
    }

    else
    {
        // Check validity of key length
        if (strlen(argv[1]) != N)
        {
            printf("Key must be %i characters long.\n", N);
            return 1;
        }

        // Check validity of key content
        int letters[N];
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            // Check only letters are used
            if (!((argv[1][i] >= 'a' && argv[1][i] <= 'z') ||
                  (argv[1][i] >= 'A' && argv[1][i] <= 'Z')))
            {
                printf("Key must contain only letters.\n");
                return 1;
            }

            // Convert to uppercase
            else if (argv[1][i] >= 'a' && argv[1][i] <= 'z')
            {
                argv[1][i] = toupper(argv[1][i]);
            }

            // Check for repeated letters
            for (int j = 0; j < N; j++)
            {
                if (argv[1][i] == letters[j])
                {
                    printf("Key must not contain repeated letters.\n");
                    return 1;
                }
            }

            letters[i] = argv[1][i];
        }


        // Ask for plaintext
        string plaintext = get_string("plaintext: ");
        int l = strlen(plaintext);
        char ciphertext[l + 1];

        // Convert to ciphertext

        // Loop through each char in plaintext
        for (int i = 0; i < l; i++)
        {
            // Check if uppercase and if so use standard alphabet/key
            if (isupper(plaintext[i]) != 0)
            {
                for (int j = 0; j < strlen(alphabet); j++)
                {
                    if (plaintext[i] == alphabet[j])
                    {
                        ciphertext[i] = argv[1][j];
                        break;
                    }
                }
            }

            // If lowercase use lowercase alphabet and key
            else if (islower(plaintext[i]) != 0)
            {
                for (int j = 0; j < strlen(alphabet); j++)
                {
                    if (plaintext[i] == tolower(alphabet[j]))
                    {
                        ciphertext[i] = tolower(argv[1][j]);
                        break;
                    }
                }
            }

            // Finally replace non letters
            else
            {
                ciphertext[i] = plaintext[i];
            }
        }

        // Add null char to make it a string
        ciphertext[l] = '\0';

        // Print result and exit
        printf("ciphertext: %s\n", ciphertext);
        return 0;
    }
}