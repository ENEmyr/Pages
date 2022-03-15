from datetime import datetime
from time import time
from typing import Optional, Literal

from pydantic import BaseModel, Field, PositiveInt, root_validator, validator
from validators import email as validate_email

# REST Models
class UserData(BaseModel):
    email: str = Field(default=None, max_length=300, description='User email.')
    first_name: str = Field(default=None, max_length=300)
    last_name: str = Field(default=None, max_length=300)
    penname: str = Field(default=None, max_length=300)
    image_url: str = Field(default=None, max_length=300)
    role_id: int = Field(default=6, description='If not defined role will be User(6) by default.')
    gender: str = Field(default='m', description='If not defined gender will be male(m) by default.')
    rank: PositiveInt = Field(default=1, description='Rank of user')
    birthdate: datetime = datetime.fromtimestamp(time())#.isoformat()
    create_dt: Optional[datetime]= datetime.fromtimestamp(time())#.isoformat()
    modified_dt: Optional[datetime]= datetime.fromtimestamp(time())#.isoformat()

    @root_validator
    def root_validate(cls, values):
        if values.get('email') != None:
            if not validate_email(values.get('email')):
                raise ValueError('given email not in the email form.')
        return values
    class Config:
        schema_extra = {
            'example': {
                'email': 'test@admin.com',
                'first_name': 'Kevin',
                'last_name': 'Johnson',
                'penname': 'Penguin',
                'image_url': 'https://imgr.url',
                'role_id': 1,
                'gender': 'm',
                'rank': 30,
                'birthdate': datetime.fromtimestamp(time()),
                'create_dt': datetime.fromtimestamp(time()),
                'modified_dt': datetime.fromtimestamp(time())
            }
        }
class UserPwd(UserData):
    """
    A class that use for update password of user
    """
    password: str = Field(default=None, description='User password.')
    password_salt: str = Field(default=None, description='User password\'s salt')
    @validator("password")
    def check_len_pwd(cls, v):
        if v != None:
            if len(v) < 8:
                raise ValueError('password must longer than 8 characters')
        return v
    class Config:
        schema_extra = {
            'example': {
                'email': 'test@admin.com',
                'first_name': 'Kevin',
                'last_name': 'Johnson',
                'penname': 'Penguin',
                'image_url': 'https://imgr.url',
                'role_id': 1,
                'gender': 'm',
                'rank': 30,
                'birthdate': datetime.fromtimestamp(time()),
                'create_dt': datetime.fromtimestamp(time()),
                'modified_dt': datetime.fromtimestamp(time()),
                'password': 'ebb7323f7312b736c3c9091e9f9f69b0c96ff2181d1b221cb29823f84a70bf1dc96bd8941c4790fd3e15a379ccb99a391f40bf01ad263d2d857acd7e3833f3b8',
                'password_salt': 'y=LN\\z])eJk0QE~]<TPJZyY;5RJ8&tk8a*1[xPd@L2XB}{KP>#'
            }
        }

class User(UserPwd):
    """
    A class that use for create user
    """
    id: int = Field(default=None)
    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'email': 'test@admin.com',
                'password': 'ebb7323f7312b736c3c9091e9f9f69b0c96ff2181d1b221cb29823f84a70bf1dc96bd8941c4790fd3e15a379ccb99a391f40bf01ad263d2d857acd7e3833f3b8',
                'password_salt': 'y=LN\\z])eJk0QE~]<TPJZyY;5RJ8&tk8a*1[xPd@L2XB}{KP>#',
                'first_name': 'Kevin',
                'last_name': 'Johnson',
                'penname': 'Penguin',
                'image_url': 'https://imgr.url',
                'role_id': 1,
                'gender': 'm',
                'rank': 30,
                'birthdate': datetime.fromtimestamp(time()),
                'create_dt': datetime.fromtimestamp(time()),
                'modified_dt': datetime.fromtimestamp(time())
            }
        }

class UserPrivateData(UserData):
    """
    A class that use for view user data
    """
    id: int = Field(default=None)
    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'email': 'test@admin.com',
                'first_name': 'Kevin',
                'last_name': 'Johnson',
                'penname': 'Penguin',
                'image_url': 'https://imgr.url',
                'role_id': 1,
                'gender': 'm',
                'rank': 30,
                'birthdate': datetime.fromtimestamp(time()),
                'create_dt': datetime.fromtimestamp(time()),
                'modified_dt': datetime.fromtimestamp(time())
            }
        }

class UserSignin(BaseModel):
    email: str = Field(..., max_length=300, description='User email.')
    password: str = Field(..., description='User password.')

    @validator('email')
    def validate_mail_form(cls, v):
        if not validate_email(v):
            raise ValueError('given email not in the email form.')
        return v
    @validator("password")
    def check_len_pwd(cls, v):
        if len(v) < 8:
            raise ValueError('password must longer than 8 characters')
        return v
    class Config:
        schema_extra = {
            'example': {
                'email': 'test@mail.com',
                'password': 'abc1234'
            }
        }

class UserRegis(UserSignin):
    first_name: str = Field(..., max_length=300)
    last_name: str = Field(..., max_length=300)
    gender: str = Field(default='m', max_length=1)
    penname: str = Field(..., max_length=300)
    image_url: str = Field(..., max_length=300)
    birthdate: datetime = datetime.fromtimestamp(time())#.isoformat()
    role_id: int = Field(default=5, description='If not defined role will be User(5) by default.')
    # password_salt: str = Field(default='default_salt', description='User password\'s salt')

    @root_validator
    def can_not_contain_space(cls, values):
        if ' ' in values.get('first_name') or ' ' in values.get('last_name'):
            raise ValueError('fist_name/last_name can\'t contains a space.')
        return values
    class Config:
        schema_extra = {
            'example': {
                'email': 'test@mail.com',
                'password': 'abc1234',
                'first_name': 'Kelvin',
                'last_name': 'Gurin',
                'gender': 'm',
                'birthdate': datetime.fromtimestamp(time()),
                'penname': 'Penguin',
                'image_url': 'https://imgur.url',
                'role_id': 3
            }
        }

class UserSearch(BaseModel):
    type: Literal['user'] = Field(default='user')
    id: int = Field(...)
    role_id: int = Field(..., description='If not defined role will be User(5) by default.')
    penname: str = Field(..., max_length=300)
    rank: PositiveInt = Field(..., description='Rank of user')
    gender: str = Field(..., max_length=1)
    image_url: str = Field(..., max_length=300)

    class Config:
        schema_extra = {
            'example': {
                'type': 'user',
                'id': 1,
                'role_id': 5,
                'penname': 'Penguin',
                'rank': 30,
                'gender': 'm',
                'image_url': 'https://imgur.url'
            }
        }
