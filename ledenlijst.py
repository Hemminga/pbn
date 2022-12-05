import csv
import re
from pprint import pprint


if __name__ == '__main__':
    # Ask for filename
    file = input("Enter path to csv ledenlijst:")
    # Use a default in case no filename is entered
    if file == '':
        file = "../../Sync/2022_Norg-deelnemers.csv"
    output = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            group = 'A'
            m = re.match('(\w)', row['paarnummer'])
            if m:
                group = m.group(0)
            m = re.search('(\d+)', row['paarnummer'])
            if m:
                number = m.group(0)
            else:
                print('Unknown error')
            row['group'] = group
            row['number'] = number
            output.append(row)
    pprint(output)
