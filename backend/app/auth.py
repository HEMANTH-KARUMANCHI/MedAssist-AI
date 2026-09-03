import os
import bcrypt
from fastapi import APIRouter, HTTPException, Depends

from app.database import get_database_connection
from app.schemas import UserRegister

from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

## read current user
def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

        return {
            "user_id": user_id,
            "email": payload.get("email"),
            "role": payload.get("role")
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def hash_password(password: str) -> str:
    """Safely hash password using native bcrypt with 72-byte truncation."""
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Safely verify password using native bcrypt."""
    try:
        pwd_bytes = plain_password.encode("utf-8")[:72]
        hash_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hash_bytes)
    except Exception:
        return False


#patient authentication
def require_patient(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "patient":
        raise HTTPException(
            status_code=403,
            detail="Patient access required"
        )

    return current_user

# Caretaker authentication
def require_caretaker(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "caretaker":
        raise HTTPException(
            status_code=403,
            detail="Caretaker access required"
        )

    return current_user


SECRET_KEY = os.getenv("SECRET_KEY", "medassist-ai-secret-key-change-later")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/register")
def register_user(user: UserRegister):
    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (user.email,)
        )
        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered. Please sign in instead."
            )

        password_hash = hash_password(user.password)

        cursor.execute(
            """
            INSERT INTO users
            (full_name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id, full_name, email, role
            """,
            (
                user.full_name,
                user.email,
                password_hash,
                user.role
            )
        )
        new_user = cursor.fetchone()
        connection.commit()

        return {
            "message": "User registered successfully",
            "user": {
                "id": new_user[0],
                "full_name": new_user[1],
                "email": new_user[2],
                "role": new_user[3]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Registration database error: {str(e)}"
        )
    finally:
        cursor.close()
        connection.close()


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id, full_name, email, password_hash, role
            FROM users
            WHERE email = %s
            """,
            (form_data.username,)
        )
        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        password_is_valid = verify_password(
            form_data.password,
            user[3]
        )

        if not password_is_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token_data = {
            "sub": str(user[0]),
            "email": user[2],
            "role": user[4],
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }

        access_token = jwt.encode(
            access_token_data,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user[0],
                "full_name": user[1],
                "email": user[2],
                "role": user[4]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Login database error: {str(e)}"
        )
    finally:
        cursor.close()
        connection.close()


@router.get("/me")
def get_my_profile(
    current_user: dict = Depends(get_current_user)
):
    return {
        "message": "Authentication successful",
        "user": current_user
    }


@router.get("/patient-only")
def patient_only_endpoint(
    current_user: dict = Depends(require_patient)
):
    return {
        "message": "You have access to the patient area",
        "user": current_user
    }

@router.get("/caretaker-only")
def caretaker_only_endpoint(
    current_user: dict = Depends(require_caretaker)
):
    return {
        "message": "You have access to the caretaker area",
        "user": current_user
    }