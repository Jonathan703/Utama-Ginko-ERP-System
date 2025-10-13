from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
from app.models import UserRole,  ContractStatus, InvoiceStatus


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
    mfa_required: Optional[bool] = False
    
class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None
    exp: Optional[int] = None
    
class UserLogin(BaseModel):
    username: str
    password: str
    mfa_code: Optional[str] = None
    
class MFASetupResponse(BaseModel):
    secret: str
    qr_code_uri: str

class MFAVerify(BaseModel):
    otp: str
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
    cancelled_by: Optional[int] = None
    cancelled_at: Optional[datetime] = None
    cancelled_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class ShipmentBase(BaseModel):
    shipment_number: str
    contract_id: int
    agency_id: int
    vessel_name: Optional[str] = None
    voyage_number: Optional[str] = None
    cargo_type: Optional[str] = None
    cargo_description: Optional[str] = None
    quantity: Optional[float] = None
    unit_of_measure: Optional [str] = None
    loading_port: Optional[str] = None
    discharge_port: Optional[str] = None
    estimated_arrival: Optional[str] = None
    actual_of_arrival: Optional[str] = None
    special_instructions: Optional[str] = None
    artificial_constrac: Optional[str] = None
    
class ShipmentCreate(ShipmentBase):
    pass

class ShipmentUpdate(BaseModel):
    vessel_name: Optional[str] = None
    voyage_number: Optional[float] = None
    cargo_type: Optional[str] = None
    cargo_description: Optional[str] = None
    quantity: Optional[float] = None
    unit_of_measure: Optional[str] = None
    loading_port: Optional[str] = None
    discharge_port: Optional[str] = None
    loading_port: Optional[date] = None
    discharge_date: Optional[date] = None
    estimated_arrival: Optional[date] = None
    actual_arrival: Optional[date] = None
    status: Optional[str] = None
    operation_remarks: Optional[str] = None
    marketing_remarks: Optional[str] = None
    special_instruction: Optional[str] = None
    
class ShipmentResponse(ShipmentBase):
    id: int
    status: str
    operation_remarks: Optional[str] = None
    marketing_remakrs: Optional[str] = None
    special_instruction: Optional[str] = None
    
class ShipmentResponse(ShipmentBase):
    id: int
    status: str
    operation_remarks: Optional[str] = None
    marketing_remarks: Optional[str] = None
    created_by: Optional[int] = None
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class FinancialTransactionBase(BaseModel):
    transaction_number: str
    contract_id: Optional[int] = None
    shipment_id: Optional[int] = None
    agency_id: Optional[int] = None
    transaction_type: TransactionType
    invoice_id: Optional[int] = None
    amount: float
    currency: str = "IDR"
    exchange_rate: Optional[float] = 1.0
    due_date: Optional[date] = None
    payment_date: Optional[date] = None
    payment_method: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    tax_rate: Optional[float] = 0.0
    discount_amount: Optional[float] = 0.0
    
class FinancialTransactionCreate(FinancialTransactionBase):
    pass

class FinancialTransactionpdate(BaseModel):
    transaction_type: Optional[TransactionType] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    exchange_rate: Optional[float] = None
    due_date: Optional[date] = None
    payment_date: Optional[date] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    tax_rate: Optional[float] = None
    discount_amount: Optional[float] = None

class FinancialTransactionResponse(FinancialTransactionBase):
    id: int
    amount_local: Optional[float] = None
    tax_amount: Optional[float] = None
    discount_amount: float
    status: str
    reminder_sent: Optional[bool] = None
    reminder_count: Optional[int] = None
    last_reminder_date: Optional[datetime] = None
    created_by: Optional[int] = None
    approved_by: Optional[int] = None
    cancelled_by: Optional[int] = None
    cancelld_reason: Optional[str] = None
    created_at = datetime
    updated_at = datetime
    
    class Config:
        from_attributes = True
        
class WorkflowAction(BaseModel):
    entity_type: str
    entity_id: int
    action: str
    from_status: Optional[str] = None
    to_status: Optional[str] = None
    department: Optional[str] = None
    remark: Optional[str] = None
    
class WorkflowHistoryResponse(WorkflowAction):
    id: int
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class DocumentBase(BaseModel):
    document_name: str
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    category: Optional[str] = None
    description: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocomentResponse(DocumentBase):
    id: int
    file_path: str
    file_size: Optional[int] = None
    mime_type: Optional[int] = None
    uploaded_by: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class NotificationBase(BaseModel):
    title: str
    message: str
    type: str = "info"
    priority: int = 1
    related_entity_type: Optional[str] = None
    related_entity_type: Optional[str] = None
    action_url: Optional[str] = None
    
class NotificationCreate(NotificationBase):
    user_id: int

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
class UserStatistics(BaseModel):
    total_users: int
    active_users: int
    inactive_users: int
    role_distribution: Dict[str, int]
    
class FinancialStatstics(BaseModel):
    total_transaction: int
    total_revenue: float
    outstanding_payments: float
    overdue_payments: int
    transactions_by_type: Dict[str, int]

class ContractStatistics(BaseModel):
    total_contracts: int
    contracts_by_status: Dict[str, int]
    contracts_by_type: Dict[str, int]
    contracts_by_month: Dict[str, int]; date
    description: Optional[str]
