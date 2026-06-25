from datetime import datetime

from pydantic import BaseModel, Field

from apps.otp.consts import DEFAULT_OTP_LENGTH, OTPPurpose


class SendOTPRequestDTO(BaseModel):
    identifier: str
    purpose: OTPPurpose
    ttl: int = Field(default=120, gt=0, lt=600)
    length: int = Field(default=DEFAULT_OTP_LENGTH, gt=0, lt=10)


class SendOTPResponseDTO(BaseModel):
    code: str | None = None
    expires_at: datetime
    is_new: bool


class VerifyOTPRequestDTO(BaseModel):
    identifier: str
    purpose: OTPPurpose
    code: str
