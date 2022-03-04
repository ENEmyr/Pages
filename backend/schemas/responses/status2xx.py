from pydantic import BaseModel

STATUS200_DESC = 'Ok.'
STATUS201_DESC = 'Created.'

class Status200(BaseModel):
    detail: str
    class Config:
        schema_extra ={
            'example': {
                'detail': 'Request Successful'
            }
        }

class Status201(BaseModel):
    detail: str
    class Config:
        schema_extra ={
            'example': {
                'detail': 'User Created.'
            }
        }
