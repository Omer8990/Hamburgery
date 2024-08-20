from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: SecretStr


class UserRead(UserBase):
    user_id: int

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    password: Optional[SecretStr] = None
