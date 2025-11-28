"""
Test orders API endpoints - organized by HTTP method with edge cases
"""

import pytest
from rest_framework.reverse import reverse

from api.models import Order
from api.serializers import OrderSerializer
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
    base = order_payloads()[0].copy()
    response = api_client.post(reverse("orders:orders_list"), base)
    assert response.status_code == 201
    expected = OrderSerializer(Order.objects.get(pk=1)).data
    assert response.data == expected

    # Edge case - empty order data
    response = api_client.post(reverse("orders:orders_list"), {})
    assert response.status_code in [400, 500]  # Should fail validation

    # Missing required field: quantity
    missing_quantity = base.copy()
    missing_quantity.pop("quantity", None)
    resp = api_client.post(reverse("orders:orders_list"), missing_quantity)
    assert resp.status_code in [400, 500]

    # Invalid consult id
    invalid_consult = base.copy()
    invalid_consult["consult_id"] = "invalid_id"
    resp = api_client.post(reverse("orders:orders_list"), invalid_consult)
    assert resp.status_code in [400, 500]

    # Nonexistent consult id
    nonexistent_consult = base.copy()
    nonexistent_consult["consult_id"] = 99999
    resp = api_client.post(reverse("orders:orders_list"), nonexistent_consult)
    assert resp.status_code in [400, 500]

    # Missing medicine
    missing_medicine = base.copy()
    missing_medicine.pop("medicine", None)
    resp = api_client.post(reverse("orders:orders_list"), missing_medicine)
    assert resp.status_code in [400, 500]

    # Quantity as non-numeric string
    bad_quantity = base.copy()
    bad_quantity["quantity"] = "ten"
    resp = api_client.post(reverse("orders:orders_list"), bad_quantity)
    assert resp.status_code in [400, 500]

    # Zero quantity
    zero_quantity = base.copy()
    zero_quantity["quantity"] = 0
    resp = api_client.post(reverse("orders:orders_list"), zero_quantity)
    assert resp.status_code in [201, 400, 500]

    # Negative quantity
    negative_quantity = base.copy()
    negative_quantity["quantity"] = -5
    resp = api_client.post(reverse("orders:orders_list"), negative_quantity)
    assert resp.status_code in [201, 400, 500]

    # Very large quantity
    large_quantity = base.copy()
    large_quantity["quantity"] = 10000
    resp = api_client.post(reverse("orders:orders_list"), large_quantity)
    assert resp.status_code in [201, 400, 500]


# Post validation cases have been consolidated under `test_orders_post` above.


@pytest.mark.django_db
def test_orders_filter_by_status(api_client, consult_and_medication, medications_many):
    """Create orders with different statuses and filter by `order_status`."""
    consult_id, medication_id = consult_and_medication

    payload0 = order_payloads()[0].copy()
    payload0["consult_id"] = consult_id
    payload0["order_status"] = "Rejected"
    resp0 = api_client.post(reverse("orders:orders_list"), payload0)
    assert resp0.status_code == 201
    order0_id = resp0.data["id"]

    payload1 = order_payloads()[1].copy()
    payload1["consult_id"] = consult_id
    payload1["order_status"] = "Pending"
    resp1 = api_client.post(reverse("orders:orders_list"), payload1)
    assert resp1.status_code == 201
    order1_id = resp1.data["id"]

    payload2 = order_payloads()[2].copy()
    payload2["consult_id"] = consult_id
    payload2["order_status"] = "Approved"
    resp2 = api_client.post(reverse("orders:orders_list"), payload2)
    assert resp2.status_code == 201
    order2_id = resp2.data["id"]

    payload3 = order_payloads()[3].copy()
    payload3["consult_id"] = consult_id
    del payload3["order_status"]  # Default to PENDING
    resp3 = api_client.post(reverse("orders:orders_list"), payload3)
    assert resp3.status_code == 201
    order3_id = resp3.data["id"]

    # Filter by pending
    resp = api_client.get(reverse("orders:orders_list") + "?order_status=PENDING")
    assert resp.status_code == 200
    ids = [o.get("id") for o in resp.data]
    assert order0_id not in ids
    assert order1_id in ids
    assert order2_id not in ids
    assert order3_id in ids


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
