"""
GET tests for orders
"""

import pytest
from rest_framework.reverse import reverse

from api.models import Order
from api.serializers import OrderSerializer
from api.tests.factories import order_payloads


@pytest.mark.django_db
def test_orders_get_FilterByStatus(
    api_client, consult_and_medication, medications_many
):
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
def test_orders_get_SingleAndList(api_client, order_instance):
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
