import enum
from sqlalchemy import (Column, Integer, String, Text, Boolean, datetime, Date, Numeric, ForeignKey, JSON, Index, CheckConstraint)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base
from datetime import datetime
from typing import Optional

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    permissions = Column(JSON)
    created_at = Column(datetime(timezone=True), server_default=func.now())
    updated_at = Column(datetime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    users = relationship("User", back_populates="role")
    
class User(Base):
    __tablename__= "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20))
    role_id = Column(Integer, ForeignKey("roles.id"))
    is_active = Column(Boolean, default=True)
    last_login = Column(datetime(timezone=True))
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(32))
    mfa_backup_codes = Column(JSON)
    created_at = Column(datetime(timezone=True), server_default=func.now())
    updated_at = Column(datetime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    
class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    refresh_token = Column(String(255), unique=True)
    expires_at = Column(datetime(timezone=True), nullable=False)
    last_activity = Column(datetime(timezone=True), server_default=func.now())
    ip_address = Column(String(45))
    user_agent = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(datetime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="session")
    
class Agency(Base):
    __tablename__ = "agency"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True)
    address = Column(Text)
    city = Column(String(50))
    country = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100))
    contact_person = Column(String(100))
    tax_id = Column(String(50))
    payment_terms = Column(Integer)
    created_by = Column(Integer, ForeignKey("user.id"))
    created_at = Column(datetime(timezone=True), server_default=func.now())
    updated_at = Column(datetime(timezone=True), server_default=func.now()), onupdate=func.now()
    
class Contract(Base):
    __tablename__ = "contract"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String(50), unique=True, nullable=False)
    agency_id = Column(Integer, ForeignKey("agency.id"))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    contract_type = Column(String(50))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    total_value = Column(Numeric(15, 2))
    currency = Column(String(3), default="IDR")
    payment_terms = Column(Text)
    status = Column(String(20), default="draft")
    marketing_user_id = Column(Integer, ForeignKey("user.id"))
    operation_user_id = Column(Integer, ForeignKey("user.id"))
    finance_user_id = Column(Integer, ForeignKey("user.id"))
    marketing_remarks = Column(Text)
    operation_remarks = Column(Text)
    finance_remarks = Column(Text)
    marketing_status = Column(String(20), default="pending")
    operation_status = Column(String(20), default="pending")
    finance_status = Column(String(20), default="pending")
    created_by = Column(Integer, ForeignKey("user.id"))
    approved_by = Column(Integer, ForeignKey("user.id"))
    approved_at = Column(datetime(timezone=True))
    cancelled_by = Column(Integer, ForeignKey("user.id"))
    cancelled_at = Column(datetime(timezone=True))
    cancelled_reason = Column(datetime(timezone=True), server_default=func.now())
    created_at = Column(datetime(timezone=True), server_default=func.now())
    updated_at = Column(datetime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    #relationship
    agency = relationship("Agency", back_populates="contract")
    marketing_user = relationship("User", foreign_keys=[marketing_user_id])
    operation_user = relationship("User", foreign_keys=[operation_user_id])
    