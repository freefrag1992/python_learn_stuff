from math import pi
from random import choice as ch

planets = [
 'Mercury',
 'Venus',
 'Earth',
 'Mars',
 'Saturn']

random_planet = ch(planets)
if random_planet == "Mercury":
  radius = 2440
if random_planet == "Venus":
  radius = 6052
if random_planet == "Earth":
  radius = 6371.
if random_planet == "Mars":
  radius = 3390
if random_planet == "Saturn":
  radius = 58232

area = pi*4*radius**2
print(random_planet+"\'s area is: "+str(round(area,2))+" square units.")


