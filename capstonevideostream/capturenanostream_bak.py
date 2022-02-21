# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2

import subprocess as sp
import sys

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


def show_camera():
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        # window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_NORMAL)
        # Window
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            ret_val, img = cap.read()
            # cv2.setWindowProperty("CSI Camera", cv2.WND_PROP_FULLSCREEN, cv2.CV_WINDOW_FULLSCREEN)
            cv2.imshow("CSI Camera", img)
            # This also acts as
            keyCode = cv2.waitKey(30) & 0xFF
            # Stop the program on the ESC key
            if keyCode == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    # show_camera()


    # # input_file = 'input_file_name.mp4'
    # output_file = 'output_file_name.mp4'

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        ret, frame = cap.read()
    else: sys.exit()

    height, width, ch = frame.shape

    ffmpeg = 'ffmpeg'
    dimension = '{}x{}'.format(width, height)
    f_format = 'bgr24' # remember OpenCV uses bgr format
    fps = str(cap.get(cv2.CAP_PROP_FPS))

    output_file = 'rtsp://192.168.1.11:554/flvplayback'

    # ffmpeg -i output_file_name.mp4 -vcodec libx264 -an -f rtsp -metadata title=test1234 rtsp://192.168.1.11:554/flvplayback

    # command = [ffmpeg,
    #         '-y',
    #         '-f', 'rawvideo',
    #         '-vcodec','rawvideo',
    #         '-s', dimension,
    #         '-pix_fmt', 'bgr24',
    #         '-r', fps,
    #         '-i', '-',
    #         '-an',
    #         '-vcodec', 'mpeg4',
    #         '-b:v', '5000k',
    #         output_file ]

    command = [ffmpeg,
            '-y',
            '-f', 'rawvideo',
            '-vcodec','rawvideo',
            '-s', dimension,
            '-pix_fmt', 'bgr24',
            '-r', fps,
            '-i', '-',
            '-an',
            "-vcodec", "libx264", 
            # "-crf", "0", 
            "-preset", "ultrafast",
            '-f', 'rtsp',
            '-metadata', 'title=test1234',
            output_file]

    print("full command: ", command)

    # proc = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE, bufsize=10)
    proc = sp.Popen(command, stdin=sp.PIPE, stdout=sp.DEVNULL, stderr=sp.STDOUT, bufsize=100)

    while True:
            
        ret, frame = cap.read()
            
        # ret, frame = cap.read()
        if not ret:
            print("proc.stderr: ", proc.stderr, " - proc.stdout", proc.stdout, " - proc.stdin", proc.stdin)
            break
        else:
            proc.stdin.write(frame.tostring())
            # try:
            #     proc.write(frame.tostring())
            # finally:
            #     print("proc.stderr: ", proc.stderr, " - proc.stdout", proc.stdout, " - proc.stdin", proc.stdin)
            #     break

    # print("proc.stderr: ", proc.stderr)
    cap.release()
    proc.stdin.close()
    proc.stderr.close()
    proc.wait()








