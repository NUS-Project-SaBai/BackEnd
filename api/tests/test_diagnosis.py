from api.tests.dummy import (
    post_visit_dummy,
    post_patient_dummy,
    post_consult_dummy,
    post_diagnosis_dummy,
)
from api.tests.test_setup import TestSetup
from rest_framework.reverse import reverse


class TestDiagnosisAPI(TestSetup):
    def setUp(self):
        super().setUp()
        self.client.post("/patients", post_patient_dummy)
        self.client.post("/visits", post_visit_dummy)
        self.client.post("/consults", post_consult_dummy)

    def test_API(self):
        list_endpoint = "diagnosis_list"
        detail_endpoint = "diagnosis_detail"
        dummy = post_diagnosis_dummy

        dummy_result = {
            "id": 1,
            "consult": {
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
                "doctor": {
                    "user_id": "1",
                    "username": "test_user",
                    "email": f"{self.user.email}",
                    "picture": "",
                    "nickname": ""
                },
                "prescriptions": [],
                "date": "2021-01-01T00:00:00Z",
                "past_medical_history": "past_medical_history",
                "consultation": "consultation",
                "plan": "plan",
                "referred_for": "referred_for",
                "referral_notes": "referral_notes",
                "remarks": "remarks",
            },
            "details": "consult_details",
            "category": "consult_category",
        }

        post_response = self.client.post(reverse(list_endpoint), dummy)

        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(
            post_response.data,
            dummy_result,
        )

        # GET
        get_response = self.client.get("/diagnosis/1")
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

        delete_response = self.client.delete(
            reverse(detail_endpoint, args=["1"]))
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.data, {
                         "message": "Deleted successfully"})

        # GET
        get_response = self.client.get(reverse(list_endpoint))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.data,
            [],
        )
