"""Prod config for minitwit"""
import os

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
DEBUG = True
SECRET_KEY = os.environ['SECRET_KEY']
PER_PAGE = 30
