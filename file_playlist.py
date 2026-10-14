#filename.write(content)
#filename.writelines("line1\nline2\n...")
#filename.readline
## callback to functions: def function_name(a,b,...): // a,b etc. as variables within function

## task: create a function to display and write liked songs to a file

## liked_songs = {"title":"artist"}
liked_songs = {
    "Bad Habits": "Ed Sheeran",
    "I'm Just Ken": "Ryan Gosling",
    "Mastermind": "Taylor Swift",
    "Uptown Funk": "Mark Ronson ft. Bruno Mars",
    "Ghost": "Justin Bieber"
}
new_song = {"Haruka Kanata":"Asian Kung-Fu Generation"}
russian_songs = {"Vesna":"Kangi","Pustoj Vokzal":"Morgenshtern","Krasnyj Flag":"Morgenshtern"}
# Function to display and write liked songs to a file

def write_liked_songs_to_file(title, file_name):
    with open(file_name, "w") as file:
        file.write("Dave\'s favorite songs:\n")
        for title, artist in title.items():       ## list of liked_song.items() => title:artist
            file.write(f"{title} by {artist}\n")
    print(f"Successfully wrote liked songs to {file_name}")

# Function to ADD liked songs to a file
def add_liked_songs_to_file(title, file_name):
    with open(file_name, "a") as file:
        for title, artist in title.items():       ## list of liked_song.items() => title:artist
            file.write(f"{title} by {artist}\n")    ## very important: for every title and artist dictionary
    print(f"Successfully added liked songs to {file_name}")

# Write liked songs to a .txt file
write_liked_songs_to_file(liked_songs, "playlist.txt")
add_liked_songs_to_file(new_song, "playlist.txt")
add_liked_songs_to_file({"Vesna":"Kangi"}, "playlist.txt") ## instead of new_song you could also enter your dictionary

## create a new filename

write_liked_songs_to_file(russian_songs, "playlist_russian.txt") ## work wohoo