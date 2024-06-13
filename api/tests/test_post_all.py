from api.tests.test_setup import TestSetup
import api.tests.dummy as dummy


class TestPostAllAPI(TestSetup):
    def create_all(self):
        create_patient = self.client.post(
            "/patients",
            dummy.patient_post_dummy,
        )
        self.assertEqual(create_patient.status_code, 200)

        create_visit = self.client.post(
            "/visits",
            {
                "patient": 1,
                "date": "2021-01-01",
                "status": "status",
            },
        )
        self.assertEqual(create_visit.status_code, 200)

        create_consult = self.client.post(
            "/consults",
            {
                "visit": 1,
                "doctor": 1,
            },
        )
        print(create_consult.data)
