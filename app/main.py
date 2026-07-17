from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from app import schemas
from app.db import get_db
from app import crud, db, models, auth
from app.routers import auth_endpoints

app = FastAPI()
app.include_router(auth_endpoints.router, prefix="/auth", tags=["auth"])


@app.get("/")
async def root():
    return {"welcome": "Welcome to the FastAPI application!"}

@app.get("/health")
async def health_check():
    return {"health": "ok"}

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)



