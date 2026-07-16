from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from app import schemas
from app.db import get_db
from app import crud

app = FastAPI()



@app.get("/health")
async def health_check():
    return {"health": "ok"}

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already exists"
        )
    return crud.create_user(db, user)
    

