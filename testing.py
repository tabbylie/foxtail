import os 
from sqlalchemy import create_engine
from app.models import Products

basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine(f'sqlite:///{basedir}tail.db')

