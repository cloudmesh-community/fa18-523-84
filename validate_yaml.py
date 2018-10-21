# Adapted from stackexchange user post (jaiks): https://stackoverflow.com/questions/3262569/validating-a-yaml-document-in-python

import yaml

with open("README.yaml", 'r') as file:
    try:
        print(yaml.load(file))
    except yaml.YAMLError as exception:
        print(exception)
