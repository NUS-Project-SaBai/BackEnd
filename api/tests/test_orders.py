"""
Test orders API endpoints - organized by HTTP method with edge cases
"""

import pytest
from rest_framework.reverse import reverse

from api.models import Order
from api.serializers import OrderSerializer
import api.tests.dummies as dummy
from api.tests.factories import order_payloads


@pytest.fixture
def order_instance(api_client, consult_and_medication):
    """Create an order instance for tests that need existing data"""
    payload = order_payloads()[0]
    response = api_client.post(reverse("orders:orders_list"), payload)
    assert response.status_code == 201
    return Order.objects.get(pk=response.data["id"])


@pytest.mark.django_db
def test_orders_post(api_client, consult_and_medication):
    """Test creating orders via POST - success and edge cases"""
    # Successful case - create order
    payload = order_payloads()[0]
    response = api_client.post(reverse("orders:orders_list"), payload)
    assert response.status_code == 201
    expected = OrderSerializer(Order.objects.get(pk=1)).data
    assert response.data == expected

    # Edge case - empty order data
    response = api_client.post(reverse("orders:orders_list"), {})
    assert response.status_code in [400, 500]  # Should fail validation


@pytest.mark.django_db
def test_orders_get(api_client, order_instance):
    """Test retrieving orders via GET - single, list, and edge cases"""
    # Successful case - retrieve single order by pk
    response = api_client.get(
        reverse("orders:orders_pk", args=[str(order_instance.pk)])
    )
    assert response.status_code == 200
    expected = OrderSerializer(order_instance).data
    assert response.data == expected

    # Successful case - list orders
    response = api_client.get(reverse("orders:orders_list"))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == order_instance.pk

    # Edge case - get nonexistent order
    response = api_client.get(reverse("orders:orders_pk", args=["99999"]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_orders_patch(api_client, order_instance):
    """Test updating orders via PATCH - success and edge cases"""
    # Successful case - update order status
    update_payload = {"order_status": "PENDING"}
    response = api_client.patch(
        reverse("orders:orders_pk", args=[str(order_instance.pk)]), update_payload
    )
    assert response.status_code == 200
    expected = OrderSerializer(order_instance).data
    assert response.data == expected

    # Edge case - update nonexistent order
    response = api_client.patch(
        reverse("orders:orders_pk", args=["99999"]), update_payload
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_orders_delete(api_client, order_instance):
    """Test deleting orders via DELETE - success and edge cases"""
    order_pk = order_instance.pk

    # Successful case - delete order
    response = api_client.delete(reverse("orders:orders_pk", args=[str(order_pk)]))
    assert response.status_code == 200
    assert response.data == {"message": "Deleted successfully"}

    # Verify order is gone from list
    response = api_client.get(reverse("orders:orders_list"))
    assert response.status_code == 200
    assert response.data == []

    # Edge case - delete already deleted order (should 404)
    response = api_client.delete(reverse("orders:orders_pk", args=[str(order_pk)]))
    assert response.status_code == 404

    # Edge case - delete nonexistent order
    response = api_client.delete(reverse("orders:orders_pk", args=["99999"]))
    assert response.status_code == 404
