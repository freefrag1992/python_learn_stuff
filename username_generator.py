import random
from functools import reduce

prefixes = ["Mystic", "Golden", "Dark", "Shadow", "Silver"]
suffixes = ["storm", "song", "fire", "blade", "whisper"]

def capitalize_first_letter(string):
    return string.capitalize()

# create list with cap. suffixes
capitalized_suffixes = list(map(capitalize_first_letter, suffixes)) ## mapping function to every item in the list

def create_fantasy_name(list_1, list_2):
  return random.choice(list_1) + ' ' + random.choice(list_2)

# random 10 names comprehension list
random_names_list = [create_fantasy_name(prefixes,capitalized_suffixes) for names in range(10)]

# returns true if fire is in the name
def fire_in_name(name):
    name = name.lower()
    if "fire" in name:
        return True

# concatenate name_1 and name_2
def concatenate_names (name_1,name_2):
    return name_1 + ', ' + name_2

# filters name from the random 10 list above to only show names with fire
filtered_names = list(filter(fire_in_name, random_names_list))

# reduces the name to create strings out of a list
reduced_names = reduce(concatenate_names,filtered_names)

def display_name_info():
    print(f"\nRandom name list:{random_names_list}")
    print(f"\nThe following names include fire: {filtered_names}")
    print(f"reduced names:{reduced_names}")

display_name_info()