#!/bin/bash
for((;;))
#main loop
do
  # get temp values
  tempC1=`i2cget -y 1 0x48`
  tempC2=`i2cget -y 1 0x4a`
  # convert to F
  tempF1=$((($tempC1*9/5)+32))
  tempF2=$((($tempC2*9/5)+32))
  # output to console
  echo It is $tempF1 and $tempF2 degrees F
  sleep 1
done
