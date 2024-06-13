from api.tests.test_setup import TestSetup
import api.tests.dummy as dummy
from rest_framework.reverse import reverse


class TestConsultAPI(TestSetup):
    def setUp(self):
        super().setUp()
        self.client.post(
            reverse("patients_list"),
            dummy.post_patient_dummy,
        )
        self.client.post("/visits", dummy.post_visit_dummy)

    def test_API(self):
        post_response = self.client.post(
            reverse("consults_list"),
            dummy.post_consult_dummy,
        )
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(
            post_response.data,
            {
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
                        "filterString": "VPF001VPF1 contact_no patient_name",
                    },
                    "date": "2021-01-01T00:00:00Z",
                    "status": "status",
                },
                "doctor": {"username": "test_user"},
                "date": "2021-01-01T00:00:00Z",
                "past_medical_history": "past_medical_history",
                "consultation": "consultation",
                "plan": "plan",
                "referred_for": "referred_for",
                "referral_notes": "referral_notes",
                "remarks": "remarks",
            },
        )

        # GET
        get_response = self.client.get(reverse("consults_detail", args=["1"]))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.data,
            {
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
                        "filterString": "VPF001VPF1 contact_no patient_name",
                    },
                    "date": "2021-01-01T00:00:00Z",
                    "status": "status",
                },
                "doctor": {"username": "test_user"},
                "date": "2021-01-01T00:00:00Z",
                "past_medical_history": "past_medical_history",
                "consultation": "consultation",
                "plan": "plan",
                "referred_for": "referred_for",
                "referral_notes": "referral_notes",
                "remarks": "remarks",
            },
        )

        # PATCH
        put_response = self.client.patch(
            reverse("consults_detail", args=["1"]),
            dummy.post_consult_dummy,
        )
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(
            put_response.data,
            {
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
                        "filterString": "VPF001VPF1 contact_no patient_name",
                    },
                    "date": "2021-01-01T00:00:00Z",
                    "status": "status",
                },
                "doctor": {"username": "test_user"},
                "date": "2021-01-01T00:00:00Z",
                "past_medical_history": "past_medical_history",
                "consultation": "consultation",
                "plan": "plan",
                "referred_for": "referred_for",
                "referral_notes": "referral_notes",
                "remarks": "remarks",
            },
        )

        # GET
        get_response = self.client.get(reverse("consults_detail", args=["1"]))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.data,
            {
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
                        "filterString": "VPF001VPF1 contact_no patient_name",
                    },
                    "date": "2021-01-01T00:00:00Z",
                    "status": "status",
                },
                "doctor": {"username": "test_user"},
                "date": "2021-01-01T00:00:00Z",
                "past_medical_history": "past_medical_history",
                "consultation": "consultation",
                "plan": "plan",
                "referred_for": "referred_for",
                "referral_notes": "referral_notes",
                "remarks": "remarks",
            },
        )

        # DELETE

        delete_response = self.client.delete(reverse("consults_detail", args=["1"]))
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.data, {"message": "Deleted successfully"})

        # GET
        get_response = self.client.get(reverse("consults_list"))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.data,
            [],
        )
