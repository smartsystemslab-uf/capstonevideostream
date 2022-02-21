# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import sys
# https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/
import subprocess as sp
import time
from uuid import getnode as get_mac


# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen

HD = [3840, 2160]
SD = [1280, 720] 
UHD = [1920, 1080] 
VGA = [640, 480] 
RESOLUTION = SD

def gstreamer_pipeline(
    capture_width=RESOLUTION[0],
    capture_height=RESOLUTION[1],
    display_width=RESOLUTION[0],
    display_height=RESOLUTION[1],
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def main(args=None):

    if args is not None:
        capstream = CaptureStream(args.cz_filename.name, args.vflip, args.hflip)
    else:
        # raise RuntimeError("There is no argumentls")
        capstream = CaptureStream("")
    capstream.start()


class CaptureStream:

    def __init__(self, cz_filename, vflip=False, hflip=False):
        self.running = False
        self.time_interval = 5
        self.cz_filename = cz_filename

        # Flip method
        # 0: identity - no rotation (default) 
        # 1: counterclockwise - 90 degrees
        # 2: rotate - 180 degrees
        # 3: clockwise - 90 degrees 
        # 4: horizontal flip 
        # 5: upper right diagonal flip
        # 6: vertical flip 
        # 7: upper-left diagonal
        self.flip_code = 0
        if (vflip and hflip):
            self.flip_code = 5
        elif vflip:
            self.flip_code = 6
        elif hflip:
            self.flip_code = 4

    def start(self):

        # HD: 1920 x 1080
        # SD: 1280 x 720
        mac_addr = get_mac()
        mac_addr = ''.join(("%012X" % mac_addr)[i:i + 2] for i in range(0, 12, 2))

        server_addr = "192.168.1.11"

        ffmpeg_path = 'ffmpeg'
        output_file = "rtsp://" + server_addr + ":554/flvplayback"
        metadata = "title=test" + mac_addr


        nb_attempts = 0

        while nb_attempts < 5:

            print(gstreamer_pipeline(flip_method=self.flip_code))
            cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=self.flip_code), cv2.CAP_GSTREAMER)
            if cap.isOpened():
                ret, frame = cap.read()
                nb_attempts = 0
            else: 
                nb_attempts += 1
                continue

            height, width, ch = frame.shape

            
            dimension = '{}x{}'.format(width, height)
            f_format = 'bgr24' # remember OpenCV uses bgr format
            fps = str(cap.get(cv2.CAP_PROP_FPS))

            # Use this link to tune ffmpeg param
            # https://trac.ffmpeg.org/wiki/Encode/H.264
            # https://superuser.com/questions/490683/cheat-sheets-and-presets-settings-that-actually-work-with-ffmpeg-1-0

            ffmpeg_cmd = [ffmpeg_path,
                '-y',
                '-f', 'rawvideo',
                '-vcodec','rawvideo',
                '-s', dimension,
                '-pix_fmt', f_format,
                '-r', fps,
                '-i', '-',
                '-an',
                "-vcodec", "libx264", 
                # "-crf", "24", # Default: 23
                "-preset", "ultrafast",
                '-f', 'rtsp',
                '-metadata', metadata,
                output_file]
            print("the commandline is[ffmpeg_cmd]: {}".format(ffmpeg_cmd))

            # ffmpeg_proc = sp.Popen(ffmpeg_cmd, stdin=sp.PIPE, stdout=sp.DEVNULL, stderr=sp.DEVNULL, shell=True, bufsize=100)
            ffmpeg_proc = sp.Popen(ffmpeg_cmd, stdin=sp.PIPE, stdout=sp.DEVNULL, stderr=sp.DEVNULL, bufsize=10)
            
            while True:
            
                ret, frame = cap.read()                    
                if ret:
                    ffmpeg_proc.stdin.write(frame.tostring())
                else:
                    break

            cap.release()
            ffmpeg_proc.stdin.close()
            ffmpeg_proc.stderr.close()
            try:
                ffmpeg_proc.wait(self.time_interval) # Wait 5 seconds
            finally:
                ffmpeg_proc.terminate()

            nb_attempts += 1


if __name__ == "__main__":
    import fcntl, sys
    pid_file = 'capstone-77e7c7ee-fe6b-49f5-825e-9fa3eca8700e.pid'
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print('Another Instance is running')
        # another instance is running
        sys.exit(0)

    main()
