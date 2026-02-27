from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import AsyncSessionLocal
from backend.models.user import Users

app = FastAPI(title="Backend API")

password_hasher = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


# --- Schemas ---


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        description="Minimum length is 8 characters",
    )


class SignupResponse(BaseModel):
    message: str
    user_id: str
    email: str


# --- Routes ---


@app.post("/signup", response_model=SignupResponse)
async def signup(body: SignupRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Users).where(Users.email == body.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = get_password_hash(body.password)
    user = Users(
        email=body.email,
        password_hash=hashed,
        is_verified=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return SignupResponse(
        message="User created successfully",
        user_id=str(user.id),
        email=user.email,
    )
