from cs50 import get_int

# Prompt for height
while True:
    height = get_int("Height: ")
    if(0 < height < 9):
        break

# Print hash pattern
for i in range(height):

    # Initial spaces
    print(" " * (height - 1 - i), end="")

    # Left hashes
    print("#" * (i + 1), end="")

    # Middle space
    print("  ", end="")

    # Right hashes
    print("#" * (i + 1), end="")

    # New line
    print()

