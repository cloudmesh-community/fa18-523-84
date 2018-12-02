#shutdown cluster

from fabric import Connection

parent_node = '10.0.0.31' #wlan0 = 10.0.0.31 | eth0 = 169.254.156.125

workers = {'w1': '169.254.62.205', 'w2': '169.254.122.189', 'w3': '169.254.159.1', 'w4': '169.254.111.219'}

for key, value in workers.items():
	print(key+': '+value)
	c = Connection(value)
	c.connect_kwargs.password = 'raspberry'
	result = c.run('sudo shutdown -h now') #uname -s
	print("{}: {}".format(value, result.stdout.strip()))
