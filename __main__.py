from capstonevideostream.capturestream import main


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType

    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-w", "--width",
                        dest="width",
                        default=640,
                        type=int,
                        help="Set image width <size>")
    parser.add_argument("-he", "--height",
                        dest="height",
                        default=480,
                        type=int,
                        help="Set image height <size>")
    parser.add_argument("-b", "--bitrate",
                        dest="bitrate",
                        default=1000000,
                        type=int,
                        help="Set bitrate. Use bits per second (e.g. 10MBits/s would be -b 10000000)")
    parser.add_argument("-fps", "--framerate",
                        dest="framerate",
                        default=30,
                        type=int,
                        help="Specify the frames per second to record")
    parser.add_argument("-t", "--time",
                        dest="time",
                        default=0,
                        type=int,
                        help="Set duration of stream in millisecond")
    parser.add_argument("-ex", "--exposure",
                        dest="exposure",
                        default="auto",
                        choices=['auto', 'night', 'nightpreview', 'backlight', 'spotlight', 'sports',
                                 'snow', 'beach', 'verylong', 'fixedfps', 'antishake', 'fireworks'],
                        help="Set exposure mode (see Notes)")
    parser.add_argument("-awb", "--awb",
                        dest="awb",
                        default="auto",
                        choices=['off', 'auto', 'sun', 'cloud', 'shade', 'tungsten',
                                 'fluorescent', 'incandescent', 'flash', 'horizon'],
                        help="Set AWB mode (see Notes)")
    parser.add_argument("-ISO", "--ISO",
                        dest="ISO",
                        default=200,
                        type=int,
                        help="Set capture ISO")
    parser.add_argument("-hf", "--hflip",
                        action="store_true",
                        dest="hflip",
                        help="Set horizontal flip")
    parser.add_argument("-vf", "--vflip",
                        action="store_true",
                        dest="vflip",
                        help="Set vertical flip")

    parser.add_argument("-czp", "--cam_zone_path",
                        dest="cz_filename",
                        default="/var/www/html/securitrixcam/cgi-dir/camera/camera-cfg.json",
                        type=FileType('r'),
                        help="Set path of json config file to read zone")

    # parser.add_argument("-csv", "--lux_value_csv_path",
    #                     dest="lux_value_csv_path",
    #                     default="/var/www/html/securitrixcam/download/csv_file/data.csv",
    #                     type=FileType('r'),
    #                     help="Set path of csv output lux value")

    # parser.add_argument("-pjson", "--position_json_obj",
    #                     dest="pjson",
    #                     default=9,
    #                     type=int,
    #                     help="Set the position of the object in json array in the filename")

    # parser.add_argument("-ddlz","--ddraw_lux_zone",
    #                     dest="ddraw_lux_zone",
    #                     action="store_true" ,
    #                     default=False,
    #                     help="Disable draw the lux meter zone on image ")
    return parser


if __name__ == '__main__':

    arguments, unknown = get_parser().parse_known_args()
    print(unknown)
    main(arguments)
