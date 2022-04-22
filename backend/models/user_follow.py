from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from database.database import Base

class UserFollow(Base):
    __tablename__ = "user_follow"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False) # find from user_id will get following users
    follow_id = Column(Integer, ForeignKey('user.id'), nullable=False) # find from follow_id will get follower users

    # Relation to other models
    user = relationship('User', backref='user', uselist=False, foreign_keys=[user_id])
    follow = relationship('User', backref='follow', uselist=False, foreign_keys=[follow_id])

    def __repr__(self) -> str:
        return "<{}{}>".format(self.__class__.__name__, 
                repr((self.user_id,
                    self.follow_id,
                    )))

    def dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'follow_id': self.follow_id
        }
