from typing import List, Union, Optional, Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status, Path, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
import uvicorn

from pydantic_models import UserModel, UserResponse, ContactModel, ContactModelResponce, Token
from models import get_db, User, Contact


app = FastAPI()


async def get_user(db: AsyncSession=Depends(get_db), token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    query = select(User).filter_by(token=token)
    result = await db.execute(query)
    user: Optional[User] = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не вірний токен")
    
    return user


@app.post(
    "/users/",
    status_code=status.HTTP_201_CREATED, response_model=UserResponse,
    tags=["Users"], 
    summary="Реєстрація користувача",
    description="Для реєстрації введіть свій логін та пароль",
    name="Sign up"
)
async def create_user(user_model: UserModel, db: AsyncSession = Depends(get_db)):
    user = User(**user_model.model_dump())
    db.add(user)
    await db.commit()
    return user


@app.post(
        "/token/",
        status_code=status.HTTP_200_OK, response_model=Token
    )
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    query = select(User).filter_by(username=form_data.username, password=form_data.password)
    result = await db.execute(query)
    user: Optional[User] = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Логін або пароль не вірний")
    
    token = uuid4().hex
    user.token = token
    await db.commit()
    return dict(access_token=token)


@app.post(
    "/contacts/",
    status_code=status.HTTP_201_CREATED,
    response_model=ContactModelResponce,
    tags=["Contact"],
    summary="Створити новий контакт",
    description="Для додавання нового контакту передайте токен та необхідні поля"
)
async def add_contact(
    contact_model: ContactModel,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    contact = Contact(**contact_model.model_dump(), user_id=user.id)
    db.add(contact)
    await db.commit()
    return contact


@app.get(
    "/contacts/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Список всіх контактів користувача",
    tags=["Contact"],
    response_model=List[ContactModelResponce]
)
async def get_contacts(
    user: Annotated[User, Depends(get_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    query = select(Contact).filter_by(user_id=user.id)
    result = await db.execute(query)
    return result.scalars()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8002)