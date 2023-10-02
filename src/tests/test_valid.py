import types
import unittest

from gradescope_utils.autograder_utils.decorators import (
    number,
    tags,
    visibility,
    weight,
)

import rsa as RSA


class TestValid(unittest.TestCase):
    rsa: RSA.RSA

    def setUp(self):
        self.allowed_imports = ["RSA"]
        self.rsa = RSA.RSA()

    def import_checker(self):
        """Check imported packages"""
        for name, val in list(globals().get("RSA").__dict__.items()):
            if name.startswith("__"):
                continue
            if isinstance(val, types.BuiltinMethodType) or isinstance(
                val, types.BuiltinFunctionType
            ):
                continue
            if name == "gcd" or "typing." in str(val):
                continue
            return self.assertIn(
                name,
                self.allowed_imports,
                f"Import not allowed: <{name}>",
            )

    @weight(0)
    @visibility("visible")
    @number("1.1")
    def test_import(self):
        """Check imported packages"""
        self.import_checker()

    @weight(0)
    @tags("output")
    @visibility("visible")
    @number("1.2")
    def test_example_case(self):
        """
        Compute Key and Encrypt/Decrypt Sample Message
        """
        self.import_checker()

        self.rsa.compute_key(67, 83, 3)
        cipher_test = self.rsa.encrypt(24)
        self.assertEqual(cipher_test, 3658, f"Checking class method encrypt")
        decrypted_msg = self.rsa.decrypt(cipher_test)
        self.assertEqual(decrypted_msg, 24, f"Checking class method decrypt")
        # for pkey in ["p", "q", "n", "phi", "e", "d"]:
        #     self.assertTrue(
        #         hasattr(self.rsa, pkey), f"Checking class has the attribute {pkey}"
        #     )
        #     self.assertEqual(
        #         self.rsa.__dict__[pkey],
        #         param.__dict__[pkey],
        #         f"Checking class attribute {pkey} has correct value",
        #     )
