from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base

class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=300), unique=True, index=True)

    # Relation to other models
    pagetag = relationship("PageTag", back_populates="page_tag")

    def __repr__(self) -> str:
        return "<{}{}>".format(self.__class__.__name__, 
                repr((self.id,
                    self.name,
                    )))

    def dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }
