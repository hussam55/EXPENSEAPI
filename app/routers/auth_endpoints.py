from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, crud, auth
from app.db import get_db


router = APIRouter()

@router.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already exists"
        )
    return crud.create_user(db, user)


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Find the user in the database (FastAPI OAuth2 uses 'username' by default, which we map to our email)
    user = crud.get_user_by_username(db, user_credentials.username)

    # 2. If user doesn't exist, throw an error
    if not user or not auth.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )


    # 4. If everything is correct, create the token
    # We embed the user's ID inside the token so we know who they are on future requests
    access_token = auth.create_access_token(data={"user_id": user.id})

    # 5. Return the token to the user
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: schemas.UserCreate = Depends(auth.get_current_user)):
    return current_user