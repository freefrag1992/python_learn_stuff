import random
number = random.randint(1, 9)

question = str(input("Enter your YES/NO question!\n"))
if number == 1:
  number = str("Yes - definitely.")
elif number == 2:
  number = str("It is decidedly so.")
elif number == 3:
  number = str("Without a doubt.")
elif number == 4:
  number = str("Reply hazy, try again.")
elif number == 5:
  number = str("Ask again later.")
elif number == 6:
  number = str("Better not tell you now.")
elif number == 7:
  number = str("My sources say no.")
elif number == 8:
  number = str("Outlook not so good.")
elif number == 9:
  number = str("Very doubtful.")

print(number)
