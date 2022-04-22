from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base

class UserFavorite(Base):
    __tablename__ = "user_favorite"
    page_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)

    # Relation to other models
    page = relationship("Page", back_populates="userfavorite")
    user = relationship("User", back_populates="userfavorite")

    def __repr__(self) -> str:
        return "<{}{}>".format(self.__class__.__name__, 
                repr((self.page_id,
                    self.user_id,
                    )))

    def dict(self) -> dict:
        return {
            'page_id': self.page_id,
            'user_id': self.user_id
        }
