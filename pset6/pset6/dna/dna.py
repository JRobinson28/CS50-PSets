from csv import reader, DictReader
from sys import argv, exit


def main():

    # Handle command line arguments
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    db_path = argv[1]
    seq_path = argv[2]

    # Open csv file and convert to dict
    with open(db_path, "r") as csvfile:
        reader = DictReader(csvfile)
        dict_list = (list(reader))

    # Open sequences file and append to list
    with open(seq_path, "r") as file:
        sequence = file.read()
        seq_list = [char for char in sequence]

    # For each STR, compute longest run of consecutive repeats in sequence

    # Loop through each STR
    max_counts = []

    for i in range(1, len(reader.fieldnames)):
        STR = reader.fieldnames[i]
        max_counts.append(0)

        # Loop through sequence to find STR
        for j in range(len(sequence)):
            STR_count = 0

            # If match found, start counting repeats
            if sequence[j:(j + len(STR))] == STR:
                k = 0
                while sequence[(j + k):(j + k + len(STR))] == STR:
                    STR_count += 1
                    k += len(STR)
                # If new maximum of repeats, update max_counts
                if STR_count > max_counts[i - 1]:
                    max_counts[i - 1] = STR_count

    # Compare against data
    for i in range(len(dict_list)):
        matches = 0
        for j in range(1, len(reader.fieldnames)):

            if int(max_counts[j - 1]) == int(dict_list[i][reader.fieldnames[j]]):
                matches += 1
            if matches == (len(reader.fieldnames) - 1):
                print(dict_list[i]['name'])
                exit(0)

    print("No match")


main()