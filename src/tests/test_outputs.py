import io
import json
import sys
import types
import unittest
from types import SimpleNamespace
from typing import Any, Callable, List

from gradescope_utils.autograder_utils.decorators import (
    number,
    tags,
    visibility,
    weight,
    partial_credit,
)

try:
    import rsa as RSA
except SystemExit:
    pass


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


class SuppressClass(io.StringIO):
    def __init__(
        self,
        *args,
    ):
        io.StringIO.__init__(self, *args)

    def getvalue(self):
        return ""


class TestOutput(unittest.TestCase):
    test_params: RSATest
    # rsa: RSA.RSA
    allowed_imports: List[str]
    test_module_not_exit: bool

    def setUp(self) -> None:
        self.original_stdout = sys.stdout
        self.suppress_text = io.StringIO()
        self.allowed_imports = ["RSA"]
        with open("grading.json", "r") as grading_file:
            self.test_params = json.load(
                grading_file, object_hook=lambda d: SimpleNamespace(**d)
            )
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

    def cls_attr_cleanup(self, cls, attr_names: List[str]) -> None:
        for attr_name in attr_names:
            if getattr(cls, attr_name, None) is not None:
                setattr(cls, attr_name, None)

    def method_wrapper(
        self, method: Callable, *inputs, suppress_print: bool = True
    ) -> Any:
        if suppress_print:
            self.suppress_print(True)
        result = method(*inputs)
        if suppress_print:
            self.suppress_print(False)
        return result

    def import_checker(self) -> None:
        """Check imported packages"""
        if self.test_module_not_exit:
            self.assertTrue(
                False,
                "Class RSA not Found, make sure your file has correct name and does not exit program itself!",
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
        try:
            self.rsa = RSA.RSA()
        except NameError:
            self.test_module_not_exit = True
        no_param = set()
        wrong_param = set()
        error_param = set()
        wrong_param_record = dict()
        for param in self.test_params.compute_key:
            self.cls_attr_cleanup(self.rsa, ["p", "q", "n", "phi", "e", "d"])
            self.method_wrapper(self.rsa.compute_key, param.p, param.q, param.cp_index)
            # each class attributes is 5 credit
            for pkey in ["n", "phi", "e", "d"]:
                if (not hasattr(self.rsa, pkey) or getattr(self.rsa, pkey) == None) and (not hasattr(RSA.RSA, pkey) or getattr(RSA.RSA, pkey) == None):
                    no_param.add(pkey)
                    continue
                elif getattr(self.rsa, pkey) != getattr(param, pkey) and getattr(RSA.RSA, pkey) != getattr(param, pkey):
                    if getattr(self.rsa, pkey) is None:
                        no_param.add(pkey)
                        continue
                    wrong_param.add(pkey)
                    wrong_param_record[pkey] = (getattr(self.rsa, pkey), ",".join([f"{tag}:{getattr(param, tag)}" for tag in ["p", "q", "n", "phi", "cp_index", "e", "d"]]))
                    continue

        error_param = no_param.union(wrong_param)
        set_score(5 * (6 - len(error_param)))

            
        self.assertTrue(
            len(no_param) == 0,
            f"\nClass does not have the attribute(s) <{', '.join(no_param)}>",
        )

        if len(wrong_param) == 0: return

        wrong_param_text = "\n".join(
            [
                f"Class compute wrong attribute(s) <{curr}={wrong_param_record[curr][0]}> for params: {wrong_param_record[curr][1]}."
                for curr in wrong_param
            ]
        )
        self.assertTrue(
            len(wrong_param) == 0,
            "\n" + wrong_param_text,
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
                # normal way of setting class instance variable
                setattr(self.rsa, pkey, getattr(param, pkey))
                # directly setting class variable
                setattr(RSA.RSA, pkey, getattr(param, pkey))
            param_string = ",".join([f"{tag}:{getattr(param, tag)}" for tag in ["p", "q", "n", "phi", "cp_index", "e", "d"]])
            cipher_test = self.method_wrapper(self.rsa.encrypt, param.msg)
            self.assertEqual(
                cipher_test, param.cipher, f"\nClass method encrypt output wrong result. {param_string}"
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
                # normal way of setting class instance variable
                setattr(self.rsa, pkey, getattr(param, pkey))
                # directly setting class variable
                setattr(RSA.RSA, pkey, getattr(param, pkey))
            param_string = ",".join([f"{tag}:{getattr(param, tag)}" for tag in ["p", "q", "n", "phi", "cp_index", "e", "d"]])
            decrypted_msg = self.method_wrapper(self.rsa.decrypt, param.cipher)
            self.assertEqual(
                decrypted_msg, param.msg, 
                f"\nClass method decrypt output wrong result. {param_string}"
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
            self.cls_attr_cleanup(self.rsa, ["p", "q", "n", "phi", "e", "d"])
            self.method_wrapper(self.rsa.compute_key, param.p, param.q, param.cp_index)
            param_string = ",".join([f"{tag}:{getattr(param, tag)}" for tag in ["p", "q", "n", "phi", "cp_index", "e", "d"]])
            cipher_test = self.method_wrapper(self.rsa.encrypt, param.msg)
            self.assertEqual(
                cipher_test, param.cipher, f"\nClass method encrypt output wrong result. {param_string}"
            )
            decrypted_msg = self.method_wrapper(self.rsa.decrypt, cipher_test)
            self.assertEqual(
                decrypted_msg, param.msg, f"\nClass method decrypt output wrong result. {param_string}"
            )
            curr_score += 2
            set_score(curr_score)
