# ez generation of pokemon data

class Pokemon:
  def __init__(self,entry,name,types,description,is_caught):
    self.entry = entry
    self.name = name
    self.types = types
    self.description = description
    self.is_caught = is_caught
  def speak(self): # voice of the pokemon
    return self.name+"! " + self.name+"!"
  def display_details(self): #ez prints
    print("Entry Number: "+str(self.entry))
    print("Name: "+self.name)
    print("Type: "+self.types)
    print("Description: "+self.description)
    if self.is_caught == True:
        print(self.name+" is already caught!")

pikachu = Pokemon(25,
                  "Pikachu",
                  "Electric",
                  "It has small electric sacs on both its cheeks. If threatened, it looses electric charges from the sacs.",
                  True)
pikachu.display_details()

print(pikachu.speak())


