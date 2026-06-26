from pydantic import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.dto import (
    LoginWithOTPRequestDTO,
    LoginWithPasswordRequestDTO,
    StartAuthRequestDTO,
)
from apps.accounts.exceptions import InvalidCredentialsError, UserNotActiveError
from apps.accounts.services import AuthService
from apps.otp.exceptions import OTPDoesNotExistsError, OTPInvalidError


class AuthStartView(APIView):
    account_type: str | None = None

    def post(self, request):
        account_type = getattr(self, "account_type", None)

        try:
            dto = StartAuthRequestDTO.model_validate(request.data)
        except ValidationError as exc:
            return Response(
                {"errors": exc.errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = AuthService.start(dto, account_type)

        return Response(
            response.model_dump(),
            status=status.HTTP_200_OK,
        )


class AuthPasswordLoginView(APIView):
    account_type: str | None = None

    def post(self, request):
        account_type = getattr(self, "account_type", None)

        try:
            dto = LoginWithPasswordRequestDTO.model_validate(request.data)
        except ValidationError as exc:
            return Response(
                {"errors": exc.errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            response = AuthService.password_login(dto, account_type)
        except UserNotActiveError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_403_FORBIDDEN,
            )
        except InvalidCredentialsError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            response.model_dump(),
            status=status.HTTP_200_OK,
        )


class AuthVerifyOTPView(APIView):
    account_type: str | None = None

    def post(self, request):
        account_type = getattr(self, "account_type", None)

        try:
            dto = LoginWithOTPRequestDTO.model_validate(request.data)
        except ValidationError as exc:
            return Response(
                {"errors": exc.errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            response = AuthService.verify_otp(dto, account_type)
        except UserNotActiveError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_403_FORBIDDEN,
            )
        except (OTPDoesNotExistsError, OTPInvalidError, InvalidCredentialsError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            response.model_dump(),
            status=status.HTTP_200_OK,
        )
