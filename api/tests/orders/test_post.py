"""
POST tests for orders
"""

import pytest
from rest_framework.reverse import reverse

from api.tests.factories import order_payloads
from api.models import Order
from api.serializers import OrderSerializer


@pytest.mark.django_db
def test_orders_post_SuccessAndValidation(api_client, consult_and_medication):
    """Test creating orders via POST - success and edge cases"""
    # Successful case - create order
    base = order_payloads()[0].copy()
    response = api_client.post(reverse("orders:orders_list"), base)
    assert response.status_code == 201
    expected = OrderSerializer(Order.objects.get(pk=1)).data
    assert response.data == expected

    # Edge case - empty order data
    response = api_client.post(reverse("orders:orders_list"), {})
    assert response.status_code in [400, 500]

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
