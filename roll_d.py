import random
## rolls a dice with x sides
def roll_d(x):
    number = random.randint(1, x)
    return number

#print(roll_d(20))