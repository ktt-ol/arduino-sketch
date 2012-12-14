/*
* opens and closes tty with 1200 baud to reset a leonardo
*/
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>

int main(int argc, char **argv) {
    int fd;
    struct termios attribs;

    if (argc != 2) {
        fprintf(stderr, "usage: %s /dev/tty.usbmodem000\n", argv[0]);
        return EXIT_FAILURE;
    }

    fd = open(argv[1], O_RDWR | O_NONBLOCK);
    if (fd == -1) {
        perror("could not open term");
        return EXIT_FAILURE;
    }

    if(!isatty(fd)) {
        perror("ERROR: not a tty");
        return EXIT_FAILURE;
    }

    if(tcgetattr(fd, &attribs) < 0) {
        perror("ERROR: could not read term attributes");
        return EXIT_FAILURE;
    }

    if(cfsetispeed(&attribs, B1200) < 0 || cfsetospeed(&attribs, B1200) < 0) {
        perror("ERROR: could not set speed");
        return EXIT_FAILURE;
    }

    if (tcsetattr(fd, TCSANOW, &attribs) < 0) {
        perror("could not set term");
        return EXIT_FAILURE;
    }

    close(fd);

    return EXIT_SUCCESS;
}
