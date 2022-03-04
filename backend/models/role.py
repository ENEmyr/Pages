from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base

# permission levels
# 0 = administrator
# 1 = tester
# 2 = moderator
# 3 = editor
# 4 = verified user
# 5 = user

class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=300), unique=True, index=True)
    permission = Column(String(length=1), default='5')

    # Relation to other models
    user = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return "<{}{}>".format(self.__class__.__name__, 
                repr((self.id,
                    self.name,
                    self.permission.
                    self.user)))
