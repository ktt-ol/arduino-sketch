import os
import sys
from collections import defaultdict

class ArduinoBoards(object):
    def __init__(self, boards_file):
        self.boards_file = boards_file
        self._parse()

    def _parse(self):
        boards = defaultdict(dict)
        with open(self.boards_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if '.' not in line or '=' not in line:
                    print >>sys.stderr, "found invalid line:", line

                name, option = line.split('.', 1)
                key, val = option.split('=')
                boards[name][key] = val
        self.boards = dict(boards)

    def list(self):
        print "%-13s%s" % ("Tag", "Board Name")
        for k in sorted(self.boards.keys()):
            print "%-13s%s" % (k, self.boards[k]['name'])

    def set_board_environ(self, board_name):
        options = {
            'MCU': 'build.mcu',
            'F_CPU': 'build.f_cpu',
            'VARIANT': 'build.variant',
            'AVRDUDE_ARD_PROGRAMMER': 'upload.protocol',
            'AVRDUDE_ARD_BAUDRATE': 'upload.speed',
            'ISP_LOCK_FUSE_PRE': 'bootloader.unlock_bits',
            'ISP_LOCK_FUSE_POST': 'bootloader.lock_bits',
            'ISP_HIGH_FUSE': 'bootloader.high_fuses',
            'ISP_LOW_FUSE': 'bootloader.low_fuses',
            'ISP_EXT_FUSE': 'bootloader.extended_fuses',
        }
        board = self.boards[board_name]
        for key, board_option in options.iteritems():
            os.environ[key] = board[board_option]

if __name__ == '__main__':
    boards = ArduinoBoards('/usr/share/arduino/hardware/arduino/boards.txt')
    boards.list()
