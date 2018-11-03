# Source: http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/

from RPLCD import CharLCD
from RPi import GPIO
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35,pins_data=[33,31,29,23], numbering_mode=GPIO.BOARD)
lcd.write_string(u'Hello World!')
