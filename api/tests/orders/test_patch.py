"""
PATCH tests for orders
"""

import pytest
from rest_framework.reverse import reverse
from api.serializers import OrderSerializer


@pytest.mark.django_db
def test_orders_patch_UpdateStatus(api_client, order_instance):
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
