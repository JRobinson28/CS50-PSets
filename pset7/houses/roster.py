from cs50 import SQL
from sys import argv, exit

db = SQL("sqlite:///students.db")


def main():

    # Check command line arguments
    if len(argv) != 2:
        print("Exactly one commmand line argument must be entered")
        exit(1)

    # Query for students in specified house
    rows = db.execute("SELECT * FROM students WHERE house = ? ORDER BY last ASC", argv[1])

    # Print student names and DOBs
    for i in range(len(rows)):
        if rows[i]['middle'] == None:
            print(f"{rows[i]['first']} {rows[i]['last']}, born {rows[i]['birth']}")
        else:
            print(f"{rows[i]['first']} {rows[i]['middle']} {rows[i]['last']}, born {rows[i]['birth']}")


main()