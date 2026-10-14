## Word and letter counter
# len() is a function
# .split is a method: divides the sentence into a list of words based on whitespace
# it means: text.split() = "hello, my friends!" becomes text = ["hello","my","friends!"]
# now we need to count all things inside with the len() function
# text input # a and A are different this is why I force the text to be lower case

text_input = input(print("Enter your text to find out how many characters and words you have used!"))
print("You entered the following text:\n"+str(text_input))
text = text_input.lower()

# character counter
print("The text has", len(text), "characters.")
# word counter
word_counter = text.split()
word_counter = len(word_counter)
print("The text has",word_counter,"words.")

# fun fact: the most letter used

letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","ö","ä","ü","ß"]
letter_usage = 0
most_used_letter = ""

letter_usage_list = input(print("Do you want to know how often letters were used? Y/N"))
letter_usage_list = letter_usage_list.lower()

if letter_usage_list == "yes" or letter_usage_list == "y":
    for x in letters:
        letter_usage = text.count(x)
        most_used_letter = x
        if text.count(x) != 0:
            print("The letter", most_used_letter, "was used", letter_usage, "times.")
