from api.tests.test_setup import TestSetup
from api.tests.dummy import post_medication_dummy
from rest_framework.reverse import reverse


class TestMedicationAPI(TestSetup):
    def test_API(self):
        post_response = self.client.post(
            reverse("medications_list"),
            post_medication_dummy,
        )
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(
            post_response.data,
            {"id": 1, **post_medication_dummy},
        )

        # GET
        get_response = self.client.get(reverse("medications_detail", args=["1"]))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.data,
            {"id": 1, **post_medication_dummy},
        )

        # PATCH
        put_response = self.client.patch(
            reverse("medications_detail", args=["1"]),
            post_medication_dummy,
        )
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(
            put_response.data,
            {"id": 1, **post_medication_dummy},
        )

        # GET
        get_response = self.client.get(reverse("medications_detail", args=["1"]))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.data,
            {"id": 1, **post_medication_dummy},
        )

        # DELETE

        delete_response = self.client.delete(reverse("medications_detail", args=["1"]))
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.data, {"message": "Deleted successfully"})

        # GET
        get_response = self.client.get(reverse("medications_list"))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.data,
            [],
        )
