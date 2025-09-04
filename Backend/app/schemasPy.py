from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum

class ContractStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    
class MarketingStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    
class OperationStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class FinanceStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    
class TransactionType(str, Enum):
    INVOICE = "invoice"
    PAYMENT = "payment"
    CREDIT_NOTE = "credit_note"
    DEBIT_NOTE = "debit_note"
    ADVANCE = "advance"
    REFUND = "refund"
    
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: Dict[str, Any]
    
class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None
    exp: Optional[int] = None
    
class UserLogin(BaseModel):
    username: str
    password: str
    mfa_code: Optional[str] = None
    
class MFASetup(BaseModel):
    secret: str
    qr_code: str
    
class MFAVerify(BaseModel):
    mfa_code: str
    backup_code: Optional[str] = None
    
class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    
class UserCreate(UserBase):
    password: str
    role_id: int
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role_id: Optional[str] = None
    is_active: Optional[str] = None
    
class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str
    
class UserResponse(UserBase):
    id: int
    role_id: int
    role_name: Optional[str] = None
    is_active: bool
    mfa_enabled: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class AgencyBase(BaseModel):
    name: str
    code: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    contact_person: Optional[str] = None
    tax_id: Optional[str] = None
    payment_terms: Optional[int] = None
    credit_limit: Optional[float] = None
    status: Optional[str] = "active"
    
class AgencyCreate(AgencyBase):
    pass

class AgencyUpdate(AgencyBase):
    pass

class AgencyResponse(AgencyBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class ContractBase(BaseModel):
    contract_number: str
    agency_id: int
    title: str
    description: Optional[str] = None
    contract_type: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    total_value: Optional[float] = None
    currency: str = "IDR"
    payment_terms: Optional[str] = None
    
class ContractCreate(ContractBase):
    pass

class ContractUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    contract_type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[str] = None
    total_value: Optional[float] = None
    currency: Optional[str] = None
    payment_terms: Optional[str] = None
    marketing_remarks: Optional[str] = None
    operation_remarks: Optional[str] = None
    finance_remarks: Optional[str] = None
    
class ContrctResponse(ContractBase):
    id: int
    status: ContractStatus
    marketing_user_id: Optional[int] = None
    operation_user_id: Optional[int] = None
    finance_user_id: Optional[int] = None
    marketing_remarks: Optional[str] = None
    operation_remarks: Optional[str] = None
    finance_remarks: Optional[str] = None
    marketing_status: MarketingStatus
    operation_status: OperationStatus
    finance_status: FinanceStatus
    created_by: Optional[int] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None