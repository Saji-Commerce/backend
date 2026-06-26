from datetime import datetime

from pydantic import BaseModel, Field

from apps.accounts.consts import AuthStep


class StartAuthRequestDTO(BaseModel):
    phone_number: str = Field(min_length=4, max_length=20)


class StartAuthResponseDTO(BaseModel):
    phone_number: str
    next_step: AuthStep
    otp_expires_at: datetime | None = None


class LoginWithPasswordRequestDTO(BaseModel):
    phone_number: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=1)


class LoginWithOTPRequestDTO(BaseModel):
    phone_number: str = Field(min_length=4, max_length=20)
    code: str = Field(min_length=1)


class TokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    is_new_user: bool = False
