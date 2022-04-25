"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import index
from .api import (
    crowd_sourced_response,
    autocomplete_response,
    settings_response,
    property_basics_page_response,
    property_details_page_response,
    owner_page_properties_by_owner_name_response,
    owner_page_properties_by_mailing_address_response,
    property_latest_owner_details_response,
    neighborhoods_page_response,
    neighborhoods_page_by_parcel_lists_response,
)

api_urlpatterns = [
    path("api/", settings_response, name="settings"),
    path("api/v1/autocomplete/", autocomplete_response, name="autocomplete_list"),
    path(
        "api/v1/crowd_sourced/",
        crowd_sourced_response,
        name="crowd_sourced_list",
    ),
    path(
        "api/v1/property/basics/",
        property_basics_page_response,
        name="property_page_list",
    ),
    path(
        "api/v1/property/details/",
        property_details_page_response,
        name="property_page_list",
    ),
    path(
        "api/v1/property/latest_owner_details/",
        property_latest_owner_details_response,
        name="property_page_latest_owner_details_list",
    ),
    path(
        "api/v1/owner/by_name/",
        owner_page_properties_by_owner_name_response,
        name="owner_page_by_owner_name_list",
    ),
    path(
        "api/v1/owner/by_mailing_address/",
        owner_page_properties_by_mailing_address_response,
        name="owner_page_by_mailing_address_list",
    ),
    path(
        "api/v1/neighborhoods/",
        neighborhoods_page_response,
        name="neighborhoods_page_list",
    ),
    path(
        "api/v1/neighborhoods_by_parcel_lists/",
        neighborhoods_page_by_parcel_lists_response,
        name="neighborhoods_page_by_parcel_lists_list",
    ),
]

urlpatterns = [
    path("", index, name="index"),
    # path("admin/", admin.site.urls),
] + api_urlpatterns
