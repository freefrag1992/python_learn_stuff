from functools import reduce

#data transformation

# map(function,data)
## map() applies the given function to each element in the data and returns a new list.
### It's perfect for when you need to perform the same operation on every item in a list, tuple, or data set.

def divide_by_2(x):
  return x / 2

halved_numbers = map(divide_by_2,[1,2,3,4,5,6,7,8])
print(list(halved_numbers))


## filter(function,data) --> function need to return a boolean
def filter_even(x):
  return x % 2 == 0
even_numbers = filter(filter_even,[1,2,3,4,5,6,7,8])
print(list(even_numbers))

## reduce(function,data,initial) -> red
# reduce() takes a collection of iterable data and combines its elements into a single value via a function.
# An optional initial value can be used, as well.

def multiply(x,y):
    return x * y
product = reduce(multiply,[1,2,3,4,5])
print(product)
