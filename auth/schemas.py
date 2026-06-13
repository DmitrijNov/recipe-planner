from typing import Annotated

from pydantic import BaseModel, Field, model_validator


class LoginUserSchema(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    username: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RegisterReqSchema(BaseModel):
    username: str
    email: str
    password: Annotated[str, Field(min_length=5)]
    repeat_password: Annotated[str, Field(min_length=5)]

    @model_validator(mode="after")
    def password_match(self):
        if self.password != self.repeat_password:
            raise ValueError("passwords mismatch")
        return self
