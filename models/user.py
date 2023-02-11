from beanie import Document
from pydantic import EmailStr, BaseModel


class User(Document):
    email: EmailStr
    password: str

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "email": "testuser",
                "password": "pass123@1",
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type:str