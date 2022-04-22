from datetime import datetime
from time import time
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from database.database import Base

class Page(Base):
    __tablename__ = "page"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=300), index=True)
    content = Column(String())
    popularity = Column(Float, default=0)
    create_dt = Column(DateTime(), default=datetime.fromtimestamp(time()))
    modified_dt = Column(DateTime(), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    # Relation to other models
    user = relationship("User", back_populates="page")
    pagetag = relationship("PageTag", back_populates="page")
    pagecate = relationship("PageCate", back_populates="page")

    def __repr__(self) -> str:
        return "<{}{}>".format(self.__class__.__name__, 
                repr((self.id,
                    self.title,
                    self.content,
                    self.popularity,
                    self.create_dt,
                    self.modified_dt,
                    self.user_id,
                    self.user)))

    def dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'popularity': self.popularity,
            'create_dt': self.create_dt,
            'modified_dt': self.modified_dt,
            'user_id': self.user_id
        }
