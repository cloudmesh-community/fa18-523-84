#Initial Cluster Setup

from fabric import Connection

workers = {'PiCluster_w01': '169.254.62.205', 
	   'PiCluster_w02': '169.254.122.189', 
	   'PiCluster_w03': '169.254.159.1', 
	   'PiCluster_w04': '169.254.111.219'}

@needs_host
def reboot(wait=120, command='reboot', use_sudo=True):
	# Shorter timeout for a more granular cycle than the default.
	timeout = 5
	# Use 'wait' as max total wait time
	attempts = int(round(float(wait) / float(timeout)))
	# Don't bleed settings, since this is supposed to be self-contained.
	# User adaptations will probably want to drop the "with settings()" and
	# just have globally set timeout/attempts values.
	with settings(
		hide('running'),
		timeout=timeout,
		connection_attempts=attempts
	):
		(sudo if use_sudo else run)(command)
		# Try to make sure we don't slip in before pre-reboot lockdown
		time.sleep(5)
		# This is actually an internal-ish API call, but users can simply drop
		# it in real fabfile use -- the next run/sudo/put/get/etc call will
		# automatically trigger a reconnect.
		# We use it here to force the reconnect while this function is still in
		# control and has the above timeout settings enabled.
		connections.connect(env.host_string)


for key, value in workers.items():
	print(key+': '+value)
	c = Connection(value, connect_timeout=60)
	c.connect_kwargs.password = 'Weather_Center01' #change back to raspberry
	#c.run('echo pi:Weather_Center01 | sudo chpasswd') #uname -s
	#print('password changed')
	#c.run('sudo hostnamectl set-hostname '+key)
	#print('hostname changed')
	reboot()
	print('rebooting '+key)
