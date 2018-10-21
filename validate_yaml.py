# Adapted from stackexchange user post (jaiks): https://stackoverflow.com/questions/3262569/validating-a-yaml-document-in-python

import os
import yaml

file_path = os.getcwd() 
with open(file_path+"/README.yml", 'r') as file:
    try:
        print(yaml.load(file))
    except yaml.YAMLError as exception:
        print(exception)
