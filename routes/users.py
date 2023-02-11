from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from models.user import User, TokenResponse

user_router = APIRouter(
    tags=["User"]
)
hash_password = HashPassword()


@user_router.post("/signup")
async def sign_up_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the email provided already exist"
        )

    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await User.save(user)
    return {
        "message": "User created successfully"
    }


@user_router.post("/signin", response_model=TokenResponse)
async def sign_in_user(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.email == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email address does not exist."
        )

    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials provided"
    )
