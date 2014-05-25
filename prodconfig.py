"""Prod config for minitwit"""
import os

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
DEBUG = True
SECRET_KEY = 'development key'
PER_PAGE = 30
