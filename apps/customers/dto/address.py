from pydantic import BaseModel, Field


class CreateAddressRequestDTO(BaseModel):
    label: str = Field(min_length=1, max_length=100)
    province: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    address: str = Field(min_length=1)
    house_number: str = Field(min_length=1, max_length=50)
    building_unit: str = Field(default="", max_length=50)
    postal_code: str = Field(min_length=1, max_length=20)
    latitude: float | None = None
    longitude: float | None = None
    receiver_full_name: str = Field(min_length=1, max_length=255)
    receiver_phone_number: str = Field(min_length=1, max_length=20)


class AddressListItemDTO(BaseModel):
    id: str
    label: str
    address: str
    postal_code: str
    receiver_full_name: str
    receiver_phone_number: str

    class Config:
        from_attributes = True
