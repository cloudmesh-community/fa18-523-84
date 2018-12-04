#Initial Cluster Setup

from fabric import Connection

workers = {'PiCluster_w01': '169.254.62.205', 
	   'PiCluster_w02': '169.254.122.189', 
	   'PiCluster_w03': '169.254.159.1', 
	   'PiCluster_w04': '169.254.111.219'}

for key, value in workers.items():
	#print(key+': '+value)
	c = Connection(value, connect_timeout=60)
	c.connect_kwargs.password = 'Weather_Center01' #change back to raspberry
	
	result = c.run('uname -s')
	print("{}: {}".format(value, result.stdout.strip()))
	
	'''
	#change password and hostname
	print('INFO: changing password')
	c.run('echo pi:Weather_Center01 | sudo chpasswd') #uname -s
	print('INFO: password changed')
	print('INFO: changing hostname')
	c.run('sudo hostnamectl set-hostname '+key)
	c.run('echo $(hostname -I | cut -d\  -f1) $(hostname) | sudo tee -a /etc/hosts')
	print('INFO: hostname changed')
	'''
	
	'''
	#update nodes
	print('INFO: running sudo apt-get update')
	c.run('sudo apt-get update')
	print('INFO: running apt-get upgrade -y')
	c.run('sudo apt-get upgrade -y')
	print('INFO: running sudo apt-get dist-upgrade -y')
	c.run('sudo apt-get dist-upgrade -y')
	print('INFO: upgrades complete')
	'''
	
	#Install packages and programs
	c.run('sudo apt-get install python3-pip')
	c.run('sudo apt-get install python3-pandas')
	print('INFO: python packages installed')
	
	#reboot each node
	#c.run('sudo shutdown -r 1') #reboot in 60 sec to avoid issues with ssh connection
	
