import random
symbols = ["🍒","🍇", "🍉", "7️⃣"]

play_again = "1"

while play_again == "1":
    result_1 = random.choices(symbols)
    result_2 = random.choices(symbols)
    result_3 = random.choices(symbols)
    print(str(result_1)+"|"+str(result_2)+"|"+str(result_3))

    if result_1 == result_2 and result_1 == result_3 and result_1 == "7️⃣":
        print("JACKPOT!\n")
    elif result_1 == result_2 and result_1 == result_3 and result_1 == "🍒":
        print("Three o'cherries!\n")
    elif result_1 == result_2 and result_1 == result_3 and result_1 == "🍉":
        print("M-m-melon!\n")
    elif result_1 == result_2 and result_1 == result_3 and result_1 == "🍇":
        print("PLUMS!\n")
    play_again = input(print("Play again?\n(1)Yes\n(2)No\n"))


