import os
import termios

def reset(device):
    fd = os.open(device, os.O_RDWR | os.O_NONBLOCK)

    if not os.isatty(fd):
        raise ValueError('device not a tty: %s' % device)

    # attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    attr = termios.tcgetattr(fd)
    attr[4] = attr[4] | termios.B1200
    attr[5] = attr[5] | termios.B1200

    termios.tcsetattr(fd, termios.TCSANOW, attr)

    os.close(fd)

if __name__ == '__main__':
    import sys
    if len(sys.argv) <= 1:
        print >>sys.stderr, "Usage: %s /dev/tty.usbmodem" % sys.argv[0]
    else:
        reset(sys.argv[1])
