#range(start,stop,step)

count = range(1,101,1)
for number in count:

  if int((number%3)) == 0 and int((number%5))== 0:
    print(str(number)+" fizzbuzz")
  elif int((number%3)) == 0:
    print(str(number)+" fizz")
  elif int((number%5) )== 0:
    print(str(number)+" buzz")
  else:
    print(number)
