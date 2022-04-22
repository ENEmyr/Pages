from sqlalchemy.orm import Session

from schemas import user as user_schema
from schemas import user_follow as schema
from models import user_follow as model

def get_following(db:Session, user_id:int):
    following_users =  db.query(model.UserFollow).filter(model.UserFollow.user_id == user_id).all()
    followings = []
    for user in following_users:
        followings.append(user.follow)
    followings_filtered = list(map(lambda item: user_schema.UserSearch(**item.dict()), followings)) if followings else [] # filter out all personal information
    return followings_filtered

def get_follower(db:Session, user_id:int):
    follower_users = db.query(model.UserFollow).filter(model.UserFollow.follow_id == user_id).all()
    followers = []
    for user in follower_users:
        followers.append(user.user)
    followers_filtered = list(map(lambda item: user_schema.UserSearch(**item.dict()), followers)) if followers else [] # filter out all personal information
    return followers_filtered

def follow(db:Session, user_follow:schema.UserFollow):
    exist = db.query(model.UserFollow).filter(
            model.UserFollow.user_id == user_follow.user_id, 
            model.UserFollow.follow_id == user_follow.follow_id).first()
    if exist:
        return False
    try:
        new_follow = model.UserFollow(**user_follow.dict())
        db.add(new_follow)
    except Exception as e:
        print(e)
        db.rollback()
        return []
    else:
        db.commit()
        return get_following(db, user_follow.user_id)

def unfollow(db:Session, user_id:int, follow_id:int):
    follows = db.query(model.UserFollow).filter(
            model.UserFollow.user_id == user_id, 
            model.UserFollow.follow_id == follow_id).all()
    if not follows:
        return True
    try:
        for follow in follows:
            db.delete(follow)
    except Exception as e:
        print(e)
        db.rollback()
        return False
    else:
        db.commit()
        return True
