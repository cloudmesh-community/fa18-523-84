#!/bin/bash

sudo apt-get python3-pandas
pip3 install pyowm
pip3 install geocoder
echo "All python dependencies have been successfully installed."

mkdir ~/cassandra
cd cassandra
# https://academy.datastax.com/all-downloads?field_download_driver_category_tid=910
wget ""
