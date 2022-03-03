from typing import Optional
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import db

# Import all routes
from routes import user

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
def get_root():
    return {"Hello": "HelloWorld"}

@server.on_event('startup')
async def startup():
    await db.connect()

@server.on_event('shutdown')
async def shutdown():
    await db.disconnect()

user.export_routes('/users', server, db)
