#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Ask user for name
    string answer = get_string("What's your name?\n");
    // Say hello
    printf("hello, %s\n", answer);
}