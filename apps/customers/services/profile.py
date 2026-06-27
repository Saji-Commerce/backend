from django.contrib.auth import get_user_model
from django.db import transaction

from apps.customers.dto import (
    CustomerProfileResponseDTO,
    UpdateCustomerProfileRequestDTO,
)
from apps.customers.models import CustomerProfile

User = get_user_model()


class ProfileService:
    @classmethod
    def get_profile(cls, user) -> CustomerProfileResponseDTO:
        profile = CustomerProfile.objects.filter(user=user).first()

        return CustomerProfileResponseDTO(
            first_name=profile.first_name if profile else None,
            last_name=profile.last_name if profile else None,
            national_code=profile.national_code if profile else None,
            email=profile.email if profile else None,
            birth_date=profile.birth_date if profile else None,
            phone_number=user.phone_number,
            has_usable_password=user.has_usable_password(),
        )

    @classmethod
    @transaction.atomic
    def update_profile(
        cls,
        user,
        dto: UpdateCustomerProfileRequestDTO,
    ) -> CustomerProfileResponseDTO:
        profile, _ = CustomerProfile.objects.get_or_create(user=user)

        profile.first_name = dto.first_name
        profile.last_name = dto.last_name
        profile.national_code = dto.national_code
        profile.birth_date = dto.birth_date
        profile.save(
            update_fields=["first_name", "last_name", "national_code", "birth_date"]
        )

        return CustomerProfileResponseDTO(
            first_name=profile.first_name,
            last_name=profile.last_name,
            national_code=profile.national_code,
            email=profile.email,
            birth_date=profile.birth_date,
            phone_number=user.phone_number,
            has_usable_password=user.has_usable_password(),
        )
