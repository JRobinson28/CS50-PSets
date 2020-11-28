from cs50 import get_string


def main():

    # Ask for text
    text = get_string("Text: ")

    # Count number of letters, words, sentences
    l = s = 0
    w = 1
    for i in range(len(text)):

        if text[i].isalpha():
            l += 1

        if text[i] == " ":
            w += 1

        if text[i] in [".", "!", "?"]:
            s += 1

    # Calculate averages per 100 words
    L = 100 * (l / w)
    S = 100 * (s / w)

    # Calculate Coleman-Liau index
    index = round(0.0588 * L - 0.296 * S - 15.8)

    # Print result
    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


main()