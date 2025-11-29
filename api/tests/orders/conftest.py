import pytest
from rest_framework.reverse import reverse

from api.models import Order
from api.tests.factories import order_payloads


@pytest.fixture
def order_instance(api_client, consult_and_medication):
    """Create an order instance for tests that need existing data"""
    payload = order_payloads()[0]
    response = api_client.post(reverse("orders:orders_list"), payload)
    assert response.status_code == 201
    return Order.objects.get(pk=response.data["id"])
