import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = sqlite3.connect("top-x.db")
cursor = db.cursor()
