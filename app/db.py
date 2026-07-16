from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = "postgresql://expense_user:password@localhost/expense_db"

# Create the database engine
# Note: We removed connect_args={"check_same_thread": False} as it is only for SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session maker to manage database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()