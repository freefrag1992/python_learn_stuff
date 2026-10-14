
#filename.write(content)
#filename.writelines("line1\nline2\n...")
#filename.readline
#open file as write
#subsequent .readline() go for the next line

with open("file_i_o_read_write.txt", "w") as file_i_o_read_write:
    file_i_o_read_write.write("This is line 1\n")
    file_i_o_read_write.write("This is line 2\n")
    file_i_o_read_write.writelines("This is line 3\nThis is line 4\n")

print("\nThe file has been written.\n")     ## for knowledge
print("The content of the file is:")        ## for knowledge

#open file as read
with open("file_i_o_read_write.txt", "r") as file_i_o_read_write:
    content = file_i_o_read_write.read()
    print(content)

#open file as read again to get a task done
print("\nPrinting first 2 lines:")

with open("file_i_o_read_write.txt", "r") as file_i_o_read_write:
    line_1 = file_i_o_read_write.readline()
    line_2 = file_i_o_read_write.readline()
    print(line_1,end="")                ## print(abc,end="") to erase standard newline \n
    print(line_2,end="")                ## it would be doubled if we didnt delete it

#open file to read all lines with .readlines()
print("\nPrinting all lines:")

with open("file_i_o_read_write.txt", "r") as file_i_o_read_write:
    lines = file_i_o_read_write.readlines()
    for x in lines:
        print(x,end="")

## open("file_name.txt","r+") as file: <--- r+ means read AND write. if i had known ealrier...