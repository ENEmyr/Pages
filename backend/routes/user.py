from random import choice, seed
from string import ascii_letters, digits, punctuation
from time import time
from typing import List
from sys import getsizeof

from Crypto.Hash import SHA512
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Response, UploadFile, File

from helpers.generate_responses_dict import gen_res_dict
from helpers.auth_bearer import JWTBearer
from helpers.auth_handler import decode_token, sign_token
from schemas import user as schema
from controllers import user as controller

# 3600 = 1 Hr
TOKEN_DURATION = 3600*24
ACCEPTABLE_MIME_TYPES = ('image/jpeg', 'image/png', 'image/bmp', 'image/gif', 'image/tiff')

def export_routes(route:str, router:FastAPI, db:Session):
    @router.post(
        route+'/register',
        status_code=201,
        tags=[route[1:], 'no_tokens_required'],
        response_model=schema.UserData
    )
    def register(user_regis: schema.UserRegis):
        seed(int(time())) # gen new random seed from current unix time
        new_user = schema.UserPwd(**user_regis.dict())
        salt = ''.join(choice(ascii_letters+digits+punctuation) for _ in range(50))
        hash = SHA512.new((new_user.password+salt).encode('ascii'))
        new_user.email = new_user.email.lower()
        new_user.password = hash.hexdigest()
        new_user.password_salt = salt
        check_penname = controller.get_user_from_penname(db, new_user.penname)
        check_email = controller.get_user_from_email(db, new_user.email)
        if check_email or check_penname:
            raise HTTPException(status_code=400, detail='penname or email are already taken')
        return controller.create_user(db, new_user)

    @router.post(
        route+'/signin',
        tags=[route[1:], 'no_tokens_required'],
        responses={
            **gen_res_dict(status_codes=[401]),
            200:{
                'description':'Return access token and token type.',
                'content': {
                    'application/json': {
                        'example': {
                            'access_token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJyb2xlIjp0cnVlLCJleHAiOjE2MTU3NTczMDkuNDI2NTMwNH0.FARjxsN4Z3wU7u7DhYP3BJn_E1y0y25c9-w1FZNSuks',
                            'token_type':'bearer'
                        }
                    }
                }
            }
        }
    )
    def signin(signin_data:schema.UserSignin):
        lookup_user = controller.get_user_from_email(db, signin_data.email)
        if lookup_user:
            hashed_pwd = SHA512.new((signin_data.password+lookup_user.password_salt).encode('ascii')).hexdigest()
            if hashed_pwd == lookup_user.password:
                token = sign_token(
                    user_id=lookup_user.id,
                    role=lookup_user.role_id,
                    exp=time()+TOKEN_DURATION
                )
                # need to collect login log
                return token
            else:
                return HTTPException(status_code=401, detail='Password mismatch.')
        else:
            return HTTPException(status_code=401, detail='User not found.')

    @router.get(
        route+'/all',
        tags=[route[1:], 'admin_token'],
        response_model=List[schema.UserData]
    )
    def list_all_user(
        token: str = Depends(JWTBearer(verify_admin=True)),
        offset: int = 0,
        limit: int = 100):
        # need to collect query log
        users_data = [schema.UserData(**user.dict()) for user in controller.get_users(db, offset, limit)]
        return users_data

    @router.put(
        route,
        tags=[route[1:], 'user_token'],
        responses={
            **gen_res_dict(status_codes=[500]),
            200: {
                'description': 'Operation result.',
                'content': {
                    'application/json': {
                        'example': {
                            'success': True
                        }
                    }
                }
            }
        }
    )
    def update_user(
        confirmed_pwd: str,
        update_info: schema.UserPwd,
        response: Response,
        token: str = Depends(JWTBearer())):
        # need to collect update log
        response_status, detail_msg = 0, ''
        decoded = decode_token(token)
        lookup_user = controller.get_user(db, decoded['user_id'])
        hashed_pwd = SHA512.new((confirmed_pwd+lookup_user.password_salt).encode('ascii')).hexdigest()
        try:
            if not lookup_user:
                response_status, detail_msg = 401, 'User not found.'
                raise LookupError('Lookup failed')
            if lookup_user.password != hashed_pwd:
                response_status, detail_msg = 401, 'Invalid confirm password.'
                raise LookupError('Lookup failed')
            else:
                    update_info.password_salt = None
                    update_info.create_dt = None
                    update_info.rank = None
                    if update_info.email:
                        if controller.get_user_from_email(db, update_info.email):
                            response_status, detail_msg = 400, 'Email has already taken.'
                            raise LookupError(detail_msg)
                        else:
                            update_info.email = update_info.email.lower()
                    if update_info.penname:
                        if controller.get_user_from_penname(db, update_info.penname):
                            response_status, detail_msg = 400, 'Penname has already taken.'
                            raise LookupError(detail_msg)
                    if update_info.password:
                       update_info.password = SHA512.new((update_info.password+lookup_user.password_salt).encode('ascii')).hexdigest()
                    if update_info.role_id:
                        if int(lookup_user.role.permission) > 0:
                            update_info.role_id = lookup_user.role_id # Ordinary user has no permission to update his own role
                    if not controller.edit_user(db, lookup_user, update_info):
                        response_status, detail_msg = 500, 'Internal server error.'
                        raise Exception
        except LookupError as e:
            response.status_code = response_status
            return {'success': False, 'detail': detail_msg }
        except Exception as e:
            print(e)
            response.status_code = response_status
            return {'success': False, 'detail': detail_msg }
        else:
            response.status_code = 200
            return {'success': True, 'detail': ''}

    @router.put(
        route+'/alter',
        tags=[route[1:], 'admin_token'],
        responses={
            **gen_res_dict(status_codes=[500]),
            200: {
                'description': 'Operation result.',
                'content': {
                    'application/json': {
                        'example': {
                            'success': True
                        }
                    }
                }
            }
        }
    )
    def alter_user_info(user_id:int, update_info: schema.UserData, token: str = Depends(JWTBearer(verify_admin=True))):
        # need to collect alter log
        lookup_user = controller.get_user(db, user_id)
        update_info.password_salt = None
        update_info.create_dt = None
        if update_info.email:
            if not controller.get_user_from_email(db, update_info.email):
                return {'success': False, 'detail': 'Email has already taken.'}
            else:
                update_info.email = update_info.email.lower()
        if update_info.penname:
            if not controller.get_user_from_penname(db, update_info.penname):
                return {'success': False, 'detail': 'Penname has already taken.'}
        update_res = controller.alter_user(db, lookup_user, update_info)
        return {'success': True, 'detail': ''} if update_res else {'success': False, 'detail': 'internal server error'}

    @router.delete(
        route,
        tags=[route[1:], 'admin_token', 'user_token'],
        responses={
            **gen_res_dict(status_codes=[500]),
            200: {
                'description': 'Operation result.',
                'content': {
                    'application/json': {
                        'example': {
                            'success': True,
                            'detail': 'deleted'
                        }
                    }
                }
            }
        }
    )
    def delete_user(response:Response, user_id:int = None, token: str = Depends(JWTBearer(verify_admin=False))):
        # need to collect delete log
        decoded = decode_token(token)
        if decoded['role'] == 1: # request came from administrator token
            if not user_id:
                return {'success': False, 'detail': 'user_id is required'}
            else:
                user = controller.get_user(db, user_id)
        else:
            user = controller.get_user(db, decoded['user_id'])
        if user:
            if controller.delete_user(db, user):
                response.status_code = 200
                return {'success': True, 'detail': 'deleted'}
            else:
                response.status_code = 500
                return {'success': False, 'detail': 'internal server error'}
        else:
            response.status_code = 400
            return {'success': False, 'detail': 'user not found'}

    @router.get(
        route,
        tags=[route[1:], 'user_token'],
        response_model=schema.UserPrivateData
    )
    def get_user_data(token: str = Depends(JWTBearer())):
        decoded = decode_token(token)
        # need to collect get_data log
        try:
            user = controller.get_user(db, decoded['user_id'])
            if user:
                return schema.UserPrivateData(**user.dict())
            else:
                return HTTPException(status_code=404, detail='User not found.')
        except Exception as e:
            return HTTPException(status_code=500, detail=f'Error: {e}')

    @router.post(
        route+'/images',
        tags=[route[1:], 'admin_token', 'user_token'],
        status_code=201,
        responses={
            **gen_res_dict(status_codes=[413, 415]),
            201:{
                'description': 'profile image created.',
                'content': {
                    'application/json': {
                        'example': { 'img_url': 'images/qeXjK599XJ.jpg' }
                    }
                }
            }
        }
    )
    async def create_profile_images( image: UploadFile = File(...), token: str = Depends(JWTBearer(verify_admin=False))):
        # Validate input file
        seed(time())
        payload = decode_token(token)
        lookup_user = controller.get_user(db, payload['user_id'])
        if not lookup_user:
            raise HTTPException(status_code=400, detail='user not found.')

        file = await image.read()
        if image.content_type not in ACCEPTABLE_MIME_TYPES:
            raise HTTPException(status_code=415, detail='Accept only [{}] MIME types.'.format(', '.join(ACCEPTABLE_MIME_TYPES)))
        elif getsizeof(file) < 50000: # if filesize less than 50KB 
            raise HTTPException(status_code=413, detail='Image size must greater than 50KB')
        elif getsizeof(file) >= 52428800: # if filesize greater than 50MB
            raise HTTPException(status_code=413, detail='Image size must less than 50MB.')
        else:
            name = ''.join(choice(ascii_letters+digits) for _ in range(15)) + image.filename[image.filename.rfind('.'):]
            image_url = f'/images/{name}'
            update_info = schema.UserPwd(image_url=image_url)
            if controller.edit_user(db, lookup_user, update_info):
                # write file into disk
                with open(f'static/images/{name}', 'wb') as f:
                    f.write(file)
                return {'img_url': image_url}
