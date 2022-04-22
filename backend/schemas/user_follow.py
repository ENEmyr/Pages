from pydantic import BaseModel, Field

class UserFollow(BaseModel):
    """
    A class that use for manipulate user_follow table
    """
    # id: int = Field(..., description='User Follow Id')
    user_id: int = Field(..., description='Foreign key of User table, use for find following users')
    follow_id: int = Field(..., description='Foreign key of User table, use  for find follower users')
    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'user_id': 1,
                'follow_id': 2,
            }
        }
