from api.tests.test_setup import TestSetup


class TestPostAllAPI(TestSetup):
    def create_all(self):
        create_patient = self.client.post(
            "/patients",
            {
                "village_prefix": "VPF",
                "name": "patient_name",
                "identification_number": "identification_number",
                "contact_no": "contact_no",
                "gender": "gender",
                "date_of_birth": "2021-01-01",
                "drug_allergy": "drug_allergy",
                "picture": "image/upload/v1715063294/ghynewr4gdhkuttombwc.jpg",
            },
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
