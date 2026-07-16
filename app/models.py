from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    expenses = relationship("Expense", back_populates="owner")


class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    # Added index=True to speed up user dashboard queries
    owner_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    
    # Changed to Numeric for accurate currency storage (e.g., 10 digits total, 2 decimal places)
    amount = Column(Numeric(10, 2), nullable=False)
    
    description = Column(String(255))
    category = Column(String(50), nullable=False)
    date = Column(Date, default=date.today, nullable=False)

    owner = relationship("User", back_populates="expenses")