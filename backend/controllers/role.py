from sqlalchemy.orm import Session

from schemas import role as schema
from models import role as model

def get_roles(db:Session, offset:int = 0, limit: int = 100):
    return db.query(model.Role).offset(offset).limit(limit).all()

def get_role(db:Session, role_id:int):
    return db.query(model.Role).filter(model.Role.id == role_id).first()

def get_role_by_name(db:Session, role_name:str):
    return db.query(model.Role).filter(model.Role.name == role_name).first()

def create_role(db:Session, role:schema.RoleCreate):
    new_role = model.Role(**role.dict())
    exist = db.query(model.Role).filter(model.Role.name == new_role.name).first()
    if exist:
        return exist
    db.add(new_role)
    db.commit() # commit change to database
    db.refresh(new_role) # query an updated version of obj from database
    return new_role

def edit_role(db:Session, role:schema.Role, update_info:schema.RoleCreate):
    role.name = update_info.name
    role.permission = update_info.permission
    db.commit()
    db.refresh(role)
    return role

def delete_role(db:Session, role:schema.Role):
    try:
        db.delete(role)
    except Exception as e:
        print(e)
        return False
    else:
        # if nothing went wrong then do commit
        db.commit()
        return True
