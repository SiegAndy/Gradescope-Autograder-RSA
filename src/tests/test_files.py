import unittest

from gradescope_utils.autograder_utils.decorators import weight, visibility
from gradescope_utils.autograder_utils.files import check_submitted_files


class TestFiles(unittest.TestCase):
    @weight(0)
    @visibility("visible")
    def test_submitted_files(self):
        """Check submitted files"""
        missing_files = check_submitted_files(["rsa.py"])
        for path in missing_files:
            print("Missing {0}".format(path))
        self.assertEqual(len(missing_files), 0, "Missing some required files!")
        print("All required files submitted!")
