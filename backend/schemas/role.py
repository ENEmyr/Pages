from pydantic import BaseModel, Field

class RoleCreate(BaseModel):
    name: str = Field(default=None, max_length=300, description='Role name.')
    permission: str = Field(default='5', max_length=1)

    class Config:
        schema_extra = {
            'example': {
                'name': 'User',
                'permission': '5'
            }
        }

class Role(RoleCreate):
    id: int = Field(default=None)

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'name': 'User',
                'permission': '5'
            }
        }
