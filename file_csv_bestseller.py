## .reader() method returns a list of rows where each row is a list of CSV data.

# .reader() and .writer()
# file.readline() to read first line

## From the csv module, we use the .reader() method to create a CSV reader object that displays our file content, row by row:

# import csv
# with open("example_1.csv","r") as file:
#     csv_reader = csv.reader(file) ## create a csv reader
#     for row in csv_reader:
#         print(row)
#       ^--- prints a list row by row

import csv

#what we want to know:
max_sales = 0.0
best_book = None

with open("file_csv_bestseller.csv","r",encoding="utf8") as file:  ## encoding="utf8" -> the csv file has letters that are not in the
    csv_reader = csv.reader(file)                                  ## normal format (CP1252) common: latin-1 and utf8 (utf8 uses all)
    file.readline()                                                ## skip first line to only deal with integers! file_header = next(csv_reader) would also work

    for row in csv_reader:
        # print(f"The book {str(row[0])} from {str(row[1])} sold for {float(row[4])} million Euros)")     #print row[4] which is the fifth row (sales in millions)
        sales = float(row[4])               # iterates all values the fifth row [4] look code above
        if sales > max_sales:
            max_sales = sales
            best_book = str(row[0])
    print(f"The name of the best book is \"{best_book}\".")
    print(f"It sold for {max_sales} million Euros.")

with open("file_csv_bestseller_info.csv","w",newline="",encoding="utf8") as file: #newline="" baby
    writer = csv.writer(file)
    writer.writerow(["Book","Author","Original language","First published","sales in millions","Genre"]) # header
    writer.writerow(["Bible","Various authors","Hebrew", "Aramaic", "Greek",-700,500,"Religious"])

