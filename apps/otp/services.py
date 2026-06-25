from datetime import timedelta
from random import choices
from string import digits

from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.utils import timezone

from apps.otp.consts import MAX_OTP_FAILURE, OTPPurpose
from apps.otp.dto import (
    SendOTPRequestDTO,
    SendOTPResponseDTO,
    VerifyOTPRequestDTO,
)
from apps.otp.exceptions import OTPDoesNotExistsError, OTPInvalidError
from apps.otp.models import OTP


class OTPService:
    @classmethod
    def _generate_otp_code(cls, length: int) -> str:
        return "".join(choices(digits, k=length))

    @classmethod
    def _get_active_otp(cls, identifier: str, purpose: OTPPurpose) -> OTP | None:
        return (
            OTP.objects.select_for_update()
            .filter(
                identifier=identifier,
                purpose=purpose,
                is_used=False,
                expires_at__gt=timezone.now(),
                failed_attempts__lt=MAX_OTP_FAILURE,
            )
            .first()
        )

    @classmethod
    @transaction.atomic
    def send(
        cls,
        dto: SendOTPRequestDTO,
    ) -> SendOTPResponseDTO:
        otp = cls._get_active_otp(
            dto.identifier,
            dto.purpose,
        )

        if otp:
            return SendOTPResponseDTO(
                expires_at=otp.expires_at,
                is_new=False,
            )

        code = cls._generate_otp_code(dto.length)
        expires_at = timezone.now() + timedelta(seconds=dto.ttl)

        otp = OTP.objects.create(
            identifier=dto.identifier,
            purpose=dto.purpose,
            code=make_password(code),
            expires_at=expires_at,
        )

        return SendOTPResponseDTO(
            code=code,
            expires_at=expires_at,
            is_new=True,
        )

    @classmethod
    @transaction.atomic
    def verify(
        cls,
        dto: VerifyOTPRequestDTO,
    ) -> bool:
        otp = cls._get_active_otp(
            dto.identifier,
            dto.purpose,
        )

        if otp is None:
            raise OTPDoesNotExistsError()

        if not check_password(
            dto.code,
            otp.code,
        ):
            otp.failed_attempts += 1
            otp.save(update_fields=["failed_attempts"])

            raise OTPInvalidError()

        otp.is_used = True
        otp.save(update_fields=["is_used"])

        return True
