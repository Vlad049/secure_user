from typing import Annotated, Optional
import string
import re

from pydantic_settings import BaseSettings
from pydantic import BaseModel, EmailStr, Field, field_validator


class Settings(BaseSettings):
    sqlalchemy_uri: str


class UserModel(BaseModel):
    username: Annotated[str, Field(..., description="Логін користувача")]
    password: Annotated[str, Field(..., min_length=8, description="Пароль користувача")]

    @field_validator("password")
    def password_validator(cls, value: str):
        is_upper = False
        is_lower = False
        is_digit = False
        is_punctuation = False

        for char in value:
            if not is_upper and char.isupper():
                is_upper = True

            if not is_lower and char.islower():
                is_lower = True

            if not is_digit and char.isdigit():
                is_digit = True

            if not is_punctuation and char in string.punctuation:
                is_punctuation = True

        if all([is_upper, is_lower, is_digit, is_punctuation]):
            return value
        
        raise ValueError("Мінімум 8 символів, одну велику та маленьку літеру та обин спецсимвол")


class UserResponse(UserModel):
    id: Annotated[int, Field(0, description="Айді користувача")]
    token: Annotated[Optional[str], Field(None, description="Токен користувача")]


class Token(BaseModel):
    access_token: Annotated[str, Field(..., description="Токен користувача")]
    token_type: Annotated[str, Field("bearer", description="Тип токену користувача")]


class ContactModel(BaseModel):
    name: Annotated[str, Field(None, description="Ім'я користувача")]
    phone_number: Annotated[Optional[str], Field(None, description="Номер телефону у форматі '+38(099)123-45-78'", examples=['+38(099)123-45-78'])]
    address: Annotated[Optional[str], Field(None, description="Адреса користувача")]
    email: Annotated[Optional[EmailStr], Field(None, description="Електронна пошта користувача")]

    @field_validator("phone_number")
    def phone_number_validator(cls, value: Optional[str]):
        if value and not re.search(r"\+38\(0\d{2}\)\d{3}-\d{2}-\d{2}", value):
            raise ValueError("Номер телефону повинен бути у форматі '+38(099)123-45-78'")
        return value


class ContactModelResponce(ContactModel):
    id: Annotated[int, Field(0, description="Порядковий номер")]
    user_id: Annotated[int, Field(0, description="Айді користувача")]

settings = Settings()
