#sets are like a list where the contents are unique and not ordered
#set1.union(set2) set1.intersection(set2) and set1.difference(set2)
# set1.add() set1.remove() to add or remove stuff

fruits_david = {"apple","banana","strawberry","kiwi"}
fruits_maurice = {"apple","strawberry","pineapple","pear"}

fruits_intersection = fruits_david.intersection(fruits_maurice)
fruits_union = fruits_david.union(fruits_maurice)
fruits_difference = fruits_david.difference(fruits_maurice)

print(f"David and Maurice like {fruits_intersection}")
print(f"David's and Mauice's favorite fruits are {fruits_union}")
print(f"The difference between David's and Maurice's taste: {fruits_difference}")