from cs50 import SQL
from sys import argv, exit
from csv import reader, DictReader

db = SQL("sqlite:///students.db")


def main():

    # Check command line args
    if len(argv) != 2:
        print("Exactly one commmand line argument must be entered")
        exit(1)

    # Open CSV file given by command line arg
    with open(argv[1], "r") as csvfile:

        reader = DictReader(csvfile)

        # Loop through students
        for row in reader:
            nameSplit = ((row["name"]).split())

            # Insert None where there is no middle name
            if (len(nameSplit) == 2):
                nameSplit.insert(1, None)

            # Insert each student into students table of students.db using db.execute
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       nameSplit[0], nameSplit[1], nameSplit[2], row["house"], row["birth"])


main()