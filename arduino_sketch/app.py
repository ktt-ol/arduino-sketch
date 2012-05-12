import os
import sys
from glob import glob
import optparse
import subprocess

def last_sketch(sketch):
    last = None
    if os.path.exists('.last_sketch'):
        last = open('.last_sketch').read().strip()

    open('.last_sketch', 'w').write(sketch)

    return last

def list_sketches():
    for sketch in glob('*.ino'):
        print sketch[:-len('.ino')]

def build(sketch, upload=False):
    makefile = os.path.join(os.path.dirname(__file__), 'Arduino.mk')
    if last_sketch(sketch) != sketch:
        subprocess.call(['make', '-f', makefile, 'clean_local'])


    cmd = ['make', '-f', makefile, 'all']
    if upload:
        cmd.append('upload')
    subprocess.call(cmd)

makefile = os.path.join(os.path.dirname(__file__), 'Arduino.mk')

def clean():
    cmd = ['make', '-f', makefile, 'clean']
    subprocess.call(cmd)

def init_env(sketch):
    os.environ['ARDUINO_DIR'] = '../Arduino.app/Contents/Resources/Java'
    os.environ['SKETCH'] = sketch
    os.environ['ARDUINO_PORT'] = '/dev/cu.usb*'


def main():
    parser = optparse.OptionParser()
    parser.add_option('-l', '--list', '--list-sketches',
        dest='list_sketches', default=False, action='store_true')

    parser.add_option('-u', '--upload',
        dest='upload', default=False, action='store_true')

    parser.add_option('-c', '--clean',
        dest='clean', default=False, action='store_true')

    options, args = parser.parse_args()

    if options.list_sketches:
        list_sketches()
        sys.exit(0)

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    sketch = args[0]
    if sketch.endswith('.ino'):
        sketch = sketch[:-len('.ino')]

    init_env(sketch)

    if options.clean:
        clean()

    build(sketch, upload=options.upload)

if __name__ == '__main__':
    main()