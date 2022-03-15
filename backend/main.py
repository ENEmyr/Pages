from typing import Optional
from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database.database import sess, engine

from rich import pretty
from rich.traceback import install 
pretty.install()
install()

# Import all routes
from routes import role, user

def get_db():
    db = sess()
    try:
        return db
    finally:
        db.close()

tags_metadata = [
    {
        'name': 'users',
        'description': 'Operations with users table.'
    },
    {
        'name': 'admin_token',
        'description': 'Required admin token to operate any operations.'
    },
    {
        'name': 'user_token',
        'description': 'Required user token to operate any operations.'
    },
    {
        'name': 'no_tokens_required',
        'description': 'No token required to operate any operations.'
    }
]
origins = [
    '*'
]
server = FastAPI(
    title="PagesREST",
    description="RESTful API written in FastAPI for used as a backend for Pages a new social network platform for short article.",
    version="0.2.1-alpha",
    openapi_tags=tags_metadata
)
server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
server.mount('/images', StaticFiles(directory='static/images'), name='images')

@server.get('/')
def get_root(request: Request):
    return RedirectResponse(url=f'{request.url}docs')

@server.on_event('startup')
def startup():
    from models import role, user
    try:
        role.Base.metadata.create_all(bind=engine)
        user.Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(e)
        exit(0)

role.export_routes('/roles', server, get_db())
user.export_routes('/users', server, get_db())
