import json
import unittest
from types import SimpleNamespace
from typing import List

from gradescope_utils.autograder_utils.decorators import (
    number,
    tags,
    visibility,
    weight,
)

from rsa import RSA


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
    rsa: RSA

    def setUp(self):
        self.rsa = RSA()
        with open("grading.json", "r") as grading_file:
            self.test_params = json.load(
                grading_file, object_hook=lambda d: SimpleNamespace(**d)
            )

    @weight(3)
    @tags("output")
    @visibility("after_due_date")
    @number("1.1")
    def test_key_generation(self):
        """
        Compute Key using given p and q,
        Check class attributes have been correctly set.
        """
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

    @weight(2)
    @tags("output")
    @visibility("after_due_date")
    @number("1.2")
    def test_encryption(self):
        """
        Encrypt message
        """
        for param in self.test_params.encryption:
            self.rsa.compute_key(param.p, param.q, param.cp_index)
            cipher_test = self.rsa.encrypt(param.msg)
            self.assertEqual(
                cipher_test, param.cipher, f"Checking class method encrypt"
            )

    @weight(2)
    @tags("output")
    @visibility("after_due_date")
    @number("1.3")
    def test_encryption(self):
        """
        Decrypt message
        """
        for param in self.test_params.encryption:
            self.rsa.compute_key(param.p, param.q, param.cp_index)
            cipher_test = self.rsa.encrypt(param.msg)
            self.assertEqual(cipher_test, param.cipher, f"Checking class method decrypt")
            decrypted_msg = self.rsa.decrypt(param.cipher)
            self.assertEqual(decrypted_msg, param.msg, f"Checking class method decrypt")
