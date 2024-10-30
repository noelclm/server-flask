import os

PROD_ENV = 'PROD'
DEV_ENV = 'DEV'
LOCAL_ENV = 'LOCAL'
ENV = os.getenv('ENV', LOCAL_ENV)
URL_API = os.getenv('URL_API', 'http://127.0.0.1:5000')

# TOKEN
SECRET_KEY = os.getenv('SECRET_KEY')
