## long version without def __init__(self,...)

class Restaurant:
  name = ""
  style = ""
  rating = 0.0
  delivery = False

pizza_palace = Restaurant()
pizza_palace.name = "Pizza Palace"
pizza_palace.style = "Italian"
pizza_palace.rating = 4.4
pizza_palace.delivery = True

kebab_house = Restaurant()
kebab_house.name = "Kebab House"
kebab_house.style = "Arab"
kebab_house.rating = 3.8
kebab_house.delivery = False

print(vars(pizza_palace))
print(vars(kebab_house))