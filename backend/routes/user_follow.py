from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Response
from typing import List

from helpers.generate_responses_dict import gen_res_dict
from helpers.auth_bearer import JWTBearer
from helpers.auth_handler import decode_token
from schemas import user as user_schema
from schemas import user_follow as schema
from controllers import user_follow as controller

def export_routes(route:str, router:FastAPI, db:Session):
    @router.post(
        route,
        status_code=201,
        tags=[route[1:], 'user_token'],
        response_model=List[user_schema.UserSearch]
    )
    def follow(response:Response, follow_id: int, token: str = Depends(JWTBearer(verify_admin=False))):
        decoded = decode_token(token)
        if decoded['user_id'] == follow_id:
            response.status_code = 400
            return
        user_follow = schema.UserFollow(user_id=decoded['user_id'], follow_id=follow_id)
        return controller.follow(db, user_follow)

    @router.delete(
        route,
        tags=[route[1:], 'user_token'],
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
    def unfollow(response:Response, follow_id:int, token: str = Depends(JWTBearer(verify_admin=False))):
        # need to collect delete log
        decoded = decode_token(token)
        del_status = controller.unfollow(db, decoded['user_id'], follow_id)
        if del_status:
            response.status_code = 200
            return {'success': True, 'detail': 'deleted'}
        else:
            response.status_code = 500
            return {'success': False, 'detail': 'internal server error'}

    @router.get(
        route+'/following',
        tags=[route[1:], 'user_token'],
        response_model=List[user_schema.UserSearch]
    )
    def get_user_followings(token: str = Depends(JWTBearer(verify_admin=False))):
        decoded = decode_token(token)
        # need to collect get_following log
        try:
            followings = controller.get_following(db, decoded['user_id'])
            return followings
        except Exception as e:
            return HTTPException(status_code=500, detail=f'Error: {e}')

    @router.get(
        route+'/follower',
        tags=[route[1:], 'user_token'],
        response_model=List[user_schema.UserSearch]
    )
    def get_user_followers(token: str = Depends(JWTBearer(verify_admin=False))):
        decoded = decode_token(token)
        # need to collect get_followers log
        try:
            followers = controller.get_follower(db, decoded['user_id'])
            return followers
        except Exception as e:
            return HTTPException(status_code=500, detail=f'Error: {e}')
