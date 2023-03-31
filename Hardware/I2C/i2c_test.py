#!/usr/bin/env python

from pyA20 import i2c

i2c.init("/dev/i2c-0")  #Initialize module to use /dev/i2c-0
i2c.open(0x50)  #The slave device address is 0x55

#If we want to write to some register
#i2c.write([1, 10]) #Write 0x20 to register 0xAA


#If we want to do write and read
i2c.write([0x00])   #Set address at 0xAA register
value1 = i2c.read(1) #Read 1 byte with start address 0xAA

i2c.write([0x01])   #Set address at 0xAA register
value2 = i2c.read(3) #Read 1 byte with start address 0xAA

i2c.close() #End communication with slave device

print(value1)
print(value2)
