#Cassandra set up for thermostat database

from cassandra.cluster import Cluster

cluster = Cluster(contact_points=['10.0.0.42','10.0.0.40'], port=9042)
session = cluster.connect()
session.execute("create keyspace smart_therm with replication={'class':'SimpleStrategy','replication_factor':3}")
session.execute("USE smart_therm")

therm_data = ''' CREATE TABLE therm_data (
            indoor_time timestamp,
            outdoor_time timestamp,
            out_condition text,
            out_temp_f double,
            in_temp_f double,
            humidity double,
            status text,
            PRIMARY KEY (indoor_time))
        '''

therm_status = '''CREATE TABLE therm_status (
            key double,
            update_time timestamp,
           	username text,
            sys_off text,
            fan_on text,
            desired_temp double,
            main double,
            secondary double,
            PRIMARY KEY (key))
'''

session.execute(therm_data)
session.execute(therm_status)

cluster.shutdown()
