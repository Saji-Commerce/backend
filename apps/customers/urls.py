from django.urls import path

from apps.customers.views import (
    CustomerAddressDeleteView,
    CustomerAddressListCreateView,
    CustomerProfileRetrieveUpdateView,
)

urlpatterns = [
    path(
        "customer/profile/",
        CustomerProfileRetrieveUpdateView.as_view(),
        name="customer-profile-retrieve-update",
    ),
    path(
        "customer/addresses/",
        CustomerAddressListCreateView.as_view(),
        name="customer-address-list-create",
    ),
    path(
        "customer/addresses/<str:address_id>/",
        CustomerAddressDeleteView.as_view(),
        name="customer-address-delete",
    ),
]
