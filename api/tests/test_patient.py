from api.tests.dummy import post_patient_dummy
from api.tests.test_setup import TestSetup
from rest_framework.reverse import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import io


class TestPatient(TestSetup):
    def test_API(self):
        list_endpoint = "patients_list"
        detail_endpoint = "patients_detail"
        dummy = post_patient_dummy
        # face_encodings is generated based on tom_holland_learn.jpeg, through AWS rekognition
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
            "face_encodings": "88e4a97a-10d0-4e63-abe0-bd36808974b4",
            "filter_string": "VPF001VPF1 contact_no patient_name",
            "patient_id" : 'VPF001'
        }

        # The value of picture must be set to the file handle of the Bytes object of the image
        dummy['picture'] = SimpleUploadedFile(
            "tom_holland_learn.jpeg",
            open("api/tests/tom_holland_learn.jpeg", 'rb').read(), 
            content_type='image/jpeg')

        post_response = self.client.post(
            reverse(list_endpoint),
            dummy,
            format='multipart'
        )

        # The image is stored in a Cloudinary field, and is represented as a url to the image on Cloudinary.
        # After every upload, a new url is generated for that image, thus the expected url string in 'picture'
        # must be updated with the generated url.
        dummy_result['picture'] = post_response.data['picture']

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

        # File pointer needs to be reset to the start before it can be used again.
        # picture.seek(0)

        dummy['picture'] = SimpleUploadedFile(
            "tom_holland_learn.jpeg",
            open("api/tests/tom_holland_learn.jpeg", 'rb').read(), 
            content_type='image/jpeg')

        # PATCH
        put_response = self.client.patch(
            reverse(detail_endpoint, args=["1"]),
            dummy,
            format='multipart'
        )

        self.assertEqual(put_response.status_code, 200)
        dummy_result['picture'] = put_response.data['picture']
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