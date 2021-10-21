import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.getenv('DEBUG',True)
BEARER_TOKEN = os.getenv('BEARER_TOKEN','')
DOMAIN = os.getenv('DOMAIN','localhost:5000/')