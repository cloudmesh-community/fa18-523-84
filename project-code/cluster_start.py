#Initial Cluster Setup

from fabric import Connection

#PiCluster_p01 eth0: 10.0.0.42  wlan0:10.0.0.31
#cassandra seeds: 10.0.0.42, 10.0.0.40

workers = {
	'PiCluster_w01': '10.0.0.36',
	'PiCluster_w02': '10.0.0.37',
	'PiCluster_w03': '10.0.0.41',
	'PiCluster_w04': '10.0.0.40'
	}

for key, value in workers.items():
	#print(key+': '+value)
	c = Connection(value, connect_timeout=60)
	c.connect_kwargs.password = 'raspberry' #update with the password you have set
	
	result = c.run('uname -s')
	print("{}: {}".format(value, result.stdout.strip()))
	
	#Only run if all yaml files have been updated
	print('\n\nINFO: starting cassandra daemon\n\n')
	c.run('cd apache-cassandra-3.11.3 && bin/cassandra')
