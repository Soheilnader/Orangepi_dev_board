#UART2
import serial
import time

ser = serial.Serial('/dev/ttyS1', baudrate = 9600, timeout = 0.5)

def getValues():
  ser.write(b'g')
  data = ser.readline().decode('ascii')
  return data
  
while(1):
  #user_input = input('Input: ')
  #if user_input == 'y':
    #print(getValues())
  print(getValues())
  #time.sleep(0.05)
