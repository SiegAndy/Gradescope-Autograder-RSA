import io
import sys
import types
from typing import Any, Callable
import unittest

from gradescope_utils.autograder_utils.decorators import (
    number,
    tags,
    visibility,
    weight,
)

try:
    import rsa as RSA
except SystemExit:
    pass


class SuppressClass(io.StringIO):
    def __init__(
        self,
        *args,
    ):
        io.StringIO.__init__(self, *args)

    def getvalue(self):
        return ""


class TestValid(unittest.TestCase):
    # rsa: RSA.RSA

    def setUp(self):
        self.original_stdout = sys.stdout
        self.suppress_text = io.StringIO()
        self.allowed_imports = ["RSA"]
        self.test_module_not_exit = False
        try:
            self.rsa = RSA.RSA()
        except NameError:
            self.test_module_not_exit = True

    def suppress_print(self, suppress_print: bool) -> None:
        if suppress_print:
            sys.stdout = self.suppress_text
        else:
            sys.stdout = self.original_stdout

    def method_wrapper(
        self, method: Callable, *inputs, suppress_print: bool = True
    ) -> Any:
        if suppress_print:
            self.suppress_print(True)
        result = method(*inputs)
        if suppress_print:
            self.suppress_print(False)
        return result

    def import_checker(self):
        """Check imported packages"""
        if self.test_module_not_exit:
            self.assertTrue(
                False,
                "Class RSA not Found, make sure your file (rsa.py) and class (RSA) has correct name and does not exit program itself!",
            )
        for name, val in list(globals().get("RSA").__dict__.items()):
            if name.startswith("__"):
                continue
            if (
                isinstance(val, types.BuiltinMethodType)
                or isinstance(val, types.BuiltinFunctionType)
                or isinstance(val, types.FunctionType)
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

        self.method_wrapper(self.rsa.compute_key, 67, 83, 3)
        cipher_test = self.method_wrapper(self.rsa.encrypt, 24)
        self.assertEqual(cipher_test, 3658, f"Checking class method encrypt")
        decrypted_msg = self.method_wrapper(self.rsa.decrypt, cipher_test)
        self.assertEqual(decrypted_msg, 24, f"Checking class method decrypt")
