from pydantic import BaseModel, Field, EmailStr, constr


class UserCreate(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8)
    
    
    
class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8)



class Token(BaseModel):
    access_token: str
    token_type: str

    

class TokenData(BaseModel):
    email: EmailStr | None = None

    