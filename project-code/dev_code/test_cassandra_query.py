#Cassandra set up for thermostat database

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

'''
cluster = Cluster(contact_points=['10.0.0.42','10.0.0.40'], port=9042)
session = cluster.connect()
session.execute("create keyspace smart_therm with replication={'class':'SimpleStrategy','replication_factor':3}")
session.execute("USE smart_therm")

therm_data = ' CREATE TABLE therm_data (
            indoor_time timestamp,
            outdoor_time timestamp,
            out_condition text,
            out_temp_f double,
            in_temp_f double,
            humidity double,
            status text,
            PRIMARY KEY (indoor_time))
        '

therm_status = 'CREATE TABLE therm_status (
            key double,
            update_time timestamp,
           	username text,
            sys_off text,
            fan_on text,
            desired_temp double,
            main double,
            secondary double,
            PRIMARY KEY (key))
'

session.execute(therm_data)
session.execute(therm_status)

cluster.shutdown()
'''

######################
# functions to send data to database
# Sources for this section:
#   code for pandas_factory function from: https://stackoverflow.com/questions/41247345/python-read-cassandra-data-into-pandas
#   documentation for cassandra cluster module: https://datastax.github.io/python-driver/api/cassandra/cluster.html
######################

def pandas_factory(colnames, rows):
	return pd.DataFrame(rows, columns=colnames)

def cassandra_query(keyspace, query, params=(), return_data=False, contact_points=['127.0.0.1'], port=9042):
	try:
		if return_data == True:
			cluster = Cluster( contact_points=contact_points, port=port )
			session = cluster.connect( keyspace )
			session.row_factory = pandas_factory
			session.default_fetch_size = None
			rslt = session.execute( query )
			rslt_df = rslt._current_rows
			cluster.shutdown()
			return rslt_df
		else:
			cluster = Cluster( contact_points, port )
			session = cluster.connect( keyspace )
			session.execute( query, params )
			cluster.shutdown()
	except:
		raise


query = 'SELECT * FROM therm_status'

result_df = cassandra_query('smart_therm', query, return_data=True, contact_points=['10.0.0.42'], port=9042)

print(result_df)
