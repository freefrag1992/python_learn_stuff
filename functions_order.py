## input and order and return it

def order(item):
  if item == 1:
    return "Cheeseburger"
  elif item == 2:
    return "Fries"
  elif item == 3:
    return "Soda"
  elif item == 4:
    return "Ice Cream"
  elif item == 5:
    return "Cookie"

option = int(input("What would you like to order?"))
print(order(option))

