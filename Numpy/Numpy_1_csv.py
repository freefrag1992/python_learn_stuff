import numpy as np
import csv
print(f"Numpy Version: {np.__version__}")

### CSV
## "a" = append
## "w" = write

### Insert Array
notifications = np.array([4,42,74,47,75,123,102])


def clear_csv(): ##### resets csv
    data_to_write = np.array([
    ])
    with open("Numpy_1_csv.csv", "w", newline="") as file:  ## newline="" -> newline parameter ensures new line after space
        csv_writer = csv.writer(file)  # Create a CSV writer object
        csv_writer.writerows(data_to_write)  # Write the data_to_write list to the CSV file
def create_csv():
    with open("Numpy_1_csv.csv", "w",newline="") as file:  ## newline="" -> newline parameter ensures new line after space ## "a" = append
        csv_writer = csv.writer(file)
    for x in range(len(notifications)):
        day = x
        data_to_write = np.array([
            [day+1,notifications[day]]
        ])
        with open("Numpy_1_csv.csv", "a", newline="") as file:  ## newline="" -> newline parameter ensures new line after space ## "a" = append
            csv_writer = csv.writer(file)  # Create a CSV writer object
            csv_writer.writerows(data_to_write)  # Write the data_to_write list to the CSV file
        day = x + 1
def append_csv():
    with open("Numpy_1_csv.csv", "r", newline="") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            current_day = int(row[0])
    for x in range(len(notifications)):
        data_to_write = np.array([
            [current_day+1,notifications[x]]
        ])
        with open("Numpy_1_csv.csv", "a", newline="") as file:  ## newline="" -> newline parameter ensures new line after space ## "a" = append
            csv_writer = csv.writer(file)  # Create a CSV writer object
            csv_writer.writerows(data_to_write)  # Write the data_to_write list to the CSV file
        with open("Numpy_1_csv.csv", "r", newline="") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                current_day = int(row[0])
        x = x + 1

### Program
## Choose Operation (remove # and run)
# -------------------
# clear_csv()
# create_csv()
# append_csv()
# -------------------

