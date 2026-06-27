from pydantic import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.customers.dto import UpdateCustomerProfileRequestDTO
from apps.customers.permissions import IsCustomer
from apps.customers.services import ProfileService


class CustomerProfileRetrieveUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        response = ProfileService.get_profile(request.user)

        return Response(
            response.model_dump(),
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        try:
            dto = UpdateCustomerProfileRequestDTO.model_validate(request.data)
        except ValidationError as exc:
            return Response(
                {"errors": exc.errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = ProfileService.update_profile(request.user, dto)

        return Response(
            response.model_dump(),
            status=status.HTTP_200_OK,
        )
