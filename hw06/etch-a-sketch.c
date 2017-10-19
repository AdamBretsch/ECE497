/*
To test that the Linux framebuffer is set up correctly, and that the device permissions
are correct, use the program below which opens the frame buffer and draws a gradient-
filled red square:

retrieved from:
Testing the Linux Framebuffer for Qtopia Core (qt4-x11-4.2.2)

http://cep.xor.aps.anl.gov/software/qt4-x11-4.2.2/qtopiacore-testingframebuffer.html
*/

#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <linux/fb.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include "beaglebone_gpio.h"

#include "/opt/source/Robotics_Cape_Installer/libraries/rc_usefulincludes.h"
#include "/opt/source/Robotics_Cape_Installer/libraries/roboticscape.h"

int main(int argc, char *argv[] )
{
    volatile void *gpio1_addr;
    volatile void *gpio2_addr;
    volatile unsigned int *gpio1_oe_addr;
    volatile unsigned int *gpio2_oe_addr;
    volatile unsigned int *gpio2_datain;
    volatile unsigned int *gpio1_setdataout_addr;
    volatile unsigned int *gpio1_cleardataout_addr;
    unsigned int reg;

    // initalize button input 
    int fd = open("/dev/mem", O_RDWR);

    printf("Mapping %X - %X (size: %X)\n", GPIO0_START_ADDR, GPIO0_END_ADDR, 
                                           GPIO0_SIZE);

    gpio1_addr = mmap(0, GPIO1_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 
                        GPIO1_START_ADDR);

    gpio1_oe_addr           = gpio1_addr + GPIO_OE;
    gpio1_setdataout_addr   = gpio1_addr + GPIO_SETDATAOUT;
    gpio1_cleardataout_addr = gpio1_addr + GPIO_CLEARDATAOUT;

    if(gpio1_addr == MAP_FAILED) {
        printf("Unable to map GPIO\n");
        exit(1);
    }

    gpio2_addr = mmap(0, GPIO2_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 
                        GPIO2_START_ADDR);

    gpio2_oe_addr           = gpio2_addr + GPIO_OE;
    gpio2_datain            = gpio2_addr + GPIO_DATAIN;

    if(gpio2_addr == MAP_FAILED) {
        printf("Unable to map GPIO\n");
        exit(1);
    }

    printf("Start copying PAUSE to USR3\n");

    int fbfd = 0;
    struct fb_var_screeninfo vinfo;
    struct fb_fix_screeninfo finfo;
    long int screensize = 0;
    char *fbp = 0;
    int x = 0, y = 1;       // Make it so the it runs before the encoder is moved
    int xold = 0, yold = 0;
    long int location = 0;

    // Open the file for reading and writing
    fbfd = open("/dev/fb0", O_RDWR);
    if (fbfd == -1) {
        perror("Error: cannot open framebuffer device");
        exit(1);
    }
    printf("The framebuffer device was opened successfully.\n");

    // Get fixed screen information
    if (ioctl(fbfd, FBIOGET_FSCREENINFO, &finfo) == -1) {
        perror("Error reading fixed information");
        exit(2);
    }

    // Get variable screen information
    if (ioctl(fbfd, FBIOGET_VSCREENINFO, &vinfo) == -1) {
        perror("Error reading variable information");
        exit(3);
    }

    printf("%dx%d, %dbpp\n", vinfo.xres, vinfo.yres, vinfo.bits_per_pixel);
    printf("Offset: %dx%d, line_length: %d\n", vinfo.xoffset, vinfo.yoffset, finfo.line_length);
    
    if (vinfo.bits_per_pixel != 16) {
        printf("Can't handle %d bpp, can only do 16.\n", vinfo.bits_per_pixel);
        exit(5);
    }

    // Figure out the size of the screen in bytes
    screensize = vinfo.xres * vinfo.yres * vinfo.bits_per_pixel / 8;

    // Map the device to memory
    fbp = (char *)mmap(0, screensize, PROT_READ | PROT_WRITE, MAP_SHARED, fbfd, 0);
    if ((int)fbp == -1) {
        perror("Error: failed to map framebuffer device to memory");
        exit(4);
    }
    printf("The framebuffer device was mapped to memory successfully.\n");

    // initialize hardware first
	if(rc_initialize()){
		fprintf(stderr,"ERROR: failed to run rc_initialize(), are you root?\n");
		return -1;
	}

	printf("\nRaw encoder positions\n");
	printf("   E1   |");
	printf("   E2   |");
	printf("   E3   |");
	printf("   E4   |");
	printf(" \n");
	
	// Black out the screen
	short color = (0<<11) | (0 << 5) | 8;  // RGB
	for(int i=0; i<screensize; i+=2) {
	    fbp[i  ] = color;      // Lower 8 bits
	    fbp[i+1] = color>>8;   // Upper 8 bits
	}

    int width = 5;
    int r = 0;     // 5 bits
    int g = 25;      // 6 bits
    int b = 0;      // 5 bits
    if (argc > 1){
        r = (int) argv[1]; 
        g = (int) argv[2]; 
        b = (int) argv[3]; 
    }
	while(rc_get_state() != EXITING) {
    	if (!(*gpio2_datain & PAUSE)) { // widen width with pause button
            if (width < 20){
                printf("width++, w = %d", width);
                width++;
            }
            *gpio1_setdataout_addr= USR3;
    	} else if (!(*gpio2_datain & MODE)){ // narrow width with mode button
        if (width > 5){
                printf("width--, w = %d", width);
                width--;
            }
            *gpio1_setdataout_addr= USR2;
        } else {
            *gpio1_cleardataout_addr = USR3;
            *gpio1_cleardataout_addr = USR2;
        }
		printf("\r");
		for(int i=1; i<=4; i++){
			printf("%6d  |", rc_get_encoder_pos(i));
		}
		fflush(stdout);
        // Update framebuffer
        // Figure out where in memory to put the pixel
        x = (rc_get_encoder_pos(1)/2 + vinfo.xres) % vinfo.xres;
        y = (rc_get_encoder_pos(3)/2 + vinfo.yres) % vinfo.yres;
        // printf("xpos: %d, xres: %d\n", rc_get_encoder_pos(1), vinfo.xres);
        
        if((x != xold) || (y != yold)) {
            printf("Updating location to %d, %d\n", x, y);
            // Original drawing logic
            /*location = (xold+vinfo.xoffset) * (vinfo.bits_per_pixel/8) +
                       (yold+vinfo.yoffset) * finfo.line_length;
            unsigned short int t = r<<11 | g << 5 | b;
            *((unsigned short int*)(fbp + location)) = t;*/
            //make line wider
            for (int i = 0; i < width; i++){
                for (int j = 0; j < width; j++){
                    location = (xold+vinfo.xoffset+i)%vinfo.xres * (vinfo.bits_per_pixel/8) +
                            (yold+vinfo.yoffset+j)%vinfo.yres * finfo.line_length;
                    unsigned short int t = r<<11 | g << 5 | b;
                    *((unsigned short int*)(fbp + location)) = t;
                }
            }
            
            // Set new location to white
            location = (x+vinfo.xoffset) * (vinfo.bits_per_pixel/8) +
                       (y+vinfo.yoffset) * finfo.line_length;
    
            *((unsigned short int*)(fbp + location)) = 0xff;
            xold = x;
            yold = y;
            // cycle colors
            if (r <= 255){ 
                r++;
                if (r == 255){r = 0;}
                if (g <= 255){
                    if (g == 255){g = 0;}
                    g++; 
                    if (b <= 255){
                        if (b == 255){b = 0;}
                        b++; 
                    }
                }
            }
        }
		
		rc_usleep(5000);
	}
	// cleanup 
	rc_cleanup();
    
    munmap(fbp, screensize);
    munmap((void *)gpio1_addr, GPIO1_SIZE);
    munmap((void *)gpio2_addr, GPIO2_SIZE);
    close(fbfd);
    return 0;
}
