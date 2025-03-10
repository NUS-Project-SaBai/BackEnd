from api.tests.test_setup import TestSetup
from rest_framework.reverse import reverse
from api.tests.dummy import post_vitals_dummy, post_patient_dummy, post_visit_dummy


class TestVitalsAPI(TestSetup):
    def setUp(self):
        super().setUp()
        self.post_patient_dummy = self.client.post(
            reverse("patients_list"), post_patient_dummy
        )
        self.post_visit_dummy = self.client.post(
            reverse("visits_list"), post_visit_dummy
        )

    def test_API(self):
        list_endpoint = "vitals_list"
        detail_endpoint = "vitals_detail"
        dummy_response = {
            "id": 1,
            "visit": {
                "id": 1,
                "patient": {
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
                },
                "date": "2021-01-01T00:00:00Z",
                "status": "status",
            },
            "height": "100.00",
            "weight": "100.00",
            "systolic": "100",
            "diastolic": "100",
            "temperature": "37.00",
            "diabetes_mellitus": "Yes",
            "heart_rate": "100",
            "urine_test": "True",
            "hemocue_count": "100.00",
            "blood_glucose": "100.00",
            "left_eye_degree": "+4",
            "right_eye_degree": "+4",
            "left_eye_pinhole": "+23",
            "right_eye_pinhole": "+23",
            "others": "others",
        }

        post_response = self.client.post(
            reverse(list_endpoint),
            post_vitals_dummy,
        )
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(
            post_response.data,
            dummy_response,
        )

        # GET
        get_response = self.client.get(reverse(detail_endpoint, args=["1"]))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.data,
            dummy_response,
        )

        # PATCH
        put_response = self.client.patch(
            reverse(detail_endpoint, args=["1"]),
            post_vitals_dummy,
        )
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(
            put_response.data,
            dummy_response,
        )

        # GET
        get_response = self.client.get(reverse(detail_endpoint, args=["1"]))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.data,
            dummy_response,
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
