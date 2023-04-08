import serial
import time

ser = serial.Serial('/dev/ttyS1', 9600)  # open serial port
print(ser.name)         # check which port was really used

ser.write(b'1')
time.sleep(2)

ser.write(b'0')
   
ser.close()
