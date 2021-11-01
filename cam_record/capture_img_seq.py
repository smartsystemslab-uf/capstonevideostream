from time import sleep
from picamera import PiCamera

maximg = 10 # capture 10 images
camera = PiCamera()
camera.start_preview()
sleep(2)
for i, filename in enumerate(camera.capture_continuous('img{counter:03d}.jpg')):
    print('Captured (%03d): %s' % (i+1, filename))
    sleep(3) # wait 3 seconds
    if i == (maximg-1):
        break


