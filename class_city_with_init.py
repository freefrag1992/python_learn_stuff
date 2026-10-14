## way to go for classes

class City:
  def __init__(self,name,nickname,founding,country,population,landmarks):
    self.name = name
    self.nickname = nickname
    self.founding = founding
    self.country = country
    self.population = population
    self.landmarks = landmarks

oberhausen = City("oberhausen","Wiege des Ruhrgebiets",1862,"Germany",220000,"Gasometer")
print(vars(oberhausen))
