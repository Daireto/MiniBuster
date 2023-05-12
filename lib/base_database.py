import env
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(env.DATABASE_URL + fr"C:\Users\{os.getenv('username')}" + r"\minibuster.db")
Session = sessionmaker(bind=engine)
BaseDatabase = declarative_base(bind=engine)