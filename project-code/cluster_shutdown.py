#shutdown cluster

#ERROR WITH FABRIC SHUTDOWN AND REBOOT http://www.fabfile.org/upgrading.html#task-functions-decorators
#Work around is to schedule shutdown for 1min later.

from fabric import Connection

workers = {
	'PiCluster_p01': '10.0.0.42',
	'PiCluster_w01': '10.0.0.36',
	'PiCluster_w02': '10.0.0.37',
	'PiCluster_w03': '10.0.0.41',
	'PiCluster_w04': '10.0.0.40'
	}

for key, value in workers.items():
	print(key+': '+value)
	c = Connection(value)
	c.connect_kwargs.password = 'Weather_Center01' #change back to raspberry
	result = c.run('sudo shutdown -h 1')
	print("{}: {}".format(value, result.stdout.strip()))
