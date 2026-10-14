# CSV = comma-seperated values

# Each row in a CSV file typically represents a record, and the values within a record are separated by commas.
# This simple structure makes CSV a widely used format for storing and exchanging data between applications.

## .reader() method returns a list of rows where each row is a list of CSV data.




## From the csv module, we use the .reader() method to create a CSV reader object that displays our file content, row by row:

# import csv
# with open("example_1.csv","r") as file:
#     csv_reader = csv.reader(file) ## create a csv reader
#     for row in csv_reader:
#         print(row)
#       ^--- prints a list row by row

import csv
data_to_write = [
  ['Name', 'Age', 'Grade'],
  ['Alice', 25, 'A'],
  ['Bob', 22, 'B'],
  ['Charlie', 28, 'A+']
]

# .writerows() can parse something iterable (a list of lists for example) and writes it into the csv file

with open("file_csv.csv", "w", newline="") as file:   ## newline="" -> newline parameter ensures new line after space
    csv_writer = csv.writer(file)                   # Create a CSV writer object
    csv_writer.writerows(data_to_write)             # Write the data_to_write list to the CSV file
