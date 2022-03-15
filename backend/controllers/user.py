from sqlalchemy.orm import Session

from schemas import user as schema
from models import user as model

from datetime import datetime
from time import time

def get_users(db:Session, offset:int = 0, limit:int = 100):
    return db.query(model.User).offset(offset).limit(limit).all()

def get_user(db:Session, user_id:int):
    return db.query(model.User).filter(model.User.id == user_id).first()

def get_user_from_email(db:Session, user_email:str):
    return db.query(model.User).filter(model.User.email == user_email.lower()).first()

def get_user_from_penname(db:Session, user_penname:str):
    return db.query(model.User).filter(model.User.penname.ilike(user_penname)).first()

def search_user(db:Session, search_conditions:schema.UserSearch):
    # columns = ['first_name', 'last_name', 'penname', 'role_id']
    columns = list(filter(
        lambda key: True if not key.startswith('__') and not key.startswith('<') else False,
        schema.UserSearch.__class__.__dict__.keys()))
    conditions = {column: search_conditions for column in columns}
    searched = [db.query.filter(getattr(model, col).ilike(f'{val}%')).all() for col, val in conditions.items()]
    return [item for item in searched if searched]

def create_user(db:Session, user:schema.UserPwd):
    new_user = model.User(**user.dict())
    try:
        db.add(new_user)
    except Exception as e:
        print(e)
        db.rollback()
        return []
    else:
        db.commit()
        db.refresh(new_user)
        return schema.UserData(**new_user.dict())

def edit_user(db:Session, user:schema.User, update_info:schema.UserPwd):
    try:
        update_info.modified_dt = datetime.fromtimestamp(time())
        for key, val in update_info.dict().items():
            if val != None:
                setattr(user, key, val)
    except Exception as e:
        print(e)
        db.rollback()
        return None
    else:
        db.commit()
        db.refresh(user)
        return user

def alter_user(db:Session, user:schema.User, update_info:schema.UserData):
    try:
        update_info.modified_dt = datetime.fromtimestamp(time())
        for key, val in update_info.dict().items():
            if val != None:
                setattr(user, key, val)
    except Exception as e:
        print(e)
        db.rollback()
        return None
    else:
        db.commit()
        db.refresh(user)
        return user

def delete_user(db:Session, user:schema.User):
    try:
        db.delete(user)
    except Exception as e:
        print(e)
        db.rollback()
        return False
    else:
        db.commit()
        return True
