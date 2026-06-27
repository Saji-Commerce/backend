from pydantic import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.customers.dto import CreateAddressRequestDTO
from apps.customers.exceptions import AddressNotFoundError
from apps.customers.permissions import IsCustomer
from apps.customers.services import AddressService


class CustomerAddressListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        addresses = AddressService.list_addresses(request.user)

        return Response(
            [address.model_dump() for address in addresses],
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        try:
            dto = CreateAddressRequestDTO.model_validate(request.data)
        except ValidationError as exc:
            return Response(
                {"errors": exc.errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        address = AddressService.create_address(request.user, dto)

        return Response(
            address.model_dump(),
            status=status.HTTP_201_CREATED,
        )


class CustomerAddressDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def delete(self, request, address_id: str):
        try:
            AddressService.delete_address(request.user, address_id)
        except AddressNotFoundError:
            return Response(
                {"detail": "Address not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
