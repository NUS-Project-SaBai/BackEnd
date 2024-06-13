from rest_framework.reverse import reverse


def general_test_API(testAPI, dummy, list_endpoint, detail_endpoint):
    post_response = testAPI.client.post(
        reverse(list_endpoint),
        dummy,
    )
    testAPI.assertEqual(post_response.status_code, 200)
    testAPI.assertEqual(
        post_response.data,
        {"id": 1, **dummy},
    )

    # GET
    get_response = testAPI.client.get(reverse(detail_endpoint, args=["1"]))
    testAPI.assertEqual(get_response.status_code, 200)
    testAPI.assertEqual(
        get_response.data,
        {"id": 1, **dummy},
    )

    # PATCH
    put_response = testAPI.client.patch(
        reverse(detail_endpoint, args=["1"]),
        dummy,
    )
    testAPI.assertEqual(put_response.status_code, 200)
    testAPI.assertEqual(
        put_response.data,
        {"id": 1, **dummy},
    )

    # GET
    get_response = testAPI.client.get(reverse(detail_endpoint, args=["1"]))
    testAPI.assertEqual(get_response.status_code, 200)
    testAPI.assertEqual(
        get_response.data,
        {"id": 1, **dummy},
    )

    # DELETE

    delete_response = testAPI.client.delete(reverse(detail_endpoint, args=["1"]))
    testAPI.assertEqual(delete_response.status_code, 200)
    testAPI.assertEqual(delete_response.data, {"message": "Deleted successfully"})

    # GET
    get_response = testAPI.client.get(reverse(list_endpoint))
    testAPI.assertEqual(get_response.status_code, 200)
    testAPI.assertEqual(
        get_response.data,
        [],
    )
