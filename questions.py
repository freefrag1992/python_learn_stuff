## yes / no function returns 0 or 1

## question with yes or no

def yesno(question):
    print(question,"Y/N")
    answer = input()
    answer = answer.lower()
    if answer == "yes" or  answer == "y":
        print("Your answer was yes.")
        return 1
    if answer == "no" or answer == "n":
        print("Your answer was no.")
        return 0
    else:
        print("Wrong input!")
        return -1