from datetime import date

from pydantic import BaseModel, Field


class UpdateCustomerProfileRequestDTO(BaseModel):
    first_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    national_code: str = Field(min_length=1, max_length=20)
    birth_date: date | None = None


class CustomerProfileResponseDTO(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    national_code: str | None = None
    email: str | None = None
    birth_date: date | None = None
    phone_number: str
    has_usable_password: bool

    class Config:
        from_attributes = True
