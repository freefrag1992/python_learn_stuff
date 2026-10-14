ph = float(input("How much pH on a scale from 0-14"))

if ph > 7:
  print("Basic")
elif ph < 7:
  print("Acidic")
else:
  print("Neutral")
