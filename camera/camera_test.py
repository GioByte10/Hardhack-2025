# This is a basic program that illustrates a few ways
# to take pictures and store them directly to file

import picamera
import time

# Initialize the camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25

# This line is optional; if you need to rotate the image
camera.rotation = 180              

# Start the camera preview (so we can see what we are taking pictures of)
# If you are accessing the RPi through VNC, you need to "activate the direct capture mode"
# (right-click on the VNC icon on the RPi, select "Options" and then "Troubleshooting" and then enable 
camera.start_preview()

# Sleep at least 2 seconds to give the sensor time to settle
time.sleep(2)                       


# Option 1 - Take a single image and store it to file
camera.capture('image_option1.jpg')
time.sleep(1)                       


# Option 2 - Take a single image and store it to a pre-opened file
#            This is essentially the same as option 1
#            It also demonstrates automatic resizing
myfile = open('image_option2.jpg','wb')
camera.capture(myfile, resize = (320,240))
myfile.close()
time.sleep(1)


# Option 3 - Take a set of consecutive images every second and store them to file
for i in range(2):
    camera.capture('image_option3_%s.jpg' % i)
    time.sleep(1)


# Stop the camera preview
camera.stop_preview()

# Clean up the camera resources
camera.close()
