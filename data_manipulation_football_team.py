##a list of dictionaries
# like: players_date = [ {"name":"your mum"}, {"name":"your father} ]
# basically dictionaries within a list

players_data = [
    {"name": "Patrick Mahomes", "position": "Quarterback", "jersey_number": 15, "yards_gained": 400, "touchdowns": 3},
    {"name": "Tyreek Hill", "position": "Wide Receiver", "jersey_number": 10, "yards_gained": 150, "touchdowns": 2},
]

names = [x["name"] for x in players_data] # looking for each "name" within players_data
print("Players Names:",names)


players_data[0]["name"] = "Patricia Mahomes"
print(players_data[0])
