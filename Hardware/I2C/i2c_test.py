#!/usr/bin/env python

from pyA20 import i2c

from time import sleep

def write_eeprom(dev_add, add, data):

  i2c.init("/dev/i2c-0")  #Initialize module to use /dev/i2c-0
  i2c.open(dev_add)  #The slave device address is 0x50
  i2c.write([add, data]) #Write data to register add
  i2c.close() #End communication with slave device
  sleep(0.005)

def read_eeprom(dev_add, add, bytes):
  i2c.init("/dev/i2c-0")
  i2c.open(dev_add)
  i2c.write([add])
  value1 = i2c.read(bytes)
  i2c.close()
  sleep(0.005)
  return value1


write_eeprom(0x50, 0x3, 0x0F)
print(read_eeprom(0x50, 0x00, 5))
#for i in range(127):
  #write_eeprom(0x50, i, 255)  
#print(read_eeprom(0x50, 0x00, 128))
