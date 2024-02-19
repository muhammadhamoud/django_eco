import pymysql
pymysql.install_as_MySQLdb()

# import celery
from .celery import app as celery_app
__all__ = ['celery_app']
