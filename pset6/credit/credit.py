from cs50 import get_int
from sys import exit

# Get card number
cc = get_int("Number: ")

# Count length
length = len(str(cc))

# Check length
if length not in [13, 15, 16]:
    print("INVALID")
    exit(1)

# Calculate checksum
sum1 = sum2 = 0
x = cc

while x > 0:

    # Remove last digit and add to sum
    mod1 = x % 10
    x = x // 10
    sum1 = sum1 + mod1

    # Remove second last digit
    mod2 = x % 10
    x = x // 10

    # Double second last digit and add digits to sum
    mod2 = mod2 * 2
    d1 = mod2 % 10
    d2 = mod2 // 10
    sum2 = sum2 + d1 + d2

total = sum1 + sum2

# Check Luhn algorithm
if (total % 10) != 0:
    print("INVALID")
    exit(2)

# Check starting digits
if str(cc)[0] == "4":
    print("VISA")

elif (str(cc)[0] == "5") and (0 < int(str(cc)[1]) < 6):
    print("MASTERCARD")

elif (str(cc)[0] == "3") and (str(cc)[1] == "4" or str(cc)[1] == "7"):
    print("AMEX")

else:
    print("INVALID")

