import csv

data = [
  ['Item', 'Quantity'],
  ['Blender', 2],
  ['Posters', 30],
  ['Shoes', 2]
]

# with open("file_csv_packing_list.csv","w") as file:
#     csv_writer = csv.writer(file)                   # csv writer
#     for item,quantity in data:                      # iterate item and quantity from data
#         file.write(f"{item},{quantity}\n")

try:
    with open("file_csv_packing_list.csv","r") as file:
        csv_reader = csv.reader(file)               # csv reader
        for item,quantity in csv_reader:
            print(f"{item},{quantity}")
except FileNotFoundError:
    print("Packing List file not found.")
    question = int(input("Do you want to generate a new CSV?\n(1)=Yes\n(2)=No\n"))
    if question == 1:
        print("File created successfully.")
        with open("file_csv_packing_list.csv","w") as file:
            csv_writer = csv.writer(file)                   # csv writer
            for item,quantity in data:                      # iterate item and quantity from data
                file.write(f"{item},{quantity}\n")
                print(f"{item},{quantity}")
    else:
        print("CSV creation aborted!")