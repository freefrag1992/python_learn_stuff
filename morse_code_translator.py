
morse_alphabet_dictionary = {
    "a": ".-",    "b": "-...",  "c": "-.-.",  "d": "-..",
    "e": ".",     "f": "..-.",  "g": "--.",   "h": "....",
    "i": "..",    "j": ".---",  "k": "-.-",   "l": ".-..",
    "m": "--",    "n": "-.",    "o": "---",   "p": ".--.",
    "q": "--.-",  "r": ".-.",   "s": "...",   "t": "-",
    "u": "..-",   "v": "...-",  "w": ".--",   "x": "-..-",
    "y": "-.--",  "z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--",
    "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.",
    "!": "-.-.--", "/": "-..-.",  "(": "-.--.",  ")": "-.--.-",
    "&": ".-...",  ":": "---...", ";": "-.-.-.", "=": "-...-",
    "+": ".-.-.",  "-": "-....-", "_": "..--.-", '"': ".-..-.",
    "$": "...-..-", "@": ".--.-.", " ": "/"
}
# approach: dictionary, only lower case (input is converted to lower case)
# enter text, search for x in text and give out the other value


text = input("Enter the text to translate into morse code:")
text = text.lower()
print(f"The following text will be transcribed to morse code: {text}")

for x in text:
    print(morse_alphabet_dictionary[x])



