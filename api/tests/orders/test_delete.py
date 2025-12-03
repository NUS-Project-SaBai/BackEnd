"""
DELETE tests for orders
"""

import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_orders_delete_RemovesAndEdgeCases(api_client, order_instance):
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
