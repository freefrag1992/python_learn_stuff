# .seek() and truncate()
# .seek(bytenumber) jumps the cursor to a specific point
# .truncate(bytenumber) erases everything after the byte

# pretend we have written a regretful message and we want to delete it

sent_message = "Dude, what the fuck is wrong with you?!"

with open("file_and_error.txt","w") as file:
    file.write(sent_message)

with open("file_and_error.txt","r+") as file: # "r+" -->> read AND write
    original_message = file.read()
    file.seek(0)                        ## move cursor to the bytenumber
    file.truncate(0)                    ## file size reduction (delete everything after bytenumber)
    unsent_message = "This was deleted by the author!"
    file.write(unsent_message)

# what we have done: move cursor to the beginning, wipe everything after the beginning and write something new