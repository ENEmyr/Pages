from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Response 

from schemas import search as search_schema
from controllers import search as controller
from helpers.auth_bearer import JWTBearer

def export_routes(route:str, router:FastAPI, db:Session):
    @router.get(
        route, 
        tags=[route[1:], 'no_tokens_required'],
        response_model=search_schema.SearchItems
    )
    def search(keyword: str, offset:int = 0, limit:int = 100):
        return controller.search_for_users_and_pages(db, keyword, offset, limit)
