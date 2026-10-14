# split() method to make the input a list using WHITESPACES as separation
# note: this is a list and really shitty for math
## separator: The string will separate at the specified separator. If it’s not provided then any whitespace is a separator.
## maxsplit: A string will split into a maximum of a specified number of times. The default is -1, which means there is no limit

a,b = input("Input the 2 short sides of a 90° triangle").split()
print("a:",a,"b:",b)

x = ((float(a)*(float(a)))+(float(b)*(float(b))))**0.5
print("x:",x)

# example max split

f,g = input("Some text").split(".", -1) # HERE a dot seperates the inputs # -1 means splits endlessly

print("f:",f,"g:",g)