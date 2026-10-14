import random
bday_messages = ["Hope you have a very Happy Birthday!","It's your special day – get out there and celebrate!","You were born and the world got better – everybody wins!","Have lots of fun on your special day!","Another year of you going around the sun!"]
random_messages = (random.choice(bday_messages))

# import bday_messages # not needed here
import datetime

today = (datetime.date.today())
next_birthday = datetime.date(2026,1,25)
print("Date today: "+str(today))

time_difference = datetime.date(2026,1,25)-(datetime.date.today())

if next_birthday == today:
      print(bday_message.random_messages)
else:
    print("Your next birthday is in "+str(time_difference))
