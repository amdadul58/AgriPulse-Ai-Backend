from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.core.config import settings
from app.models.user import User


# Bearer Token Authentication
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:

    # Authorization header না থাকলে
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode JWT
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        subject = payload.get("sub")

        if not subject:
            raise cred_exception

    except JWTError:
        raise cred_exception

    # ---------------------------------------------------------
    # Support both JWT formats:
    #
    # 1. sub = email
    #    Example: "sub": "adiba.as@gmail.com"
    #
    # 2. sub = user ID
    #    Example: "sub": "4"
    # ---------------------------------------------------------

    user = None

    # যদি sub numeric হয় → User ID দিয়ে search
    try:
        user_id = int(subject)

        result = await db.execute(
            select(User).where(User.id == user_id)
        )

        user = result.scalar_one_or_none()

    except (ValueError, TypeError):
        # numeric না হলে email হিসেবে search হবে
        result = await db.execute(
            select(User).where(User.email == subject)
        )

        user = result.scalar_one_or_none()

    # User পাওয়া না গেলে
    if user is None:
        raise cred_exception

    return user

