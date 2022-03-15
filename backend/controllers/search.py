from sqlalchemy.orm import Session

from schemas import search as search_schema
from schemas import user as user_schema
from schemas import role as role_schema
from models import user as user_model
from models import role as role_model

def append_search_item(*args):
    items = []
    for arg in args:
        for item in arg:
            items.append(item)
    return items

def search_for_users_and_pages(db:Session, keyword:str, offset:int = 0, limit:int = 100):
    users = db.query(user_model.User).filter(user_model.User.penname.contains(keyword, autoescape=True)).all()
    roles = db.query(role_model.Role).filter(role_model.Role.name.contains(keyword, autoescape=True)).all()

    # check for existance
    users = list(map(lambda item: user_schema.UserSearch(**item.dict()), users)) if users else []
    roles = list(map(lambda item: role_schema.RoleSearch(**item.dict()), roles)) if roles else []
    items = append_search_item(users, roles) # because standard list can't operate + over list of pydantic model
    searched = search_schema.SearchItems(count=len(users)+len(roles), items=items)

    if searched.count != 0:
        if offset < 0:
            offset = 0
        elif offset > searched.count:
            offset = searched.count-1
        searched.items = searched.items[offset:]
        searched.items = searched.items[:limit]
        searched.count = len(searched.items)
    return searched
