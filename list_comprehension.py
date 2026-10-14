# list comprehension like this

## [expression for item in dataset if condition]

# The expression is applied to each item.
## A for..in statement loops through each item.
### An optional if condition can filter out items.

# The dataset can be something iterable like a list or tuple. List comprehensions do not change the original list.
## does not work with WHILE

## original approach

# numbers_list = [1, 2, 3, 4, 5]
# squares = []
#
# for x in numbers_list:
#     squared = x * x
#     squares.append(squared) ## .append()
# print(squares)
#
# ## list comprehension is this:
#
# squared_numbers = [number ** 2 for number in numbers_list] ## number_squared for each number in the list
# print(f"Original numbers: {numbers_list}")
# print(f"Squared numbers: {squared_numbers}")


numbers_list = [57, 10, 82, 36, 89, 46, 13, 23, 92, 48]

even_numbers = [number for number in numbers_list if number % 2 == 0]
odd_numbers = [number for number in numbers_list if number % 2 == 1]
print(f"Even numbers {even_numbers}")
print(f"Odd numbers {odd_numbers}")