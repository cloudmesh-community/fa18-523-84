#Initial Cluster Setup

from fabric import Connection

workers = {'w1': '169.254.62.205', 'w2': '169.254.122.189', 'w3': '169.254.159.1', 'w4': '169.254.111.219'}

for key, value in workers.items():
	print(key+': '+value)
	c = Connection(value)
	c.connect_kwargs.password = 'raspberry'
	result = c.run('sudo echo pi:Weather!Center01 | chpasswd') #uname -s
	print("{}: {}".format(value, result.stdout.strip()))
