height = int(input("Your height in cm?"))
cost = int(input("How many credits do you have?"))

if height >= 137 and cost >= 10:
  print("Enjoy the ride!")
elif height <137 and cost >=10:
  print("You are not tall enough to ride!")
elif height >=137 and cost <10:
  print("You dont have enough credits!")
else:
  print("You are not tall enough and you dont have enough credits!")
