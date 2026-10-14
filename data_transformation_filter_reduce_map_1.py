from functools import reduce

playlist = [('What Was I Made For?', 3.42), ('Just Like That', 5.05), ('Song 3', 6.8), ('Leave The Door Open', 4.02), ('I Can\'t Breath', 4.47), ('Bad Guy', 3.14)]

def longer_than_five_minutes(song):
    return song[1] > 5.00

long_songs = filter(longer_than_five_minutes, playlist)
print(list(long_songs))

def minutes_to_seconds(duration):
    return duration[1] * 60

song_time = map(minutes_to_seconds, playlist)
print(list(song_time))

def add_durations(total, song):
  duration = song[1]
  return total + duration

total_duration = reduce(add_durations,playlist,0) ## starts with 0 as initial 0 was given
print(total_duration)

