from apis import readBarcodes, find_item
import picamera
import picamera.array
import time

camera = picamera.PiCamera()
camera.resolution = (800, 800)
camera.framerate = 25


rawframe = picamera.array.PiRGBArray(camera, size = camera.resolution)

try:
	time.sleep(0.1)
	for frame in camera.capture_continuous(rawframe, format = 'bgr', use_video_port = True):
		image = frame.array
		
		upcs = readBarcodes(image, debug = True)
		print(upcs)
		for upc in upcs:
			name = find_item(upc)
			print(upc, name)
		
		rawframe.truncate(0)

except Exception as e:
	print(e)
