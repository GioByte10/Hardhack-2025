
import picamera
import picamera.array
import cv2
import time
import numpy as np
import RPi.GPIO as GPIO
import time

from apis import readBarcodes
from firebase_admin import db
from dbUpdate import updateDatabase

ref = db.reference('storage/user3')
updates = ref.get()


GPIO.setmode(GPIO.BCM)

TOGGLE_PIN = 17
BUZZER_PIN = 27
GPIO.setup(TOGGLE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# set camera attributes
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25
camera.vflip = True
camera.hflip = True

INSERT = 1
DELETE = 0

LOCKOUT_TIME = 5 # in seconds

BUZZER_TIME = 0.5 ## in  seconds


# map code -> time added
# every n minutes, check curr - time_added > some time in minutes and delete 
lockoutDict = {}
# Sweeps for locked out codes which are timed out (existed for more than LOCKOUT_TIME seconds)
def sweepLockout(lockoutDict):
    to_delete = []
    for k,v in lockoutDict.items():
        if time.time() - v > LOCKOUT_TIME:
            to_delete.append(k)
    
    if to_delete:
        print(f'deleting {to_delete} from lockout')
    for x in to_delete:
        del lockoutDict[x]
    
# cache for codes we've seen before. contains {code: productName}
cache = {'0071142915361': {'name': 'Arrowhead 100% Moutain Water', 'type': 'Drink'}, '0085239049457': {'name': 'Granny Smith Apples', 'type': 'Produce'}, '0611269991000': {'name': 'Red Bull Original Energy Drink, 8.4 Oz., 24/Carton (RBD99124)', 'type': 'Drink'}, '0028400516914': {'name': 'Ruffles Potato Chips Cheddar & Sour Cream Flavored - 8 Oz', 'type': 'Snack'}, '0810291001002': {'name': "Tate's Bake Shop Cookies Chocolate Chip 7 Oz", 'type': 'Snack'}, '0085239156834': {'name': 'Peanut Butter Chocolate Trail Mix - 8oz - Favorite Day™', 'type': 'Snack'}, '0028400043809': {'name': 'Lays Wavy Regular Potato Chips - 7.75 Oz', 'type': 'Snack'}, '0012000001291': {'name': 'Pepsi Cola Soda - 20 Fl Oz Bottle', 'type': 'Drink'}, '0765756931199': {'name': 'Raspberry-Pi Rpi4-Modbp-8Gb Raspberry Pi 4 Model B, Cortex-A72, 8Gb', 'type': 'Snack'}, '0082592720641': {'name': 'Naked Juice  Green Machine  64 Fl Oz Bottle', 'type': 'Drink'}, '0014100079477': {'name': 'Pepperidge Farm Milano Mint Chocolate Cookies - 7 Oz', 'type': 'Snack'}, '0632565000036': {'name': 'BG12984  Artesian Water - 12x1.5 Ltr', 'type': 'Drink'}, '0602652271465': {'name': 'KIND Gluten Free Bar Dark Chocolate Almond & Coconut 6 Bars', 'type': 'Snack'}, '0611269001945': {'name': 'Red Bull Green Edition Energy Drink - Curuba Elderflower, 80mg Caffeine, 8.4 Fl Oz', 'type': 'Drink'}, '0044000051051': {'name': 'RITZ Toasted Chips Sour Cream and Onion Crackers, 8.1 Oz | CVS', 'type': 'Snack'}, '0025293600393': {'name': 'Silk Soymilk, Original - 0.5 Gl', 'type': 'Drink'}}


def isValidCode(code):
    if code in cache:
        return cache[code]['name'],cache[code]['type']  # returns a dict object {name:name,category:category}
    else:
        # TODO perform an API call
        return "trash", "GARBAGE"
        

# forever loop of a barcode scanner. 
def beginBarcodeScanner():
    rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))
    # main loop

    while True:
        try:
            time.sleep(0.1)
            buzzerTimer = 0
            pwm = GPIO.PWM(BUZZER_PIN,440)
            pwm.start(0)
            for frame in camera.capture_continuous(rawframe, format='bgr', use_video_port=True):
                image = frame.array
                sweepLockout(lockoutDict)
                codes = readBarcodes(image)
                # for every code we scanned in the image, try and validate
                #rint(f'code len: {len(codes)}')
                for code in codes:
                    #  database check via our scraper, AND check if lockout
                    productName,catType = isValidCode(code)
                    # if product name is None, then this if failsf
                    if code not in lockoutDict:
                        print(code)
                        
                        # GPIO.output(BUZZER_PIN,GPIO.HIGH)
                        pwm.start(75)
                        buzzerTimer = time.time()
                        # lockoutDict.update({code: time.time()})
                        lockoutDict[code] = time.time()
                        updateDatabase(ref, updates, code, productName, time.strftime("%Y-%m-%d %H:%M:%S"),catType, GPIO.input(TOGGLE_PIN) == INSERT)
                        print(updates,ref.get())
                        
                if time.time() - buzzerTimer >= BUZZER_TIME:
                    buzzerTimer = 0
                    pwm.start(0)
                    
                rawframe.truncate(0)

        except KeyboardInterrupt:
            print("Ctrl + C called")
            cv2.destroyAllWindows()
            GPIO.cleanup()
            camera.close()
            quit()

if __name__ == "__main__": 
    print("beginning barcode scanner loop!")
    # print("")
    beginBarcodeScanner()
