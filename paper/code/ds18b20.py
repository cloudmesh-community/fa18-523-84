# Source: http://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/ 

import os
import sys
import glob
import time

class ds18b20(object):
	"""docstring for ds18b20
	DS18B20 sensor should be plugged into GPIO4
	Returns temp in celcius then farenhiet
	"""
	def __init__(self):
		os.system('modprobe w1-gpio')
		os.system('modprobe w1-therm')
		self.base_dir = '/sys/bus/w1/devices/'
		self.device_folder = glob.glob(self.base_dir + '28*')[0]
		self.device_file = self.device_folder + '/w1_slave'

	def read_temp_raw(self):
		f = open(self.device_file, 'r')
		lines = f.readlines()
		f.close()
		return lines

	def get(self):
		lines = self.read_temp_raw()
		while lines[0].strip()[-3:] != 'YES':
			time.sleep(0.2)
			lines = read_temp_raw()
		equals_pos = lines[1].find('t=')
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = float(temp_string) / 1000.0
			temp_f = temp_c * 9.0 / 5.0 + 32.0
			return temp_c, temp_f
		

if __name__ == '__main__':
	try:
		temperature = ds18b20()
		while True:
			print(temperature.get())
			time.sleep(1)
	except KeyboardInterrupt:
		print('\n\n*** Stopping Program ***')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
