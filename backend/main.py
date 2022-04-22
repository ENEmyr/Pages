from typing import Optional
from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database.database import sess, engine

from rich import pretty
from rich.traceback import install 
from rich import print
pretty.install()
install()

# Import all routes
from routes import role, user, search, user_follow

ROLES = ('administrator', 'tester',
         'moderator', 'editor',
         'verified_user', 'user')

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
    version="0.3.1-alpha",
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
    from models import role, user, user_follow
    try:
        role.Base.metadata.create_all(bind=engine)
        user.Base.metadata.create_all(bind=engine)
        user_follow.Base.metadata.create_all(bind=engine)
        sess = get_db()
        roles = sess.query(role.Role).all()
        if len(roles) != len(ROLES):
            from schemas.role import RoleCreate as RoleCreateSchema
            from controllers.role import create_role as controller_create_role
            for permission, name in enumerate(ROLES):
                new_role = RoleCreateSchema()
                new_role.name = name
                new_role.permission = str(permission)
                res = controller_create_role(sess, new_role)
                print(f'[bold green] New Role Created : {res.name} with permission {res.permission}')
    except Exception as e:
        print(e)
        exit(0)

role.export_routes('/roles', server, get_db())
user.export_routes('/users', server, get_db())
search.export_routes('/search', server, get_db())
user_follow.export_routes('/follow', server, get_db())
