from api.tests.test_setup import TestSetup
from rest_framework.reverse import reverse
from api.tests.dummy import post_patient_dummy, post_visit_dummy, post_consult_dummy, post_order_dummy, post_medication_dummy


class TestOrdersAPI(TestSetup):
    def setUp(self):
        super().setUp()
        self.post_patient_dummy = self.client.post(
            reverse("patients_list"),
            post_patient_dummy
        )
        self.post_visit_dummy = self.client.post(
            reverse("visits_list"),
            post_visit_dummy
        )
        self.post_consult_dummy = self.client.post(
            reverse("consults_list"),
            post_consult_dummy
        )
        self.post_medication_dummy = self.client.post(
            reverse("medications_list"),
            post_medication_dummy
        )

    def test_API(self):
        list_endpoint = "orders_list"
        detail_endpoint = "orders_detail"
        dummy_response = {
            'id': 1,
            'medicine': {
                'id': 1,
                'medicine_name': 'medicine_name',
                'quantity': 1,
                'notes': 'notes',
                'remarks': 'remarks'
            },
            'consult': {
                'id': 1,
                'visit': {
                    'id': 1,
                    'patient': {
                        'model': 'clinicmodels.patient',
                        'pk': 1,
                        'village_prefix': 'VPF',
                        'name': 'patient_name',
                        'identification_number': 'identification_number',
                        'contact_no': 'contact_no',
                        'gender': 'gender',
                        'date_of_birth': '2021-01-01T00:00:00Z',
                        'drug_allergy': 'drug_allergy',
                        'face_encodings': None,
                        'picture': 'image/upload/v1715063294/ghynewr4gdhkuttombwc.jpg',
                        'filterString': 'VPF001VPF1 contact_no patient_name'
                    },
                    'date': '2021-01-01T00:00:00Z',
                    'status': 'status'
                },
                'doctor': {
                    'username': 'test_user'
                },
                'date': '2021-01-01T00:00:00Z',
                'past_medical_history': 'past_medical_history',
                'consultation': 'consultation',
                'plan': 'plan',
                'referred_for': 'referred_for',
                'referral_notes': 'referral_notes',
                'remarks': 'remarks'
            },
            'quantity': 100,
            'notes': 'order_notes',
            'remarks': None,
            'order_status': 'status'
        }

        post_response = self.client.post(
            reverse(list_endpoint),
            post_order_dummy,
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
            post_order_dummy,
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