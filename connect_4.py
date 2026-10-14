## connect 4

## color codes
class Bcolors:
  HEADER = '\033[95m' #purple
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'   #red
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

## victory condition = four 1's in a row or four 2's in a row (1 is yellow), horizontally, vertically and diagonally (not to be confused with Diagon Alley)
column_1 = [0,0,0,0,0,0]
column_2 = [0,0,0,0,0,0]
column_3 = [0,0,0,0,0,0]
column_4 = [0,0,0,0,0,0]
column_5 = [0,0,0,0,0,0]
column_6 = [0,0,0,0,0,0]
column_7 = [0,0,0,0,0,0]

## visualize the playing field with colors
column_1_playing_field = [" "," "," "," "," "," "]
column_2_playing_field = [" "," "," "," "," "," "]
column_3_playing_field = [" "," "," "," "," "," "]
column_4_playing_field = [" "," "," "," "," "," "]
column_5_playing_field = [" "," "," "," "," "," "]
column_6_playing_field = [" "," "," "," "," "," "]
column_7_playing_field = [" "," "," "," "," "," "]

## victory condition checker

def victory_checker_yellow():

  ## verticals:  x = cd(ab v be v ef)
  if column_1[2] == 1 and column_1[3] == 1 and ((column_1[0] == 1 and column_1[1] == 1) or (column_1[1] == 1 and column_1[4] == 1) or (column_1[4] == 1 and column_1[5] == 1)):
    return 0
  elif column_2[2] == 1 and column_2[3] == 1 and ((column_2[0] == 1 and column_2[1] == 1) or (column_2[1] == 1 and column_2[4] == 1) or (column_2[4] == 1 and column_2[5] == 1)):
    return 0
  elif column_3[2] == 1 and column_3[3] == 1 and ((column_3[0] == 1 and column_3[1] == 1) or (column_3[1] == 1 and column_3[4] == 1) or (column_3[4] == 1 and column_3[5] == 1)):
    return 0
  elif column_4[2] == 1 and column_4[3] == 1 and ((column_4[0] == 1 and column_4[1] == 1) or (column_4[1] == 1 and column_4[4] == 1) or (column_4[4] == 1 and column_4[5] == 1)):
    return 0
  elif column_5[2] == 1 and column_5[3] == 1 and ((column_5[0] == 1 and column_5[1] == 1) or (column_5[1] == 1 and column_5[4] == 1) or (column_5[4] == 1 and column_5[5] == 1)):
    return 0
  elif column_6[2] == 1 and column_6[3] == 1 and ((column_6[0] == 1 and column_6[1] == 1) or (column_6[1] == 1 and column_6[4] == 1) or (column_6[4] == 1 and column_6[5] == 1)):
    return 0
  elif column_7[2] == 1 and column_7[3] == 1 and ((column_7[0] == 1 and column_7[1] == 1) or (column_7[1] == 1 and column_7[4] == 1) or (column_7[4] == 1 and column_7[5] == 1)):
    return 0

  ##horizontals
  #  x=       c         and        d         and         (a         and        b          or         b         and        e          or         e         and        f        ) or        (d         and        e         and        f         and        g)
  elif column_3[0] == 1 and column_4[0] == 1 and ((column_1[0] == 1 and column_2[0] == 1) or (column_2[0] == 1 and column_5[0] == 1) or (column_5[0] == 1 and column_6[0] == 1) or (column_4[0] == 1 and column_5[0] == 1 and column_6[0] == 1 and column_7[0] == 1)):
    return 0
  elif column_3[1] == 1 and column_4[1] == 1 and ((column_1[1] == 1 and column_2[1] == 1) or (column_2[1] == 1 and column_5[1] == 1) or (column_5[1] == 1 and column_6[1] == 1) or (column_4[1] == 1 and column_5[1] == 1 and column_6[1] == 1 and column_7[1] == 1)):
    return 0
  elif column_3[2] == 1 and column_4[2] == 1 and ((column_1[2] == 1 and column_2[2] == 1) or (column_2[2] == 1 and column_5[2] == 1) or (column_5[2] == 1 and column_6[2] == 1) or (column_4[2] == 1 and column_5[2] == 1 and column_6[2] == 1 and column_7[2] == 1)):
    return 0
  elif column_3[3] == 1 and column_4[3] == 1 and ((column_1[3] == 1 and column_2[3] == 1) or (column_2[3] == 1 and column_5[3] == 1) or (column_5[3] == 1 and column_6[3] == 1) or (column_4[3] == 1 and column_5[3] == 1 and column_6[3] == 1 and column_7[3] == 1)):
    return 0
  elif column_3[4] == 1 and column_4[4] == 1 and ((column_1[4] == 1 and column_2[4] == 1) or (column_2[4] == 1 and column_5[4] == 1) or (column_5[4] == 1 and column_6[4] == 1) or (column_4[4] == 1 and column_5[4] == 1 and column_6[4] == 1 and column_7[4] == 1)):
    return 0
  elif column_3[5] == 1 and column_4[5] == 1 and ((column_1[5] == 1 and column_2[5] == 1) or (column_2[5] == 1 and column_5[5] == 1) or (column_5[5] == 1 and column_6[5] == 1) or (column_4[5] == 1 and column_5[5] == 1 and column_6[5] == 1 and column_7[5] == 1)):
    return 0

  ## bot left to top right
  elif column_1[2] == 1 and column_2[3] == 1 and column_3[4] == 1 and column_4[5] == 1:
    return 0
  elif column_7[3] == 1 and column_6[2] == 1 and column_5[1] == 1 and column_4[0] == 1:
    return 0
  elif column_2[2] == 1 and column_3[3] == 1 and column_4[4] == 1 and ((column_5[5] == 1) or (column_1[1] == 1)):
    return 0
  elif column_4[1] == 1 and column_5[2] == 1 and column_6[3] == 1 and ((column_7[4] == 1) or (column_3[0] == 1)):
    return 0
  elif column_3[2] == 1 and column_4[3] == 1 and (((column_5[4] == 1) and (column_2[1] == 1)) or ((column_1[0] == 1) and (column_2[1] == 1)) or ((column_5[4] == 1) and (column_6[5] == 1))):
    return 0
  elif column_4[2] == 1 and column_5[3] == 1 and (((column_3[1] == 1) and (column_6[4] == 1)) or ((column_3[1] == 1) and (column_2[0] == 1)) or ((column_6[4] == 1) and (column_7[5] == 1))):
    return 0

    ## bot right to top left
  elif column_1[3] == 1 and column_2[2] == 1 and column_3[1] == 1 and column_4[0] == 1:
    return 0
  elif column_4[5] == 1 and column_5[4] == 1 and column_6[3] == 1 and column_7[2] == 1:
    return 0
  elif column_4[4] == 1 and column_5[3] == 1 and column_6[4] == 1 and ((column_3[5] == 1) or (column_7[1] == 1)):
    return 0
  elif column_2[3] == 1 and column_3[2] == 1 and column_4[1] == 1 and ((column_5[0] == 1) or (column_1[4] == 1)):
    return 0
  elif column_3[3] == 1 and column_4[2] == 1 and (((column_5[1] == 1) and (column_2[4] == 1)) or ((column_2[4] == 1) and (column_1[5] == 1)) or ((column_5[1] == 1) and (column_6[0] == 1))):
    return 0
  elif column_4[3] == 1 and column_5[2] == 1 and (((column_6[1] == 1) and (column_3[4] == 1)) or ((column_3[4] == 1) and (column_2[5] == 1)) or ((column_6[1] == 1) and (column_7[0] == 1))):
    return 0


def victory_checker_red():

  ## verticals:  cd(ab v be v ef)
  if column_1[2] == 2 and column_1[3] == 2 and ((column_1[0] == 2 and column_1[1] == 2) or (column_1[1] == 2 and column_1[4] == 2) or (column_1[4] == 2 and column_1[5] == 2)):
    return 0
  elif column_2[2] == 2 and column_2[3] == 2 and ((column_2[0] == 2 and column_2[1] == 2) or (column_2[1] == 2 and column_2[4] == 2) or (column_2[4] == 2 and column_2[5] == 2)):
    return 0
  elif column_3[2] == 2 and column_3[3] == 2 and ((column_3[0] == 2 and column_3[1] == 2) or (column_3[1] == 2 and column_3[4] == 2) or (column_3[4] == 2 and column_3[5] == 2)):
    return 0
  elif column_4[2] == 2 and column_4[3] == 2 and ((column_4[0] == 2 and column_4[1] == 2) or (column_4[1] == 2 and column_4[4] == 2) or (column_4[4] == 2 and column_4[5] == 2)):
    return 0
  elif column_5[2] == 2 and column_5[3] == 2 and ((column_5[0] == 2 and column_5[1] == 2) or (column_5[1] == 2 and column_5[4] == 2) or (column_5[4] == 2 and column_5[5] == 2)):
    return 0
  elif column_6[2] == 2 and column_6[3] == 2 and ((column_6[0] == 2 and column_6[1] == 2) or (column_6[1] == 2 and column_6[4] == 2) or (column_6[4] == 2 and column_6[5] == 2)):
    return 0
  elif column_7[2] == 2 and column_7[3] == 2 and ((column_7[0] == 2 and column_7[1] == 2) or (column_7[1] == 2 and column_7[4] == 2) or (column_7[4] == 2 and column_7[5] == 2)):
    return 0

  ## horizontals: x = cd( ab v be v ef) v defg
  elif column_3[0] == 2 and column_4[0] == 2 and ((column_1[0] == 2 and column_2[0] == 2) or (column_2[0] == 2 and column_5[0] == 2) or (column_5[0] == 2 and column_6[0] == 2) or (column_4[0] == 2 and column_5[0] == 2 and column_6[0] == 2 and column_7[0] == 2)):
    return 0
  elif column_3[1] == 2 and column_4[1] == 2 and ((column_1[1] == 2 and column_2[1] == 2) or (column_2[1] == 2 and column_5[1] == 2) or (column_5[1] == 2 and column_6[1] == 2) or (column_4[1] == 2 and column_5[1] == 2 and column_6[1] == 2 and column_7[1] == 2)):
    return 0
  elif column_3[2] == 2 and column_4[2] == 2 and ((column_1[2] == 2 and column_2[2] == 2) or (column_2[2] == 2 and column_5[2] == 2) or (column_5[2] == 2 and column_6[2] == 2) or (column_4[2] == 2 and column_5[2] == 2 and column_6[2] == 2 and column_7[2] == 2)):
    return 0
  elif column_3[3] == 2 and column_4[3] == 2 and ((column_1[3] == 2 and column_2[3] == 2) or (column_2[3] == 2 and column_5[3] == 2) or (column_5[3] == 2 and column_6[3] == 2) or (column_4[3] == 2 and column_5[3] == 2 and column_6[3] == 2 and column_7[3] == 2)):
    return 0
  elif column_3[4] == 2 and column_4[4] == 2 and ((column_1[4] == 2 and column_2[4] == 2) or (column_2[4] == 2 and column_5[4] == 2) or (column_5[4] == 2 and column_6[4] == 2) or (column_4[4] == 2 and column_5[4] == 2 and column_6[4] == 2 and column_7[4] == 2)):
    return 0
  elif column_3[5] == 2 and column_4[5] == 2 and ((column_1[5] == 2 and column_2[5] == 2) or (column_2[5] == 2 and column_5[5] == 2) or (column_5[5] == 2 and column_6[5] == 2) or (column_4[5] == 2 and column_5[5] == 2 and column_6[5] == 2 and column_7[5] == 2)):
    return 0

  ## bot left to top right
  elif column_1[2] == 2 and column_2[3] == 2 and column_3[4] == 2 and column_4[5] == 2:
    return 0
  elif column_7[3] == 2 and column_6[2] == 2 and column_5[1] == 2 and column_4[0] == 2:
    return 0
  elif column_2[2] == 2 and column_3[3] == 2 and column_4[4] == 2 and ((column_5[5] == 2) or (column_1[1] == 2)):
    return 0
  elif column_4[1] == 2 and column_5[2] == 2 and column_6[3] == 2 and ((column_7[4] == 2) or (column_3[0] == 2)):
    return 0
  elif column_3[2] == 2 and column_4[3] == 2 and (((column_5[4] == 2) and (column_2[1] == 2)) or ((column_1[0] == 2) and (column_2[1] == 2)) or ((column_5[4] == 2) and (column_6[5] == 2))):
    return 0
  elif column_4[2] == 2 and column_5[3] == 2 and (((column_3[1] == 2) and (column_6[4] == 2)) or ((column_3[1] == 2) and (column_2[0] == 2)) or ((column_6[4] == 2) and (column_7[5] == 2))):
    return 0

    ## bot right to top left
  elif column_1[3] == 2 and column_2[2] == 2 and column_3[1] == 2 and column_4[0] == 2:
    return 0
  elif column_4[5] == 2 and column_5[4] == 2 and column_6[3] == 2 and column_7[2] == 2:
    return 0
  elif column_4[4] == 2 and column_5[3] == 2 and column_6[4] == 2 and ((column_3[5] == 2) or (column_7[1] == 2)):
    return 0
  elif column_2[3] == 2 and column_3[2] == 2 and column_4[1] == 2 and ((column_5[0] == 2) or (column_1[4] == 2)):
    return 0
  elif column_3[3] == 2 and column_4[2] == 2 and (((column_5[1] == 2) and (column_2[4] == 2)) or ((column_2[4] == 2) and (column_1[5] == 2)) or ((column_5[1] == 2) and (column_6[0] == 2))):
    return 0
  elif column_4[3] == 2 and column_5[2] == 2 and (((column_6[1] == 2) and (column_3[4] == 2)) or ((column_3[4] == 2) and (column_2[5] == 2)) or ((column_6[1] == 2) and (column_7[0] == 2))):
    return 0

## function to print the field
def print_field():
  print(f"{column_1_playing_field[5]}|{column_2_playing_field[5]}|{column_3_playing_field[5]}|{column_4_playing_field[5]}|{column_5_playing_field[5]}|{column_6_playing_field[5]}|{column_7_playing_field[5]}")
  print(f"{column_1_playing_field[4]}|{column_2_playing_field[4]}|{column_3_playing_field[4]}|{column_4_playing_field[4]}|{column_5_playing_field[4]}|{column_6_playing_field[4]}|{column_7_playing_field[4]}")
  print(f"{column_1_playing_field[3]}|{column_2_playing_field[3]}|{column_3_playing_field[3]}|{column_4_playing_field[3]}|{column_5_playing_field[3]}|{column_6_playing_field[3]}|{column_7_playing_field[3]}")
  print(f"{column_1_playing_field[2]}|{column_2_playing_field[2]}|{column_3_playing_field[2]}|{column_4_playing_field[2]}|{column_5_playing_field[2]}|{column_6_playing_field[2]}|{column_7_playing_field[2]}")
  print(f"{column_1_playing_field[1]}|{column_2_playing_field[1]}|{column_3_playing_field[1]}|{column_4_playing_field[1]}|{column_5_playing_field[1]}|{column_6_playing_field[1]}|{column_7_playing_field[1]}")
  print(f"{column_1_playing_field[0]}|{column_2_playing_field[0]}|{column_3_playing_field[0]}|{column_4_playing_field[0]}|{column_5_playing_field[0]}|{column_6_playing_field[0]}|{column_7_playing_field[0]}")
  print("1|2|3|4|5|6|7")
  print("")

## insert coin functions (1 = yellow, 2 = red)
def insert_coin_yellow():
  column = int(input("Insert yellow coin: "))
  while column >7:
    column = int(input("Insert yellow coin: "))
  turn_completed = 0

  while turn_completed == 0:

    if column == 1 and column_1[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert yellow coin: "))
    if column == 2 and column_2[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert yellow coin: "))
    if column == 3 and column_3[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert yellow coin: "))
    if column == 4 and column_4[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert yellow coin: "))
    if column == 5 and column_5[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert yellow coin: "))
    if column == 6 and column_6[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert yellow coin: "))
    if column == 7 and column_7[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert yellow coin: "))

    if column == 1 and column_1[5] == 0:      ## column 1 statements
      if column_1[0] == 0:
        column_1[0] = 1
        column_1_playing_field[0] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_1[1] == 0:
        column_1[1] = 1
        column_1_playing_field[1] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_1[2] == 0:
        column_1[2] = 1
        column_1_playing_field[2] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_1[3] == 0:
        column_1[3] = 1
        column_1_playing_field[3] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_1[4] == 0:
        column_1[4] = 1
        column_1_playing_field[4] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_1[5] == 0:
        column_1[5] = 1
        column_1_playing_field[5] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return
    elif column == 2 and column_2[5] == 0:    ## column 2 statements
      if column_2[0] == 0:
        column_2[0] = 1
        column_2_playing_field[0] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_2[1] == 0:
        column_2[1] = 1
        column_2_playing_field[1] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_2[2] == 0:
        column_2[2] = 1
        column_2_playing_field[2] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_2[3] == 0:
        column_2[3] = 1
        column_2_playing_field[3] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_2[4] == 0:
        column_2[4] = 1
        column_2_playing_field[4] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_2[5] == 0:
        column_2[5] = 1
        column_2_playing_field[5] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return
    elif column == 3 and column_3[5] == 0:  ## column 3 statements
      if column_3[0] == 0:
        column_3[0] = 1
        column_3_playing_field[0] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_3[1] == 0:
        column_3[1] = 1
        column_3_playing_field[1] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_3[2] == 0:
        column_3[2] = 1
        column_3_playing_field[2] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_3[3] == 0:
        column_3[3] = 1
        column_3_playing_field[3] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_3[4] == 0:
        column_3[4] = 1
        column_3_playing_field[4] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_3[5] == 0:
        column_3[5] = 1
        column_3_playing_field[5] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return
    elif column == 4 and column_4[5] == 0:  ## column 4 statements
      if column_4[0] == 0:
        column_4[0] = 1
        column_4_playing_field[0] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_4[1] == 0:
        column_4[1] = 1
        column_4_playing_field[1] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_4[2] == 0:
        column_4[2] = 1
        column_4_playing_field[2] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_4[3] == 0:
        column_4[3] = 1
        column_4_playing_field[3] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_4[4] == 0:
        column_4[4] = 1
        column_4_playing_field[4] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_4[5] == 0:
        column_4[5] = 1
        column_4_playing_field[5] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return
    elif column == 5 and column_5[5] == 0:  ## column 5 statements
      if column_5[0] == 0:
        column_5[0] = 1
        column_5_playing_field[0] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_5[1] == 0:
        column_5[1] = 1
        column_5_playing_field[1] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_5[2] == 0:
        column_5[2] = 1
        column_5_playing_field[2] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_5[3] == 0:
        column_5[3] = 1
        column_5_playing_field[3] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_5[4] == 0:
        column_5[4] = 1
        column_5_playing_field[4] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_5[5] == 0:
        column_5[5] = 1
        column_5_playing_field[5] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return
    elif column == 6 and column_6[5] == 0:  ## column 6 statements
      if column_6[0] == 0:
        column_6[0] = 1
        column_6_playing_field[0] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_6[1] == 0:
        column_6[1] = 1
        column_6_playing_field[1] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_6[2] == 0:
        column_6[2] = 1
        column_6_playing_field[2] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_6[3] == 0:
        column_6[3] = 1
        column_6_playing_field[3] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_6[4] == 0:
        column_6[4] = 1
        column_6_playing_field[4] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_6[5] == 0:
        column_6[5] = 1
        column_6_playing_field[5] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return
    elif column == 7 and column_7[5] == 0:  ## column 7 statements
      if column_7[0] == 0:
        column_7[0] = 1
        column_7_playing_field[0] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_7[1] == 0:
        column_7[1] = 1
        column_7_playing_field[1] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_7[2] == 0:
        column_7[2] = 1
        column_7_playing_field[2] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_7[3] == 0:
        column_7[3] = 1
        column_7_playing_field[3] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_7[4] == 0:
        column_7[4] = 1
        column_7_playing_field[4] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      elif column_7[5] == 0:
        column_7[5] = 1
        column_7_playing_field[5] = (f"{Bcolors.WARNING}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return
def insert_coin_red():
  column = int(input("Insert red coin: "))
  while column > 7:
    column = int(input("Insert red coin: "))
  turn_completed = 0

  while turn_completed == 0:

    if column == 1 and column_1[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert red coin: "))
    if column == 2 and column_2[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert red coin: "))
    if column == 3 and column_3[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert red coin: "))
    if column == 4 and column_4[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert red coin: "))
    if column == 5 and column_5[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert red coin: "))
    if column == 6 and column_6[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert red coin: "))
    if column == 7 and column_7[5] != 0:
      print(f"Column {column} is full! Choose another!")
      column = int(input("Insert red coin: "))

    if column == 1 and column_1[5] == 0:      ## column 1 statements
      if column_1[0] == 0:
        column_1[0] = 2
        column_1_playing_field[0] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_1[1] == 0:
        column_1[1] = 2
        column_1_playing_field[1] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_1[2] == 0:
        column_1[2] = 2
        column_1_playing_field[2] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_1[3] == 0:
        column_1[3] = 2
        column_1_playing_field[3] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_1[4] == 0:
        column_1[4] = 2
        column_1_playing_field[4] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_1[5] == 0:
        column_1[5] = 2
        column_1_playing_field[5] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return
    elif column == 2 and column_2[5] == 0:    ## column 2 statements
      if column_2[0] == 0:
        column_2[0] = 2
        column_2_playing_field[0] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_2[1] == 0:
        column_2[1] = 2
        column_2_playing_field[1] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_2[2] == 0:
        column_2[2] = 2
        column_2_playing_field[2] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_2[3] == 0:
        column_2[3] = 2
        column_2_playing_field[3] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_2[4] == 0:
        column_2[4] = 2
        column_2_playing_field[4] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_2[5] == 0:
        column_2[5] = 2
        column_2_playing_field[5] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return
    elif column == 3 and column_3[5] == 0:  ## column 3 statements
      if column_3[0] == 0:
        column_3[0] = 2
        column_3_playing_field[0] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_3[1] == 0:
        column_3[1] = 2
        column_3_playing_field[1] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_3[2] == 0:
        column_3[2] = 2
        column_3_playing_field[2] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_3[3] == 0:
        column_3[3] = 2
        column_3_playing_field[3] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_3[4] == 0:
        column_3[4] = 2
        column_3_playing_field[4] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_3[5] == 0:
        column_3[5] = 2
        column_3_playing_field[5] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return
    elif column == 4 and column_4[5] == 0:  ## column 4 statements
      if column_4[0] == 0:
        column_4[0] = 2
        column_4_playing_field[0] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_4[1] == 0:
        column_4[1] = 2
        column_4_playing_field[1] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_4[2] == 0:
        column_4[2] = 2
        column_4_playing_field[2] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_4[3] == 0:
        column_4[3] = 2
        column_4_playing_field[3] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_4[4] == 0:
        column_4[4] = 2
        column_4_playing_field[4] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_4[5] == 0:
        column_4[5] = 2
        column_4_playing_field[5] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return
    elif column == 5 and column_5[5] == 0:  ## column 5 statements
      if column_5[0] == 0:
        column_5[0] = 2
        column_5_playing_field[0] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_5[1] == 0:
        column_5[1] = 2
        column_5_playing_field[1] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_5[2] == 0:
        column_5[2] = 2
        column_5_playing_field[2] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_5[3] == 0:
        column_5[3] = 2
        column_5_playing_field[3] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_5[4] == 0:
        column_5[4] = 2
        column_5_playing_field[4] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_5[5] == 0:
        column_5[5] = 2
        column_5_playing_field[5] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return
    elif column == 6 and column_6[5] == 0:  ## column 6 statements
      if column_6[0] == 0:
        column_6[0] = 2
        column_6_playing_field[0] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_6[1] == 0:
        column_6[1] = 2
        column_6_playing_field[1] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_6[2] == 0:
        column_6[2] = 2
        column_6_playing_field[2] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_6[3] == 0:
        column_6[3] = 2
        column_6_playing_field[3] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_6[4] == 0:
        column_6[4] = 2
        column_6_playing_field[4] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_6[5] == 0:
        column_6[5] = 2
        column_6_playing_field[5] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return
    elif column == 7 and column_7[5] == 0:  ## column 7 statements
      if column_7[0] == 0:
        column_7[0] = 2
        column_7_playing_field[0] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_7[1] == 0:
        column_7[1] = 2
        column_7_playing_field[1] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_7[2] == 0:
        column_7[2] = 2
        column_7_playing_field[2] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_7[3] == 0:
        column_7[3] = 2
        column_7_playing_field[3] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_7[4] == 0:
        column_7[4] = 2
        column_7_playing_field[4] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      elif column_7[5] == 0:
        column_7[5] = 2
        column_7_playing_field[5] = (f"{Bcolors.FAIL}o{Bcolors.ENDC}")
        return
      else:
        print("Error")
        return


## red: ask for coin, print field, check victory
def player_yellow_turn():
  insert_coin_yellow()
  print_field()
  victory_checker_yellow()
def player_red_turn():
  insert_coin_red()
  print_field()
  victory_checker_red()

## gameplay loop
def gameplay_loop():
  while victory_checker_yellow() != 0 or victory_checker_red() !=0:
    player_yellow_turn()
    if victory_checker_yellow() == 0:
      print("Player 1 won!")
      return
    player_red_turn()
    if victory_checker_red() == 0:
      print("Player 2 won!")
      return


## Start game
print("This is Connect 4! Integers only else crash")
print_field()
gameplay_loop()