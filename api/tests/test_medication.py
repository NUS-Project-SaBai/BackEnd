from api.tests.test_setup import TestSetup
from api.tests.utils import general_test_API
from api.tests.dummy import medication_dummy


class TestMedicationAPI(TestSetup):
    def test_API(self):
        general_test_API(
            self, medication_dummy, "medications_list", "medications_detail"
        )
