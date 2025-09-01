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
    finance_user = relationship("User", foreign_keys=[finance_user_id])
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_contracts")
    approver = relationship("User", foreign_keys=[approved_by], back_populates="approved_contracts")
    canceller = relationship("User", foreign_keys=[cancelled_by], back_populates="cancelled_contracts")
    shipment = relationship("Shipment", back_populates="contract")
    transaction = relationship("FinancialTransaction", back_populates="contract")
    
class Shipment(Base):
    __tablename__ = "shipment"
    
    id = Column(Integer, primary_key=True, index=True)
    shipment_number = Column(String(50), unique=True, nullable=False)
    contract_id = Column(Integer, ForeignKey("contract.id"))
    agency_id =  Column(Integer, ForeignKey("agency.id"))
    vessel_name = Column(String(100), ForeignKey("agency.id"))
    voyage_number = Column(String(50))
    cargo_type = Column(String(100))
    cargo_description = Column(Text)
    quantity = Column(Numeric(12, 2))
    unit_of_measure = Column(String(20))
    loading_port = Column(String(100))
    discharge_port = Column(String(100))
    loading_date = Column(Date)
    discharge_date = Column(Date)
    estimated_arrival = Column(Date)
    actual_arrival = Column(Date)
    status = Column(String(30), default="planned")
    operation_remarks = Column(Text)
    marketing_remarks = Column(Text)
    special_instructions = Column(Text)
    created_by = Column(Integer, ForeignKey("user.id"))
    assigned_to = Column(Integer, ForeignKey("user.id"))
    created_at = Column(datetime(timezone=True), server_default=func.now())
    updated_at = Column(datetime(timezone=True), server_default=func.now())
    
    #relationship
    contract = relationship("Contract", back_populates="shipment")
    agency = relationship("Agency", back_populates="shipment")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_shipment")
    assignee = relationship("User", foreign_keys=[assigned_to], back_populates="assigned_shipment")
    transaction = relationship("FinancialTransaction", back_populates="shipment")
    
class FinancialTransaction(Base):
    __tablename__ = "financial_transaction"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_number = Column(String(50), unique=True, nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    shipment_id = Column(Integer, ForeignKey("shipment.id"))
    agency_id = Column(Integer, ForeignKey("agencies.id"))
    transaction_type = Column(String(30), nullable=False)
    invoice_id = Column(Integer)
    amount = Column(Numeric(15, 2))
    currency = Column(String(3), default="IDR")
    exchange_rate = Column(Numeric(10, 6), default=1.000000)
    amount_local = Column(Numeric(15, 2))
    due_date = Column(Date)
    payment_date = Column(Date)
    status = Column(String(20), default ="pending")
    preference_method = Column(String(30))
    description = Column(Text)
    notes = Column(Text)
    tax_amount = Column(Numeric(15, 2), default=0.00)
    tax_rate = Column(Numeric(5, 2), default=0.00)
    discount_amount = Column(Numeric(15, 2), default=0.00)
    total_amount = Column(Numeric(15, 2), bullable=False)
    created_by = Column(Integer, ForeignKey("user.id"))
    approved_by = Column(Integer, ForeignKey("user.id"))
    approved_at = Column(datetime(timezone=True))
    cancelled_by = Column(Integer, ForeignKey("user.id"))
    cancelled_at = Column(datetime(timezone=True))
    cancelled_reason = Column(Text)
    reminder_sent = Column(Boolean, default=False)
    reminder_count = Column(Integer, default=0)
    last_reminder_date = Column(datetime(timezone=True))
    created_at = Column(datetime(timezone=True), server_default=func.now())
    updated_at = Column(datetime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    contract = relationship("Contract", back_populates="transaction")
    shipment = relationship("Shipment", back_populates="transaction")
    agency = relationship("Agency", back_populates="transaction")
    creator = relationship("User", foreignkey=[created_by], back_populates="created_transaction")
    approver
    