from api.tests.dummy import post_patient_dummy
from api.tests.test_setup import TestSetup
from rest_framework.reverse import reverse


class TestPatient(TestSetup):
    def test_API(self):
        list_endpoint = "patients_list"
        detail_endpoint = "patients_detail"
        dummy = post_patient_dummy
        dummy_result = {
            "model": "clinicmodels.patient",
            "pk": 1,
            "village_prefix": "VPF",
            "name": "patient_name",
            "identification_number": "identification_number",
            "contact_no": "contact_no",
            "gender": "gender",
            "date_of_birth": "2021-01-01T00:00:00Z",
            "drug_allergy": "drug_allergy",
            "face_encodings": None,
            "picture": "image/upload/v1715063294/ghynewr4gdhkuttombwc.jpg",
            "filter_string": "VPF001VPF1 contact_no patient_name",
            "patient_id": "VPF001",
        }

        post_response = self.client.post(
            reverse(list_endpoint),
            dummy,
        )
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(
            post_response.data,
            dummy_result,
        )

        # GET
        get_response = self.client.get(reverse(detail_endpoint, args=["1"]))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.data,
            dummy_result,
        )

        # PATCH
        put_response = self.client.patch(
            reverse(detail_endpoint, args=["1"]),
            dummy,
        )
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(
            put_response.data,
            dummy_result,
        )

        # GET
        get_response = self.client.get(reverse(detail_endpoint, args=["1"]))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.data,
            dummy_result,
        )

        # DELETE

        delete_response = self.client.delete(reverse(detail_endpoint, args=["1"]))
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.data, {"message": "Deleted successfully"})

        # GET
        get_response = self.client.get(reverse(list_endpoint))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.data,
            [],
        )
