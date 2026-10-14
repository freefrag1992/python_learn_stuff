import random

blackjack_cards = [2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11]

#blackjack_cards = [11,11,11,11,11,11] # to test aces working properly :)

random.shuffle(blackjack_cards)
deck_counter = -1


# Rules: Draw cards until you have 21 points. Ace is 1 or 11 which converts AUTOMATICALLY in retrospective

# player_1 game:
draw_card = 1
player_1_points = 0
has_ace = 0 # ace counter player 1

print("++++++++++++++++++++++++")
print("+++ Player 1's turn! +++")
print("++++++++++++++++++++++++")
print("Your points:",player_1_points)

while player_1_points < 22 and draw_card == 1:
    deck_counter = deck_counter + 1
    ask_continue = input("Do you want to draw a card? [y/n] \n")
    if ask_continue == "y":
        print("New card: "+str(blackjack_cards[deck_counter]))
        player_1_points = player_1_points + blackjack_cards[deck_counter]
        if has_ace >= 1 and player_1_points > 21:                               # retroactively uses ace as 1 instead of 11
            player_1_points = player_1_points - 10                              # before losing the game
            has_ace = has_ace - 1                                               # deduct ace usability
        if blackjack_cards[deck_counter] == 11 and player_1_points >21:
            player_1_points = player_1_points - 10
            has_ace = has_ace + 1                                               # add ace usability
        print("Your points: ", player_1_points)
    else:
        draw_card = 0

if player_1_points > 21:
    print("++++++++++++++++++++++++")
    print("+++ Player 1 BUSTED! +++")
    print("++++++++++++++++++++++++")

# player_2 game:
draw_card = 1
player_2_points = 0
has_ace = 0 # ace counter player 2

print("++++++++++++++++++++++++")
print("+++ Player 2's turn! +++")
print("++++++++++++++++++++++++")
print("Your points:",player_2_points)

while player_2_points < 22 and draw_card == 1:
    deck_counter = deck_counter + 1
    ask_continue = input("Do you want to draw a card? [y/n] \n")
    if ask_continue == "y":
        print("New card: "+str(blackjack_cards[deck_counter]))
        player_2_points = player_2_points + blackjack_cards[deck_counter]
        if has_ace >= 1 and player_2_points > 21:                               # retroactively uses ace as 1 instead of 11
            player_2_points = player_2_points - 10                              # before losing the game
            has_ace = has_ace - 1                                               # deduct ace usability
        if blackjack_cards[deck_counter] == 11 and player_2_points >21:
            player_2_points = player_2_points - 10
            has_ace = has_ace + 1                                               # add ace usability
        print("Your points: ", player_2_points)
    else:
        draw_card = 0

if player_2_points > 21:
    print("++++++++++++++++++++++++")
    print("+++ Player 2 BUSTED! +++")
    print("++++++++++++++++++++++++")

# winning evaluation
if player_1_points > player_2_points and player_1_points <22:
    print("Player 1:", player_1_points, "|| Player 2:", player_2_points)
    print("+")
    print("++")
    print("++++")
    print("++++++++++++")
    print("The winner: Player 1!")
elif player_2_points > player_1_points and player_2_points <22:
    print("Player 1:", player_1_points, "|| Player 2:", player_2_points)
    print("+")
    print("++")
    print("++++")
    print("++++++++++++")
    print("The winner: Player 2!")
elif player_2_points == player_1_points and player_2_points <22:
    print("Player 1:", player_1_points, "|| Player 2:", player_2_points)
    print("+")
    print("++")
    print("++++")
    print("++++++++++++")
    print("The winner: Draw!")
elif player_1_points and player_2_points > 22:
    print("Player 1:", player_1_points, "|| Player 2:", player_2_points)
    print("+")
    print("++")
    print("++++")
    print("++++++++++++")
    print("Both BUSTED!")

