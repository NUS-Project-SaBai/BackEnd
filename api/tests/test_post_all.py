from django.urls import reverse
from api.tests.test_setup import TestSetup
import api.tests.dummy as dummy


class TestPostAllAPI(TestSetup):
    def test_post_all(self):
        create_patient = self.client.post(
            reverse("patients_list"),
            dummy.post_patient_dummy,
        )
        self.assertEqual(create_patient.status_code, 200)

        create_visit = self.client.post("/visits", dummy.post_visit_dummy)
        self.assertEqual(create_visit.status_code, 200)

        create_vitals = self.client.post(
            reverse("vitals_list"),
            dummy.post_vitals_dummy,
        )
        self.assertEqual(create_vitals.status_code, 200)

        create_consult = self.client.post(
            reverse("consult_list"),
            dummy.post_consult_dummy,
        )
        self.assertEqual(create_consult.status_code, 200)

        create_diagnosis = self.client.post(
            reverse("diagnosis_list"),
            dummy.post_diagnosis_dummy,
        )
        self.assertEqual(create_diagnosis.status_code, 200)

        create_medication = self.client.post(
            reverse("medications_list"),
            dummy.post_medication_dummy,
        )
        self.assertEqual(create_medication.status_code, 200)

        create_order = self.client.post(
            reverse("orders_list"),
            dummy.post_order_dummy,
        )
        self.assertEqual(create_order.status_code, 200)
