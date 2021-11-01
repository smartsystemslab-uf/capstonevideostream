# https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/
import subprocess as sp
import time
from uuid import getnode as get_mac

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
        self.time_interval = 5  # number of second between two lux value
        self.fps = '30'
        self.cz_filename = cz_filename

        self.flip_code = None
        if (vflip and hflip):
            self.flip_code = -1
        elif vflip:
            self.flip_code = 0
        elif hflip:
            self.flip_code = 1

    def start(self):

        # HD: 1920 x 1080
        # SD: 1280 x 720
        mac_addr = get_mac()
        mac_addr = ''.join(("%012X" % mac_addr)[i:i + 2] for i in range(0, 12, 2))
        rasp_cmd = "raspivid -w 1280 -h 720 -fps 25 -b 10000000 -vf -hf -t 0 -o - "

        server_addr = "192.168.0.2"
        ffmpeg_cmd = "ffmpeg -i - -vcodec copy -an -f rtsp -metadata title=test" + mac_addr + " rtsp://" + server_addr + ":554/flvplayback "

        print("the commandline is[rasp_cmd]: {}".format(rasp_cmd))
        print("the commandline is[ffmpeg_cmd]: {}".format(ffmpeg_cmd))
        nb_attempts = 0

        while nb_attempts < 5:
            ffmpeg_proc = sp.Popen(ffmpeg_cmd, stdin=sp.PIPE, stdout=sp.DEVNULL, stderr=sp.DEVNULL, shell=True)
            rasp_proc = sp.Popen(rasp_cmd, stdin=None, stdout=ffmpeg_proc.stdin, stderr=sp.DEVNULL, shell=True)

            # Wait while the two processes still alive
            while rasp_proc.poll() is None and ffmpeg_proc.poll() is None:
                try:
                    time.sleep(5)
                finally:
                    pass

            try:
                time.sleep(0.2)
            finally:
                rasp_proc.terminate()
                ffmpeg_proc.terminate()
                try:
                    out, err = rasp_proc.communicate(timeout=0.5)
                    print('== subprocess exited with rc =', rasp_proc.returncode)
                    print(out.decode('utf-8'))
                except sp.TimeoutExpired:
                    print('subprocess did not terminate in time')
                    break
            out, err = rasp_proc.communicate()
            print("OutPut Message: {}".format(out))
            print("OutPut Error : {}".format(err))
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
