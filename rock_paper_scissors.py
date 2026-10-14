import random

gaming = 1
while gaming == 1:
    randomized_rps = ["Rock","Paper","Scissors"]
    enemy_rps = random.choice(randomized_rps)

    my_rps = int(input("Rock, Paper or Scissors?\n(1)Rock\n(2)Paper\n(3)Scissors\n"))
    if my_rps == 1:
        print("You chose Rock!")
    elif my_rps == 2:
        print("You chose Paper!")
    elif my_rps == 3:
        print("You chose Scissors!")
    else:
        print("Invalid input")

    print("The enemy chose "+enemy_rps+"!")
    if enemy_rps == "Rock" and my_rps == 1:
        print("Draw!\n")
    elif enemy_rps == "Paper" and my_rps == 1:
        print("You lose!\n")
    elif enemy_rps == "Scissors" and my_rps == 1:
        print("You win!\n")
    elif enemy_rps == "Rock" and my_rps == 2:
        print("You win!\n")
    elif enemy_rps == "Paper" and my_rps == 2:
        print("Draw!\n")
    elif enemy_rps == "Scissors" and my_rps == 2:
        print("You lose!\n")
    elif enemy_rps == "Rock" and my_rps == 3:
        print("You lose!\n")
    elif enemy_rps == "Paper" and my_rps == 3:
        print("You win!\n")
    elif enemy_rps == "Scissors" and my_rps == 3:
        print("Draw!\n")
    else:
        print("Invalid input")
    gaming = int(input("Do you want to play again?\n(1)Yes\n(2)No\n"))


