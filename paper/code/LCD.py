# Source: http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/

from RPLCD import CharLCD
from RPi import GPIO

class LCD_Display(object):
	"""docstring for LCD_Display
	This class is for the 16 x 2 LCD component
	"""
	def __init__(self, cols=16, rows=2, rs=37, e=35, data_pins = [33,31,29,23], mode='BOARD'):
		GPIO.setwarnings(False)
		if mode == 'BCM':
			self.lcd = CharLCD(cols=cols, rows=rows, pin_rs=rs, pin_e=e, pins_data=data_pins, numbering_mode=GPIO.BCM)
		else:
			self.lcd = CharLCD(cols=cols, rows=rows, pin_rs=rs, pin_e=e, pins_data=data_pins, numbering_mode=GPIO.BOARD)
		

	def display_string(self, string, clear='N', pos=(0,0)):
		if clear == 'Y':
			self.lcd.clear()
		else:
			pass
		self.lcd.cursor_pos = pos
		self.lcd.write_string(string)

if __name__ == '__main__':
	LCD_Display().display_string(u'Hello World!')
