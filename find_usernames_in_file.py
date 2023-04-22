#########################################################
#This code checks the contents of the file for valid usernames
def read_and_clean_file(filename):
    with open(filename, 'r') as f:
        content = f.readlines()

    cleaned_content = set()  # use the set to automatically get rid of duplicates

    for line in content:
        line = line.strip()  # remove spaces and newlines
        if line.startswith('@'):
            cleaned_content.add(line)

    return cleaned_content


def main():
    file1 = '1000.txt'

    cleaned_file1 = read_and_clean_file(file1)

    with open('Results_ready_for_use/results1000.txt', 'w') as f:
        f.write('\n'.join(cleaned_file1))


if __name__ == "__main__":
    main()
