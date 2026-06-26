from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.consts import AccountType, AuthStep
from apps.accounts.dto import (
    LoginWithOTPRequestDTO,
    LoginWithPasswordRequestDTO,
    StartAuthRequestDTO,
    StartAuthResponseDTO,
    TokenResponseDTO,
)
from apps.accounts.exceptions import InvalidCredentialsError, UserNotActiveError
from apps.otp.consts import OTPPurpose
from apps.otp.dto import SendOTPRequestDTO, VerifyOTPRequestDTO
from apps.otp.services import OTPService

User = get_user_model()


class AuthService:
    @classmethod
    def _get_user(cls, phone_number: str, account_type: AccountType):
        return User.objects.filter(
            phone_number=phone_number,
            account_type=account_type,
        ).first()

    @classmethod
    def _create_user(cls, phone_number: str, account_type: AccountType):
        user = User(
            phone_number=phone_number,
            account_type=account_type,
        )
        user.set_unusable_password()
        user.save()
        return user

    @classmethod
    def _build_token_response(cls, user, is_new_user: bool) -> TokenResponseDTO:
        refresh = RefreshToken.for_user(user)

        access = refresh.access_token
        access["account_type"] = user.account_type

        return TokenResponseDTO(
            access_token=str(access),
            refresh_token=str(refresh),
            is_new_user=is_new_user,
        )

    @classmethod
    def _validate_account_type(cls, account_type: AccountType) -> None:
        if account_type not in (AccountType.CUSTOMER, AccountType.SELLER):
            raise InvalidCredentialsError("Invalid account type.")

    @classmethod
    def _get_otp_purpose(cls, account_type: AccountType, is_new_user: bool):
        match (account_type, is_new_user):
            case (AccountType.CUSTOMER, False):
                return OTPPurpose.LOGIN_CUSTOMER
            case (AccountType.CUSTOMER, True):
                return OTPPurpose.SIGNUP_CUSTOMER
            case (AccountType.SELLER, False):
                return OTPPurpose.LOGIN_SELLER
            case (AccountType.SELLER, True):
                return OTPPurpose.SIGNUP_SELLER
            case _:
                raise ValueError(f"Unsupported account type: {account_type}")

    @classmethod
    def start(
        cls,
        dto: StartAuthRequestDTO,
        account_type: AccountType,
    ) -> StartAuthResponseDTO:
        cls._validate_account_type(account_type)

        user = cls._get_user(dto.phone_number, account_type)

        if user and user.has_usable_password():
            return StartAuthResponseDTO(
                phone_number=dto.phone_number,
                next_step=AuthStep.PASSWORD,
            )

        send_otp_response = OTPService.send(
            SendOTPRequestDTO(
                identifier=dto.phone_number,
                purpose=cls._get_otp_purpose(account_type, user is None),
            )
        )

        # TODO: Send otp with sms service
        if send_otp_response.is_new:
            print("OTP Code: ", send_otp_response.code)

        return StartAuthResponseDTO(
            phone_number=dto.phone_number,
            next_step=AuthStep.OTP,
            otp_expires_at=send_otp_response.expires_at,
        )

    @classmethod
    @transaction.atomic
    def verify_otp(
        cls,
        dto: LoginWithOTPRequestDTO,
        account_type: AccountType,
    ) -> TokenResponseDTO:
        cls._validate_account_type(account_type)

        user = cls._get_user(dto.phone_number, account_type)

        if user is not None and not user.is_active:
            raise UserNotActiveError("User account is not active.")

        OTPService.verify(
            VerifyOTPRequestDTO(
                identifier=dto.phone_number,
                purpose=cls._get_otp_purpose(account_type, user is None),
                code=dto.code,
            )
        )

        is_new_user = user is None

        if is_new_user:
            user = cls._create_user(dto.phone_number, account_type)

        return cls._build_token_response(user, is_new_user)

    @classmethod
    def password_login(
        cls,
        dto: LoginWithPasswordRequestDTO,
        account_type: AccountType,
    ) -> TokenResponseDTO:
        cls._validate_account_type(account_type)

        user = cls._get_user(dto.phone_number, account_type)

        if user is not None and not user.is_active:
            raise UserNotActiveError("User account is not active.")

        if (
            user is None
            or not user.has_usable_password()
            or not user.check_password(dto.password)
        ):
            raise InvalidCredentialsError("Phone number or password is invalid.")

        return cls._build_token_response(user, False)
