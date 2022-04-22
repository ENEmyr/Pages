from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base

class PageTag(Base):
    __tablename__ = "page_tag"
    page_id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, primary_key=True)

    # Relation to other models
    page = relationship("page", back_populates="pagetag")
    tag = relationship("tag", back_populates="pagetag")

    def __repr__(self) -> str:
        return "<{}{}>".format(self.__class__.__name__, 
                repr((self.page_id,
                    self.tag_id,
                    )))

    def dict(self) -> dict:
        return {
            'page_id': self.page_id,
            'tag_id': self.tag_id
        }
