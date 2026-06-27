from django.contrib.auth import get_user_model
from django.db import transaction

from apps.customers.dto import AddressListItemDTO, CreateAddressRequestDTO
from apps.customers.exceptions import AddressNotFoundError
from apps.customers.models import CustomerAddress

User = get_user_model()


class AddressService:
    @classmethod
    def list_addresses(cls, user) -> list[AddressListItemDTO]:
        addresses = CustomerAddress.objects.filter(user=user).order_by("-created_at")
        return [AddressListItemDTO.model_validate(address) for address in addresses]

    @classmethod
    @transaction.atomic
    def create_address(
        cls,
        user,
        dto: CreateAddressRequestDTO,
    ) -> AddressListItemDTO:
        address = CustomerAddress.objects.create(
            user=user,
            label=dto.label,
            province=dto.province,
            city=dto.city,
            address=dto.address,
            house_number=dto.house_number,
            building_unit=dto.building_unit,
            postal_code=dto.postal_code,
            latitude=dto.latitude,
            longitude=dto.longitude,
            receiver_full_name=dto.receiver_full_name,
            receiver_phone_number=dto.receiver_phone_number,
        )
        return AddressListItemDTO.model_validate(address)

    @classmethod
    @transaction.atomic
    def delete_address(cls, user, address_id: str) -> None:
        address = CustomerAddress.objects.filter(id=address_id, user=user).first()

        if not address:
            raise AddressNotFoundError(f"Address with id {address_id} not found.")

        address.delete()
