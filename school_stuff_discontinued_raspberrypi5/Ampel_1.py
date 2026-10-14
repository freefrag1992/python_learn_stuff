import RPi.GPIO as GPIO
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

## GPIO pins from raspberry_pi_5
# switches on (16) and (18)
ped_switch_1 = GPIO.input(23)
ped_switch_2 = GPIO.input(24)

# red light on (3)
ped_red_on = GPIO.output(2, 1)
ped_red_off = GPIO.output(2, 0)
# green light on (5)
ped_green_on = GPIO.output(3, 1)
ped_green_off = GPIO.output(3, 0)
# red light on (8)
light_1_red_on = GPIO.output(14, 1)
light_1_red_off = GPIO.output(14, 0)
# yellow light on (10)
light_1_yellow_on = GPIO.output(15, 1)
light_1_yellow_off = GPIO.output(15, 0)
# green light on (12)
light_1_green_on = GPIO.output(18, 1)
light_1_green_off = GPIO.output(18, 0)

def Green_Phase():
    light_1_red_off = True
    light_1_yellow_off = True
    light_1_green_off = False

    light_1_red_on = False
    light_1_yellow_on = False
    light_1_green_on = True

    print("Car:")
    print("             | |")
    print("             | |")
    print(f"             |{bcolors.OKGREEN}o{bcolors.ENDC}|")

def Yellow_Phase():
    light_1_red_off = True
    light_1_yellow_off = False
    light_1_green_off = True

    light_1_red_on = False
    light_1_yellow_on = True
    light_1_green_on = False

    print("Car:")
    print("             | |")
    print(f"             |{bcolors.WARNING}o{bcolors.ENDC}|")
    print("             | |")

def Red_Phase():
    light_1_red_off = False
    light_1_yellow_off = True
    light_1_green_off = True

    light_1_red_on = True
    light_1_yellow_on = False
    light_1_green_on = False

    print("Car:")
    print(f"             |{bcolors.FAIL}o{bcolors.ENDC}|")
    print("             | |")
    print("             | |")

def Red_Phase_Pedestrian():
    ped_red_off = False
    ped_green_off = True

    ped_red_on = True
    ped_green_on = False

    print("Pedestrian:")
    print(f"             |{bcolors.FAIL}o{bcolors.ENDC}|")
    print("             | |")

def Green_Phase_Pedestrian():
    ped_red_off = True
    ped_green_off = False

    ped_red_on = False
    ped_green_on = True

    print("Pedestrian:")
    print("             | |")
    print(f"             |{bcolors.OKGREEN}o{bcolors.ENDC}|")

while True:
    Green_Phase()
    Red_Phase_Pedestrian()
    ped_switch_1 = input("Press (1) to switch: ")
    time.sleep(2)

    Yellow_Phase()
    Red_Phase_Pedestrian()
    time.sleep(2)

    Red_Phase()
    Green_Phase_Pedestrian()
    time.sleep(2)