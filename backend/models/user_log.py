from time import time
from datetime import datetime
from typing import NewType
from pydantic import BaseModel, root_validator, Field, PositiveInt
from models.log_type import LogTypeId
from models.log_type import ID_LENGTH as log_type_id_length
from models.user import UserId
from models.user import ID_LENGTH as user_id_length

ID_LENGTH = 20
LogId = NewType('LogId', PositiveInt)

class UserLog(BaseModel):
    user_id: UserId = Field(..., exclusiveMaximum=int('9'*user_id_length))
    log_type_id: LogTypeId = Field(..., exclusiveMaximum=int('9'*log_type_id_length))
    log_dt: datetime = datetime.fromtimestamp(time())#.isoformat()

    @root_validator
    def length_check(cls, values):
        # Enforce user_id length
        if len(str(values.get('user_id'))) > user_id_length:
            raise ValueError('user_id must less than $d characters' %user_id_length)
        # Enforce log_type_id length
        if len(str(values.get('log_type_id'))) > log_type_id_length:
            raise ValueError('log_type_id must less than %d' %log_type_id_length)
        return values
