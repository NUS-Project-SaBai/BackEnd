from api.tests.test_setup import TestSetup


class TestMedicationAPI(TestSetup):
    def test_medicine_list(self):
        response = self.client.get("/medications")
        self.assertEqual(response.status_code, 200)
