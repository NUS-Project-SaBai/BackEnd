from api.tests.test_setup import TestSetup
from django.urls import reverse
from api.models import Patient
from django.utils import timezone


class TestPatient(TestSetup):
    def test_patient_list(self):
        response = self.client.get(reverse("patients_list"))
        self.assertEqual(response.status_code, 200)

    def test_patient_detail(self):
        Patient.objects.create(
            village_prefix="test",
            name="Adam",
            identification_number="A12345",
            gender="male",
            drug_allergy="None",
            face_encodings=None,
            picture=None,
        )
        response = self.client.get(reverse("patients_detail", args=["1"]))
        self.assertEqual(response.status_code, 200)

    def test_patient_delete(self):
        Patient.objects.create(
            village_prefix="test",
            name="Adam",
            identification_number="A12345",
            gender="male",
            drug_allergy="None",
            face_encodings=None,
            picture=None,
        )
        response = self.client.delete(reverse("patients_detail", args=["1"]))
        self.assertEqual(response.status_code, 200)
