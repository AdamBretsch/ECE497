# The main files for hw03 are fTemp.sh, tempAlarm.py, and etch_disp.py

# fTemp.sh is a shell program that reads out the values of two TMP101 sensors connected to the i2c bus in F.

# tempAlarm.py configures the Alarm pins of the TMP101 sensors and shows a message when tempurature passes a certain threshold and the hardware alarm goes off.
# A custom tempurature for the alarm can be set as a command line argument.
# For example "./tempAlarm.py 85" sets the alarm to go off at 85 degrees F.

# etch_display.py connects the previously made in hw02 etch a sketch with buttons to output to the led matrix. All the controls are the same as before, and printed to the console on startup.
