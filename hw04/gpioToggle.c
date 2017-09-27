// From : http://stackoverflow.com/questions/13124271/driving-beaglebone-gpio-through-dev-mem
//
// Be sure to set -O3 when compiling.
// Modified by Mark A. Yoder  26-Sept-2013
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "beaglebone_gpio.h"
#include <signal.h>    // Defines signal-handling functions (i.e. trap Ctrl-C)

#define BUTTON1 (1<<17)
#define BUTTON2 (1<<25)
/****************************************************************
 * Global variables
 ****************************************************************/
int keepgoing = 1;    // Set to 0 when ctrl-c is pressed

/****************************************************************
 * signal_handler
 ****************************************************************/
void signal_handler(int sig);
// Callback called when SIGINT is sent to the process (Ctrl-C)
void signal_handler(int sig)
{
	printf( "\nCtrl-C pressed, cleaning up and exiting...\n" );
	keepgoing = 0;
}
int main(int argc, char *argv[]) {
    volatile void *gpio1_addr;
    volatile unsigned int *gpio1_oe_addr;
    volatile unsigned int *gpio1_setdataout_addr;
    volatile unsigned int *gpio1_cleardataout_addr;
    volatile void *gpio0_addr;
    volatile unsigned int *gpio0_oe_addr;
    volatile unsigned int *gpio0_datain;

    unsigned int reg;
    
    // Set the signal callback for Ctrl-C
	signal(SIGINT, signal_handler);

    int fd = open("/dev/mem", O_RDWR);

    //setup GPIO1
    printf("Mapping %X - %X (size: %X)\n", GPIO1_START_ADDR, GPIO1_END_ADDR, GPIO1_SIZE);

    gpio1_addr = mmap(0, GPIO1_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO1_START_ADDR);

    gpio1_oe_addr           = gpio1_addr + GPIO_OE;
    gpio1_setdataout_addr   = gpio1_addr + GPIO_SETDATAOUT;
    gpio1_cleardataout_addr = gpio1_addr + GPIO_CLEARDATAOUT;

    if(gpio1_addr == MAP_FAILED) {
        printf("Unable to map GPIO1\n");
        exit(1);
    }
    printf("GPIO mapped to %p\n", gpio1_addr);
    printf("GPIO OE mapped to %p\n", gpio1_oe_addr);
    printf("GPIO SETDATAOUTADDR mapped to %p\n", gpio1_setdataout_addr);
    printf("GPIO CLEARDATAOUT mapped to %p\n", gpio1_cleardataout_addr);

    //setup GPIO0
    printf("Mapping %X - %X (size: %X)\n", GPIO0_START_ADDR, GPIO0_END_ADDR, GPIO0_SIZE);

    gpio0_addr = mmap(0, GPIO0_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO0_START_ADDR);

    gpio0_oe_addr  = gpio0_addr + GPIO_OE;
    gpio0_datain = gpio0_addr + GPIO_DATAIN;

    if(gpio0_addr == MAP_FAILED) {
        printf("Unable to map GPIO0\n");
        exit(1);
    }
    printf("GPIO mapped to %p\n", gpio0_addr);
    printf("GPIO OE mapped to %p\n", gpio0_oe_addr);
    printf("GPIO DATAIN mapped to %p\n", gpio0_datain);
    // Set up GPIO1 I/O
    reg = *gpio1_oe_addr;
    printf("GPIO1 configuration: %X\n", reg);
    reg &= ~USR3;       // Set USR3 bit to 0
    reg &= ~USR2;       // Set USR2 bit to 0
    *gpio1_oe_addr = reg;
    // Set up GPIO0 I/O
    reg = *gpio0_oe_addr;
    printf("GPIO0 configuration: %X\n", reg);
    reg &= BUTTON1;       // Set button1 bit to 1
    reg &= BUTTON2;       // Set button2 bit to 1
    *gpio0_oe_addr = reg;
    printf("Start blinking LED USR2/3\n");
    while(keepgoing) {
        reg = *gpio0_datain;
        printf("GPIO0 values: %X\n",reg);
        // printf("ON\n");
        *gpio1_setdataout_addr = USR3;
        *gpio1_cleardataout_addr = USR2;
        usleep(250000);
        // printf("OFF\n");
        *gpio1_cleardataout_addr = USR3;
        *gpio1_setdataout_addr = USR2;
        usleep(250000);
    }
    close(fd);
    return 0;
}
