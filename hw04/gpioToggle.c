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
    volatile void *gpio2_addr;
    volatile unsigned int *gpio2_oe_addr;
    volatile unsigned int *gpio2_datain_addr;
    volatile void *gpio3_addr;
    volatile unsigned int *gpio3_oe_addr;
    volatile unsigned int *gpio3_datain_addr;

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
    printf("GPIO1 mapped to %p\n", gpio1_addr);
    printf("GPIO1 OE mapped to %p\n", gpio1_oe_addr);
    printf("GPIO1 SETDATAOUTADDR mapped to %p\n", gpio1_setdataout_addr);
    printf("GPIO1 CLEARDATAOUT mapped to %p\n", gpio1_cleardataout_addr);

    //setup GPIO2
    printf("Mapping %X - %X (size: %X)\n", GPIO2_START_ADDR, GPIO2_END_ADDR, GPIO2_SIZE);

    gpio2_addr = mmap(0, GPIO2_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO2_START_ADDR);

    gpio2_oe_addr           = gpio2_addr + GPIO_OE;
    gpio2_datain_addr   = gpio2_addr + GPIO_DATAIN;

    if(gpio2_addr == MAP_FAILED) {
        printf("Unable to map GPIO2\n");
        exit(1);
    }
    printf("GPIO2 mapped to %p\n", gpio2_addr);
    printf("GPIO2 OE mapped to %p\n", gpio2_oe_addr);
    printf("GPIO2 GPIO_DATAIN mapped to %p\n", gpio2_datain_addr);

    //setup GPIO3
    printf("Mapping %X - %X (size: %X)\n", GPIO3_START_ADDR, GPIO2_END_ADDR, GPIO2_SIZE);

    gpio3_addr = mmap(0, GPIO3_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO3_START_ADDR);

    gpio3_oe_addr  = gpio3_addr + GPIO_OE;
    gpio3_datain_addr = gpio3_addr + GPIO_DATAIN;

    if(gpio3_addr == MAP_FAILED) {
        printf("Unable to map GPIO3\n");
        exit(1);
    }
    printf("GPIO3 mapped to %p\n", gpio3_addr);
    printf("GPIO3 OE mapped to %p\n", gpio3_oe_addr);
    printf("GPIO3 DATAIN mapped to %p\n", gpio3_datain_addr);

    // Set up GPIO1 I/O
    reg = *gpio1_oe_addr;
    printf("GPIO1 configuration: %X\n", reg);
    reg &= ~USR3;       // Set USR3 bit to 0
    reg &= ~USR2;       // Set USR2 bit to 0
    *gpio1_oe_addr = reg;

    // Set up GPIO2 I/O
    reg = *gpio2_oe_addr;
    printf("GPIO2 configuration: %X\n", reg);
    reg &= PAUSE;       // Set button1 bit to 1
    *gpio2_oe_addr = reg;

    // Set up GPIO3 I/O
    reg = *gpio3_oe_addr;
    printf("GPIO3 configuration: %X\n", reg);
    reg &= GPIO3_17;       // Set button1 bit to 1
    printf("Start copying PAUSE to USR2\n");
    printf("Start copying GPIO3_17 to USR3\n");

    // Main loop
    while(keepgoing) { 
    // PAUSE > USR2
    	if(*gpio2_datain_addr & PAUSE) {
            *gpio1_setdataout_addr= USR2;
    	} else {
            *gpio1_cleardataout_addr = USR2;
    	}
        // GPIO3_17 > USR3
    	if(*gpio3_datain_addr & GPIO3_17) {
            *gpio1_setdataout_addr= USR3;
    	} else {
            *gpio1_cleardataout_addr = USR3;
    	}
    }
    close(fd);
    return 0;
}
