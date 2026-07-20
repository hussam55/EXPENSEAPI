from pydantic import BaseModel, Field, EmailStr, constr, ConfigDict
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

    



class Token(BaseModel):
    access_token: str
    token_type: str

    

    