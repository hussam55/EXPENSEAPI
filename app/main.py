from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from app import schemas
from app.db import get_db
from app import crud, db, models, auth
from app.routers import auth_endpoints
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings 

app = FastAPI()
app.include_router(auth_endpoints.router, prefix="/auth", tags=["auth"])


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"welcome": "Welcome to the FastAPI application!"}

@app.get("/health")
async def health_check():
    return {"health": "ok"}
