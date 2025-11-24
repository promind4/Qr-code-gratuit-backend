from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Registration
class UserRegister(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)

# Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# User response (what we send to frontend)
class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    email_verified: bool
    oauth_provider: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True  # For SQLAlchemy models

# Password reset request
class PasswordResetRequest(BaseModel):
    email: EmailStr

# Password reset confirmation
class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)

# Email verification
class EmailVerification(BaseModel):
    token: str
