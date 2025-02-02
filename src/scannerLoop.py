
import picamera
import picamera.array
import cv2
import time
import numpy as np
import RPi.GPIO as GPIO
import time

from readBarcode import readBarcodes
from dbUpdate import updateDatabase

updates = db.reference('storage/user1').get()
print(updates)

GPIO.setmode(GPIO.BCM)

TOGGLE_PIN = 27
GPIO.setup(TOGGLE_PIN, GPIO.IN, pull_up_down=GPIO.pud_up)

# set camera attributes
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25
camera.vflip = True
camera.hflip = True

INSERT = 1
DELETE = 0

LOCKOUT_TIME = 60 # in seconds


# map code -> time added
# every n minutes, check curr - time_added > some time in minutes and delete 
lockoutDict = {}
# Sweeps for locked out codes which are timed out (existed for more than LOCKOUT_TIME seconds)
def sweepLockout(lockoutDict):
    for k,v in lockoutDict.items():
        if time.time - v > LOCKOUT_TIME:
            del lockoutDict[k]

# cache for codes we've seen before. contains {code: productName}
cache = {}

def isValidCode(code):
    if code in cache:
        return cache[code]
    else:
        # TODO perform an API call
        return ...
        

# forever loop of a barcode scanner. 
def beginBarcodeScanner():
    rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))
    # main loop
    while True:
        try:
            time.sleep(0.1)
            for frame in camera.capture_continuous(rawframe, format='bgr', use_video_port=True):
                image = frame.array
                :with expression as target:
                    passsweepLockout(lockoutDict)
                codes = readBarcodes(image);
                # for every code we scanned in the image, try and validate
                for code in codes:

                    # TODO: database check via our scraper, AND check if lockout
                    productName = isValidCode(code)
                    # if product name is None, then this if fails
                    if productName:
                        # TODO: beep or indicate it was scanned
                        # add code to the lockout
                        lockoutDict.update({code: time.time})
                        updateDatabase(updates, "MAIN_TEST_ID", "MAIN_TEST_NAME", "TODAY", GPIO.input(TOGGLE_PIN) == INSERT)
                
                # clear buffer (because we've been acumulating due to the API call)
                 camera.close()
                # begin camera capture again, and re-set the pointer to frame
                frame = camera.capture_continuous(rawframe, format='bgr', use_video_port=True)

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
