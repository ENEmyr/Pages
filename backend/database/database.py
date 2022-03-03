from configs import DB_CONF
from databases import Database
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

DATABASE_URL = "{dialect}://{username}:{password}@{host}/{database}".format(**DB_CONF)
db = Database(DATABASE_URL)
# engine = create_engine(DATABASE_URL)
# sess = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# base = declarative_base()
# conn = engine.connect()
# res = conn.execute('SELECT host FROM INFORMATION_SCHEMA.PROCESSLIST WHERE ID = CONNECTION_ID()').fetchall()
# print(res)
