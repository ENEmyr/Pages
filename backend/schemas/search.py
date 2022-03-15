from typing import Optional, Union, List

from pydantic import BaseModel, Field
from schemas import user as user_schema
from schemas import role as role_schema

# REST Models
class SearchItems(BaseModel):
    count: int = Field(default=0, description='number of search items')
    items: Optional[List[Union[user_schema.UserSearch, role_schema.RoleSearch]]]
