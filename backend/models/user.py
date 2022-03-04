from datetime import datetime
from time import time
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database.database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=300), unique=True, index=True)
    password = Column(String(length=128))
    password_salt = Column(String(length=50))
    first_name = Column(String(length=300))
    last_name = Column(String(length=300))
    penname = Column(String(length=300), unique=True, index=True)
    gender = Column(String(length=1), default='m')
    image_url = Column(String(length=300))
    create_dt = Column(DateTime(), default=datetime.fromtimestamp(time()))
    modified_dt = Column(DateTime(), nullable=True)
    birthdate = Column(DateTime(), nullable=True)
    rank = Column(Integer, default=0)
    role_id = Column(Integer, ForeignKey('role.id'))

    # Relation to other models
    role = relationship("Role", back_populates="user")

    def __repr__(self) -> str:
        return "<{}{}>".format(self.__class__.__name__, 
                repr((self.id,
                    self.email,
                    self.password,
                    self.password_salt,
                    self.first_name,
                    self.last_name,
                    self.penname,
                    self.gender,
                    self.image_url,
                    self.create_dt,
                    self.modified_dt,
                    self.birthdate,
                    self.rank,
                    self.role_id,
                    self.role)))
