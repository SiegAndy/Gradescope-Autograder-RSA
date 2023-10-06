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
    partial_credit,
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

    @partial_credit(30)
    @tags("output")
    @visibility("after_due_date")
    @number("2.1")
    def test_key_generation(self, set_score=None):
        """
        Compute Key using given p and q, and check class attributes have been correctly set.
        """
        self.import_checker()
        self.rsa = RSA.RSA()
        no_param = set()
        wrong_param = set()
        error_param = set()
        for param in self.test_params.compute_key:
            self.rsa.compute_key(param.p, param.q, param.cp_index)
            # each class attributes is 5 credit
            for pkey in ["p", "q", "n", "phi", "e", "d"]:
                if not hasattr(self.rsa, pkey) or getattr(self.rsa, pkey) == None:
                    no_param.add(pkey)
                    continue
                elif getattr(self.rsa, pkey) != getattr(param, pkey):
                    wrong_param.add(pkey)
                    continue

        error_param = no_param.union(wrong_param)
        set_score(5 * (6 - len(error_param)))

        self.assertTrue(
            len(no_param) == 0,
            f"Class does not have the attribute(s) <{', '.join(no_param)}>",
        )
        self.assertTrue(
            len(wrong_param) == 0,
            f"Class compute wrong attribute(s) <{', '.join(wrong_param)}>",
        )

    @partial_credit(20)
    @tags("output")
    @visibility("after_due_date")
    @number("2.2")
    def test_encryption(self, set_score=None):
        """
        Check class method encrypt
        """
        self.import_checker()
        self.rsa = RSA.RSA()
        curr_score = 0

        for param in self.test_params.encryption:
            for pkey in ["p", "q", "n", "phi", "e", "d"]:
                setattr(self.rsa, pkey, getattr(param, pkey))
            cipher_test = self.rsa.encrypt(param.msg)
            self.assertEqual(
                cipher_test, param.cipher, f"Class method encrypt output wrong result"
            )
            curr_score += 4
            set_score(curr_score)

    @partial_credit(20)
    @tags("output")
    @visibility("after_due_date")
    @number("2.3")
    def test_decryption(self, set_score=None):
        """
        Check class method decrypt
        """
        self.import_checker()
        self.rsa = RSA.RSA()
        curr_score = 0

        for param in self.test_params.decryption:
            for pkey in ["p", "q", "n", "phi", "e", "d"]:
                setattr(self.rsa, pkey, getattr(param, pkey))
            cipher_test = self.rsa.encrypt(param.msg)
            self.assertEqual(
                cipher_test, param.cipher, f"Class method encrypt output wrong result"
            )
            decrypted_msg = self.rsa.decrypt(param.cipher)
            self.assertEqual(
                decrypted_msg, param.msg, f"Class method decrypt output wrong result"
            )
            curr_score += 4
            set_score(curr_score)

    @partial_credit(30)
    @tags("output")
    @visibility("after_due_date")
    @number("2.4")
    def test_all(self, set_score=None):
        """
        Check all methods
        """
        self.import_checker()
        self.rsa = RSA.RSA()
        curr_score = 0

        for param in (
            self.test_params.compute_key
            + self.test_params.encryption
            + self.test_params.decryption
        ):
            self.rsa.compute_key(param.p, param.q, param.cp_index)
            cipher_test = self.rsa.encrypt(param.msg)
            self.assertEqual(
                cipher_test, param.cipher, f"Class method encrypt output wrong result"
            )
            decrypted_msg = self.rsa.decrypt(param.cipher)
            self.assertEqual(
                decrypted_msg, param.msg, f"Class method decrypt output wrong result"
            )
            curr_score += 2
            set_score(curr_score)
