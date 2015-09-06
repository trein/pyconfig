#!/bin/bash

python pyconfig/config.py setup
python pyconfig/config.py $1
source .env/bin/activate