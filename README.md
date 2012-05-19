arduino-sketch
==============

`arduino-sketch` lets you compile and upload Arduino Sketches without the IDE. Just use your favorite editor to write the Arduino `.ino` files and call `arduino-sketch my.ino -u`.


Usage
-----

`arduino-sketch my.ino` will compile the `my.ino` file. It remembers the name of your sketch, so you can just call `arduino-sketch` the next time. 






Configuration
-------------

`arduino-sketch` uses local configuration (`.arduino_sketch`) and a user configuration (`~/.arduino_sketch`). Some configuration options are:

`arduino_dir`:
    Path to the Arduino core directory. Should contain the `hardware` and `tools` directory.

`avr_tools_path`:
    Path to `avr-xxx` binaries.

`arduino_port`:
    The Arduino serial device.
    Defaults to `/dev/cu.usb*`, but this will only work if you have a single USB serial device attached.

`board_tag`:
    The name/type of the Arduino. See `--list-boards` and `--board` options.


Install
-------

arduino-sketch is [registered at the Python Package Index (PyPi)](http://pypi.python.org/pypi/arduino-sketch), so you can install it with `pip` or `easy_install`.

For example on Debian:

    sudo aptitude install python-pip
    sudo pip install arduino-sketch

To uninstall:

    sudo pip uninstall arduino-sketch

License
-------

arduino-sketch is licensed under the MIT license.
It ships with Arduino.mk and ard-parse-boards which are licensed under LGPL 2.1.
