from api.tests.test_setup import TestSetup
from api.tests.utils import general_test_API


class TestMedicationAPI(TestSetup):

    def test_API(self):
        dummy = {
            "medicine_name": "medicine_name",
            "quantity": 1,
            "notes": "notes",
            "remarks": "remarks",
        }
        general_test_API(self, dummy, "medications_list", "medications_detail")
