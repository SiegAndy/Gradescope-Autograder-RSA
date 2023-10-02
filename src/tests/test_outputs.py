import json
import types
import unittest
from types import SimpleNamespace
from typing import List

from gradescope_utils.autograder_utils.decorators import (
    number,
    tags,
    visibility,
    weight,
)

import rsa as RSA


class RSAParams:
    p: int
    q: int
    n: int
    phi: int
    cp_index: int
    e: int
    d: int
    msg: int
    cipher: int


class RSATest:
    compute_key: List[RSAParams]
    encryption: List[RSAParams]
    decryption: List[RSAParams]


class TestOutput(unittest.TestCase):
    test_params: RSATest
    rsa: RSA.RSA
    allowed_imports: List[str]

    def setUp(self):
        self.rsa = RSA.RSA()
        self.allowed_imports = ["RSA"]
        with open("grading.json", "r") as grading_file:
            self.test_params = json.load(
                grading_file, object_hook=lambda d: SimpleNamespace(**d)
            )

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

    @weight(30)
    @tags("output")
    @visibility("after_due_date")
    @number("2.1")
    def test_key_generation(self):
        """
        Compute Key using given p and q, and check class attributes have been correctly set.
        """
        self.import_checker()

        for param in self.test_params.compute_key:
            self.rsa.compute_key(param.p, param.q, param.cp_index)
            for pkey in ["p", "q", "n", "phi", "e", "d"]:
                self.assertTrue(
                    hasattr(self.rsa, pkey), f"Checking class has the attribute {pkey}"
                )
                self.assertEqual(
                    self.rsa.__dict__[pkey],
                    param.__dict__[pkey],
                    f"Checking class attribute {pkey} has correct value",
                )

    @weight(20)
    @tags("output")
    @visibility("after_due_date")
    @number("2.2")
    def test_encryption(self):
        """
        Check class method encrypt
        """
        self.import_checker()

        for param in self.test_params.encryption:
            self.rsa.compute_key(param.p, param.q, param.cp_index)
            cipher_test = self.rsa.encrypt(param.msg)
            self.assertEqual(
                cipher_test, param.cipher, f"Checking class method encrypt"
            )

    @weight(20)
    @tags("output")
    @visibility("after_due_date")
    @number("2.3")
    def test_decryption(self):
        """
        Check class method decrypt
        """
        self.import_checker()

        for param in self.test_params.decryption:
            self.rsa.compute_key(param.p, param.q, param.cp_index)
            cipher_test = self.rsa.encrypt(param.msg)
            self.assertEqual(
                cipher_test, param.cipher, f"Checking class method decrypt"
            )
            decrypted_msg = self.rsa.decrypt(param.cipher)
            self.assertEqual(decrypted_msg, param.msg, f"Checking class method decrypt")

    @weight(30)
    @tags("output")
    @visibility("after_due_date")
    @number("2.4")
    def test_all(self):
        """
        Check all methods
        """
        self.import_checker()

        for param in (
            self.test_params.compute_key
            + self.test_params.encryption
            + self.test_params.decryption
        ):
            self.rsa.compute_key(param.p, param.q, param.cp_index)
            cipher_test = self.rsa.encrypt(param.msg)
            self.assertEqual(
                cipher_test, param.cipher, f"Checking class method decrypt"
            )
            decrypted_msg = self.rsa.decrypt(param.cipher)
            self.assertEqual(decrypted_msg, param.msg, f"Checking class method decrypt")
