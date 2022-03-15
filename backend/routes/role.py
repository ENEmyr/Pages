from typing import List 

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Response, status

from helpers.generate_responses_dict import gen_res_dict
from schemas import role as schema
from controllers import role as controller
from helpers.auth_bearer import JWTBearer

def export_routes(route:str, router:FastAPI, db:Session):
    @router.post(
        route, 
        response_model=schema.Role,
        tags=[route[1:], 'admin_token']
    )
    def create_role(role: schema.RoleCreate, token: str = Depends(JWTBearer(verify_admin=True))):
        role.name = role.name.lower()
        db_role = controller.get_role_by_name(db, role.name)
        if db_role:
            raise HTTPException(status_code=400, detail='name already registered')
        return controller.create_role(db, role)

    @router.get(
        route, 
        tags=[route[1:], 'no_tokens_required'],
        response_model=schema.Role
    )
    def get_role_by_id(role_id:int):
        return controller.get_role(db, role_id)

    @router.get(
        route+'/name', 
        tags=[route[1:], 'no_tokens_required'],
        response_model=schema.Role
    )
    def get_role_by_name(role_name:str):
        return controller.get_role_by_name(db, role_name.lower())

    @router.get(
        route+'/all', 
        tags=[route[1:], 'no_tokens_required'],
        response_model=List[schema.Role]
    )
    def list_all_role(offset:int = 0, limit:int = 100):
        return controller.get_roles(db, offset, limit)

    @router.put(
        route,
        response_model=schema.Role,
        tags=[route[1:], 'admin_token']
    )
    def update_role(role_id:int, update_info:schema.RoleCreate, token: str = Depends(JWTBearer(verify_admin=True))):
        db_role = controller.get_role(db, role_id)
        return controller.edit_role(db, db_role, update_info)

    @router.delete(
        route, 
        responses={**gen_res_dict(status_codes=[200, 400])},
        tags=[route[1:], 'admin_token']
    )
    def delete_role(role_id:int, response:Response, token: str = Depends(JWTBearer(verify_admin=True))):
        db_role = controller.get_role(db, role_id)
        successful = controller.delete_role(db, db_role)
        if not successful:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='error occurs')
        else:
            response.status_code = status.HTTP_200_OK
        return {"status": "deleted"}
