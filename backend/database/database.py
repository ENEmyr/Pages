from configs import DB_CONF
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "{dialect}://{username}:{password}@{host}/{database}".format(**DB_CONF)
engine = create_engine(DATABASE_URL)
sess = sessionmaker(autocommit=False, autoflush=False, bind=engine) # create database session
Base = declarative_base() # return class of base
