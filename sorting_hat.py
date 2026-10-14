gryffindor = 0
ravenclaw = 0
hufflepuff = 0
slytherin = 0

question_1 = int(input("Do you like (1)Dawn or (2)Dusk\n"))

if question_1 == 1:
  gryffindor = gryffindor + 1
  ravenclaw = ravenclaw + 1
elif question_1 == 2:
  hufflepuff = hufflepuff + 1
  slytherin = slytherin + 1
else:
  print("Wrong answer 1!")

question_2 = int(input("When I’m dead, I want people to remember me as:\n(1)The Good\n(2)The Great\n(3)The Wise\n(4)The Bold\n"))

if question_2 == 1:
  hufflepuff = hufflepuff + 2
elif question_2 == 2:
  slytherin = slytherin + 2
elif question_2 == 3:
  ravenclaw = ravenclaw + 2
elif question_2 == 4:
  gryffindor = gryffindor + 2
else:
  print("Wrong answer 2!")

question_3 = int(input("Which kind of instrument most pleases your ear?\n(1)The violin\n(2)The trumpet\n(3)The piano\n(4)The drum\n"))

if question_3 == 1:
  slytherin = slytherin + 4
elif question_3 == 2:
  hufflepuff = hufflepuff + 4
elif question_3 == 3:
  ravenclaw = ravenclaw + 4
elif question_3 == 4:
  gryffindor = gryffindor + 4
else:
  print("Wrong answer 3!")

print("Gryffindor:" + str(gryffindor))
print("Hufflepuff:" + str(hufflepuff))
print("Slytherin: " + str(slytherin))
print("Ravenclaw: " + str(ravenclaw))

if gryffindor >= hufflepuff and gryffindor >= slytherin and gryffindor >= ravenclaw:
  print("You are a Gryffindor!")
elif hufflepuff >= gryffindor and hufflepuff >= slytherin and hufflepuff >= racenclaw:
  print("You are a Hufflepuff!")
elif slytherin >= gryffindor and slytherin >= hufflepuff and slytherin >= ravenclaw:
  print("You are a Slytherin!")
else:
  print("You are a Racenclaw!")
