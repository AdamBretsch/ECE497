# Before running gpioToggle.c and gpioThru.c, install.sh must be ran as superuser.

# gpioToggle.c reads from 2 switches and controls 2 leds with the values. 
# These switches are GPIO2_5 (PAUSE) and GPIO3_17 (GP0_6).
# The leds are USR2 and USR3.

# gpioThu.c has been modified to copy from swich GPIO2_5 to control led USR3.

# etch_display has full functionality with buttons, LEDMatrix, TMP101 sensors, and now encoders.
# Instructions on how to play are shown at startup.

# memstack_gpio.jpg is a visual representation of the memory and GPIO ports of the BeagleBone Blue

