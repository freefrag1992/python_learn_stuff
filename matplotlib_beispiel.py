import matplotlib.pyplot as plt                                                                 #Mathplotlib importieren

temperature = [-20,-10,0,10,20,25,40,50,60,80,100]
pt_1000 = [922,961,1000,1039,1078,1097,1155,1194,1232,1309,1385]
kty_81 = [1367,1495,1630,1772,1922,2000,2245,2417,2597,2980,3392]

plt.xlim(-20, 110)  # Startpunkt X-Achse, Endpunkt X-Achse
plt.ylim(-0, 4000)  # Startpunkt Y-Achse, Endpunkt Y-Achse
plt.plot(temperature, pt_1000,"g-o",label="PT 1000")    # g-o green und kreis
plt.plot(temperature, kty_81,"r-s",label="KTY 81")      # r-s rot und squared

plt.title("Temperaturabhängige Widerstände")
plt.xlabel("Temperatur [°C]")
plt.ylabel("Widerstand [Ω]")

plt.legend()
plt.show()

