#!/bin/bash

VIRTUALENV_HOME=".env"

python pyconfig/config.py -e $VIRTUALENV_HOME $1
source .env/bin/activate