## it tries to run and if it doesnt work it closes (i guess)

with open("file_try_and_finally.txt","w") as file:
    file = file.write("Hello world!")

try:
    file = open("file_try_and_finally.txt","r")     # Perform operations on the file
    print(f"File opened, the content:\n{file.read()}")
finally:
    file.close()                                    # Ensures file close even if an exception occurs
