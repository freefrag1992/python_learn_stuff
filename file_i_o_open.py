## OPEN FILES in python with the open("filename.txt","mode") function
#  modes can be "r" = read; "w" = write and "a" = add
#  example: file_1 = open("file_a.txt","w")

## opened files should be CLOSED at the end
#  example: file_1.close()
# Better close it with this:
# with open("filename.txt","r") as f: <--- this will close the file after executing its content

##### Example
### text_file = open("sample_file.txt","w")
### text_file.write("This is pretty interesting stuff!\n")
### text_file.close()

##### or

### with open("sample_file.txt","a") as text_file:
###     text_file.write("This is pretty amazing stuff!\n")