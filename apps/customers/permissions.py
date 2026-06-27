from rest_framework.permissions import BasePermission

from apps.accounts.consts import AccountType


class IsCustomer(BasePermission):
    message = "Only customers can access this endpoint."

    def has_permission(self, request, view):
        return request.user and request.user.account_type == AccountType.CUSTOMER
