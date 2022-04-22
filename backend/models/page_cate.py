from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base

class PageCate(Base):
    __tablename__ = "page_cate"
    page_id = Column(Integer, primary_key=True)
    cate_id = Column(Integer, primary_key=True)

    # Relation to other models
    page = relationship("page", back_populates="pagecate")
    category = relationship("category", back_populates="pagecate")

    def __repr__(self) -> str:
        return "<{}{}>".format(self.__class__.__name__, 
                repr((self.page_id,
                    self.cate_id,
                    )))

    def dict(self) -> dict:
        return {
            'page_id': self.page_id,
            'cate_id': self.cate_id
        }
