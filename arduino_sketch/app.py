# Copyright (c) 2012,2013 Oliver Tonnhofer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import with_statement
import os
import time
import sys
from glob import glob
import optparse
import subprocess
import multiprocessing
import ConfigParser

from arduino_sketch.boards import ArduinoBoards
from arduino_sketch.reset import reset


MAKEFILE = os.path.join(os.path.dirname(__file__), 'Arduino.mk')
LOCAL_CONF_PATH = '.arduino_sketch'
USER_CONF_PATH = '~/.arduino_sketch'
INI_SECTION = 'arduino-sketch'

class DefaultValue(str):
    pass

class SketchConf(dict):
    @classmethod
    def from_ini(cls, ini_file, load_defaults=True):
        conf = ConfigParser.ConfigParser()
        conf.read(ini_file)
        if not conf.has_section(INI_SECTION):
            sketch_conf = cls()
        else:
            sketch_conf = cls(conf.items(INI_SECTION))

        if load_defaults:
            sketch_conf.fill_defaults()
        return sketch_conf

    def write_ini(self, ini_file):
        conf = ConfigParser.ConfigParser()
        conf.add_section(INI_SECTION)
        for k, v in self.iteritems():
            if not isinstance(v, DefaultValue):
                conf.set(INI_SECTION, k, v)
        with open(ini_file, 'w') as f:
            conf.write(f)

    def fill_defaults(self):
        user_defaults = SketchConf.from_ini(
            os.path.expanduser(USER_CONF_PATH), load_defaults=False)
        for k, v in user_defaults.iteritems():
            if k not in self:
                self[k] = DefaultValue(v)

        for platform in [sys.platform, 'other']:
            app_default_file = os.path.join(os.path.dirname(__file__), 'defaults_%s.ini' % platform)
            if os.path.exists(app_default_file):
                app_defaults = SketchConf.from_ini(
                    app_default_file, load_defaults=False)
                for k, v in app_defaults.iteritems():
                    if k not in self:
                        self[k] = DefaultValue(v)
                break

def boards(conf):
    return ArduinoBoards(os.path.join(conf['arduino_dir'], 'hardware', 'arduino', 'boards.txt'))

def list_sketches():
    for sketch in glob('*.ino'):
        print sketch[:-len('.ino')]

def clean_ino(conf):
    subprocess.call(['make', '-f', MAKEFILE, 'clean_ino'])

def list_boards(conf):
    boards(conf).list()

def build(conf, upload=False):
    cmd = ['make', '-j%d' % multiprocessing.cpu_count(), '-f', MAKEFILE, 'all']
    subprocess.call(cmd)
    if upload:
        if conf['board_tag'] == 'leonardo':
            reset_port(conf)
            time.sleep(2)
        cmd = ['make', '-f', MAKEFILE, 'upload']
        subprocess.call(cmd)

def reset_port(conf):
    arduino_port = glob(conf['arduino_port'])[0]
    print 'resetting leonardo', arduino_port
    reset(arduino_port)

def clean(conf):
    cmd = ['make', '-f', MAKEFILE, 'clean']
    subprocess.call(cmd)

def init_env(conf):
    for k, v in conf.iteritems():
        os.environ[k.upper()] = v
    os.environ['OBJDIR'] = os.path.join(os.curdir, 'build-' + conf['board_tag'])

def init_board_env(conf):
    boards(conf).set_board_environ(conf['board_tag'])

def main():
    parser = optparse.OptionParser()
    parser.add_option('-l', '--list', '--list-sketches',
        dest='list_sketches', default=False, action='store_true')
    parser.add_option('-u', '--upload',
        default=False, action='store_true')
    parser.add_option('-c', '--clean',
        default=False, action='store_true')
    parser.add_option('--list-boards',
        default=False, action='store_true')
    parser.add_option('--board',
        help='Arduino board tag, see --list-boards')
    parser.add_option('--port',
        help='the serial port for uploading (e.g. /dev/ttyUSB0)')


    options, args = parser.parse_args()

    if options.list_sketches:
        list_sketches()
        sys.exit(0)


    conf = SketchConf.from_ini(LOCAL_CONF_PATH)

    if options.list_boards:
        list_boards(conf)
        sys.exit(0)


    if len(args) == 1:
        sketch = args[0]
    elif 'sketch' in conf:
        sketch = conf['sketch']
    else:
        parser.print_help()
        sys.exit(1)

    if sketch.endswith('.ino'):
        sketch = sketch[:-len('.ino')]

    if not os.path.exists(sketch + '.ino'):
        print >>sys.stderr, "ERROR: sketch not found %s" % sketch
        sys.exit(2)

    if options.board:
        conf['board_tag'] = options.board

    if options.port:
        conf['arduino_port'] = options.port

    init_env(conf)
    init_board_env(conf)


    if options.clean:
        clean(conf)
        sys.exit(3)
    elif sketch != conf.get('sketch'):
        # name of sketch changed, remove compiled .ino files
        clean_ino(conf)

    build(conf, upload=options.upload)

    conf['sketch'] = sketch
    conf.write_ini(LOCAL_CONF_PATH)
