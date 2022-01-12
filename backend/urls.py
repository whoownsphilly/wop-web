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
from .api_phillydb import (
    appeals_response,
    appeals_schema_response,
    case_investigations_response,
    case_investigations_schema_response,
    complaints_response,
    complaints_schema_response,
    condominiums_response,
    condominiums_schema_response,
    licenses_response,
    licenses_schema_response,
    permits_response,
    permits_schema_response,
    properties_response,
    properties_schema_response,
    real_estate_tax_delinquencies_response,
    real_estate_tax_delinquencies_schema_response,
    real_estate_transfers_response,
    real_estate_transfers_schema_response,
    violations_response,
    violations_schema_response,
)
from .api import (
    bios_response,
    owners_timeline_response,
    autocomplete_response,
    settings_response,
    property_basics_page_response,
    property_details_page_response,
    owner_page_properties_by_owner_name_response,
    owner_page_properties_by_mailing_address_response,
    owner_current_properties_map_response,
    property_latest_owner_details_response,
)

api_urlpatterns = [
    path("api/", settings_response, name="settings"),
    path("api/v1/autocomplete/", autocomplete_response, name="autocomplete_list"),
    path(
        "api/v1/bios/",
        bios_response,
        name="bios_list",
    ),
    path(
        "api/v1/owners_timeline/",
        owners_timeline_response,
        name="owners_timeline_list",
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
        "api/v1/owner_current_properties_map/",
        owner_current_properties_map_response,
        name="owner_current_properties_map_list",
    ),
]

table_schema_api_urlpatterns = [
    path(
        "api/v1/table_schema/properties/",
        properties_schema_response,
        name="properties_schema_list",
    ),
    path(
        "api/v1/table_schema/permits/",
        permits_schema_response,
        name="permits_schema_list",
    ),
    path(
        "api/v1/table_schema/licenses/",
        licenses_schema_response,
        name="licenses_schema_list",
    ),
    path(
        "api/v1/table_schema/violations/",
        violations_schema_response,
        name="violations_schema_list",
    ),
    path(
        "api/v1/table_schema/condominiums/",
        condominiums_schema_response,
        name="condominiums_schema_list",
    ),
    path(
        "api/v1/table_schema/complaints/",
        complaints_schema_response,
        name="complaints_schema_list",
    ),
    path(
        "api/v1/table_schema/appeals/",
        appeals_schema_response,
        name="appeals_schema_list",
    ),
    path(
        "api/v1/table_schema/real_estate_tax_delinquencies/",
        real_estate_tax_delinquencies_schema_response,
        name="real_estate_tax_delinquencies_schema_list",
    ),
    path(
        "api/v1/table_schema/real_estate_transfers/",
        real_estate_transfers_schema_response,
        name="real_estate_transfers_schema_list",
    ),
    path(
        "api/v1/table_schema/case_investigations/",
        case_investigations_schema_response,
        name="case_investigations_schema_list",
    ),
]

table_api_urlpatterns = [
    path("api/v1/table/properties/", properties_response, name="properties_list"),
    path("api/v1/table/permits/", permits_response, name="permits_list"),
    path("api/v1/table/licenses/", licenses_response, name="licenses_list"),
    path("api/v1/table/violations/", violations_response, name="violations_list"),
    path("api/v1/table/condominiums/", condominiums_response, name="condominiums_list"),
    path("api/v1/table/complaints/", complaints_response, name="complaints_list"),
    path("api/v1/table/appeals/", appeals_response, name="appeals_list"),
    path(
        "api/v1/table/real_estate_tax_delinquencies/",
        real_estate_tax_delinquencies_response,
        name="real_estate_tax_delinquencies_list",
    ),
    path(
        "api/v1/table/real_estate_transfers/",
        real_estate_transfers_response,
        name="real_estate_transfers_list",
    ),
    path(
        "api/v1/table/case_investigations/",
        case_investigations_response,
        name="case_investigations_list",
    ),
]

urlpatterns = (
    [
        path("", index, name="index"),
        # path("admin/", admin.site.urls),
    ]
    + api_urlpatterns
    + table_api_urlpatterns
    + table_schema_api_urlpatterns
)
