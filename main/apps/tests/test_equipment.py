from main.apps.common.models import Currency
from main.apps.dashboard.models.dashboard import Object
from main.apps.equipment.models.hydro_station import FinancialResource, HydroStation
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model




@pytest.fixture
def create_object_and_currency():
    obj = Object.objects.create(title="Test Object")
    currency = Currency.objects.create(title="USD")
    return obj, currency


@pytest.fixture
def create_user():
    return get_user_model().objects.create_user(
        username="testuser",
        password="password123",
        email="testuser@example.com"
    )


@pytest.fixture
def create_hydro_station(create_user, create_object_and_currency):
    """Fixture to create a HydroStation instance."""
    obj, currency = create_object_and_currency
    return HydroStation.objects.create(
        object=obj,
        supplier_name="Test Supplier",
        contract_number="12345",
        contract_amount="10000.00",
        currency=currency,
        delivery_date="2025-02-17"
    )


@pytest.mark.django_db
def test_create_hydro_station(create_user, create_object_and_currency):
    obj, currency = create_object_and_currency
    client = APIClient()
    client.force_authenticate(user=create_user)

    url = reverse('equipment:hydro_station:hydro_station_create')
    data = {
        "object": obj.id,  
        "supplier_name": "Test Supplier",
        "contract_number": "12345",
        "contract_amount": "10000.00",
        "currency": currency.id,  
        "delivery_date": "2025-02-17"
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.data

    assert response_data["supplier_name"] == "Test Supplier"
    assert response_data["contract_amount"] == "10000.00"


@pytest.mark.django_db
def test_create_financial_resource(create_user, create_hydro_station):
    """Test creating a financial resource linked to a hydro station."""
    client = APIClient()
    client.force_authenticate(user=create_user)

    url = reverse("equipment:hydro_station:financial_resource_create")
    data = {
        "hydro_station": create_hydro_station.id,
        "title": "Test Financial Resource",
        "amount": "10000.00",
        "prepayment_from_own_fund": "1000.00",
        "prepayment_from_foreign_credit_account": "2000.00",
        "additional_prepayment": "500.00",
        "payment_on_completion": "7000.00"
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "data" in response.data  
    response_data = response.data["data"]  

    assert response_data["title"] == "Test Financial Resource"
    assert response_data["amount"] == "10000.00"
    assert response_data["payment_on_completion"] == "7000.00"


@pytest.mark.django_db
def test_create_hydro_station_invalid_data(create_user):
    """Test creating a hydro station with invalid data."""
    client = APIClient()
    client.force_authenticate(user=create_user)

    url = reverse("equipment:hydro_station:hydro_station_create")
    data = {
        "object": None,
        "supplier_name": "",
        "contract_number": "12345",
        "contract_amount": "0.00",
        "currency": None,
        "transit_equipment_amount": "5000.00",
        "delivery_date": "2025-02-17"
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "errors" in response.data
    assert "object" in response.data["errors"]
    assert "supplier_name" in response.data["errors"]


@pytest.mark.django_db
def test_create_financial_resource_invalid_data(create_user, create_hydro_station):
    """Test creating a financial resource with invalid data."""
    client = APIClient()
    client.force_authenticate(user=create_user)

    url = reverse("equipment:hydro_station:financial_resource_create")
    data = {
        "hydro_station": create_hydro_station.id,
        "title": "",
        "amount": "0.00",
        "prepayment_from_own_fund": "1000.00",
        "prepayment_from_foreign_credit_account": "2000.00",
        "additional_prepayment": "500.00",
        "payment_on_completion": "7000.00"
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "errors" in response.data
    assert "title" in response.data["errors"]

