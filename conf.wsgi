#!/usr/bin/python
import os

# Work around needed to s3.py can access keys in config.py outside of the app context.
os.environ['FLASK_ENV']= 'production'

from app import app as application
