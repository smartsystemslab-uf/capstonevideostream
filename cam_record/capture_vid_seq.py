# sudo apt-get install -y gpac
# convert h264 to mp4 with the following commandline
# MP4Box -fps 30 -add video.h264 video.mp4

import picamera

# camera = picamera.PiCamera(resolution=(640, 480))
camera = picamera.PiCamera(resolution=(1280, 960))
for filename in camera.record_sequence(
        '%d.h264' % i for i in range(1, 6)):
    print('Recording: %s' % filename)
    camera.wait_recording(30) # record 30 seconds

