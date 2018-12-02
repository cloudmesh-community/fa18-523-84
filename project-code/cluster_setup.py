#Initial Cluster Setup

from fabric import Connection

workers = {'PiCluster_w01': '169.254.62.205', 
	   'PiCluster_w02': '169.254.122.189', 
	   'PiCluster_w03': '169.254.159.1', 
	   'PiCluster_w04': '169.254.111.219'}

for key, value in workers.items():
	print(key+': '+value)
	c = Connection(value, connect_timeout=60)
	c.connect_kwargs.password = 'Weather_Center01' #change back to raspberry
	#c.run('echo pi:Weather_Center01 | sudo chpasswd') #uname -s
	#print('password changed')
	#c.run('sudo hostnamectl set-hostname '+key)
	#print('hostname changed')
	c.run('sudo reboot')
	c.close()
	print('rebooting '+key)
