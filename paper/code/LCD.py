# Source: http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/

from RPLCD import CharLCD
from RPi import GPIO

class LCD_Display(object):
	"""docstring for LCD_Display"""
	def __init__(self, cols=16, rows=2, rs=37, e=35, data_pins = [33,31,29,23], mode='BOARD'):
		if mode == 'BCM':
			self.lcd = CharLCD(cols=cols, rows=rows, pin_rs=rs, pin_e=e, pins_data=data_pins, numbering_mode=GPIO.BCM)
		else:
			self.lcd = CharLCD(cols=cols, rows=rows, pin_rs=rs, pin_e=e, pins_data=data_pins, numbering_mode=GPIO.BOARD)


	def display_string(self, string=u'Hello World!', clear='N'):
		if clear == 'Y':
			self.lcd.clear()
		else:
			pass
		self.lcd.write_string(string)


LCD_Display().display_string()
