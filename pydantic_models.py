from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import BaseModel


class Settings(BaseSettings):
    sqlalchemy_uri: str


class UserModel(BaseModel):
    username: str
    password: str


class UserResponse(UserModel):
    id: str
    token: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ContactModel(BaseModel):
    name: str
    phone_number: str
    address: Optional[str] = None
    email: Optional[str] = None


class ContactModelResponce(ContactModel):
    id: str
    user_id: str

settings = Settings()
