import json
from math import gcd
import random
from typing import List

from json import JSONEncoder
class RSAJSONEncoder(JSONEncoder):
        def default(self, o):
            if hasattr(o, "toJSON"):
                return o.toJson()    
            else:
                return o.__dict__


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

    def toJson(self):
        ignore_keys = [key for key in self.__dict__.keys() if key.startswith("_")]
        json_dict = self.__dict__.copy()
        for key in ignore_keys:
            json_dict.pop(key, None)
        return json_dict

class RSATest:
    compute_key: List[RSAParams]
    encryption: List[RSAParams]
    decryption: List[RSAParams]


random.seed(0)


def primes(start_num: int = 1, end_num: int = 95):
    current = start_num
    while current <= end_num:
        current += 1
        while True:
            for i in range(start_num + 1, current // 2 + 1):
                if current % i == 0:
                    current += 1
                    break
            else:
                break
        # print(current)
        yield current


def generate_params(prime_list: List[int]) -> RSAParams:
    instance = RSAParams()
    while True:
        p, q = random.choices(prime_list, k=2)
        if p == q or abs(p - q) <= 20 or abs (p - q) >= 60:
            continue
        if p > q:
            instance.p = q
            instance.q = p
        else:
            instance.p = p
            instance.q = q
        # modulus n
        instance.n = instance.p * instance.q
        # eular totient of n
        instance.phi = (instance.p - 1) * (instance.q - 1)

        # pick e as the coprime_index-th coprime for phi
        instance.e = 0
        instance.cp_index = 0
        coprime_list = []
        for i in range(2, instance.phi):
            if gcd(i, instance.phi) == 1:
                coprime_list.append(i)
        if len(coprime_list) == 0:
            continue
        instance.cp_index = random.randint(1, min(10, len(coprime_list)))
        instance.e = coprime_list[instance.cp_index-1]
        # print(instance.p, instance.q, instance.e, instance.cp_index, coprime_list)

        # compute d by e^{-1} mod phi
        instance.d = pow(instance.e, -1, instance.phi)

        instance.msg = random.randint(30, 100)

        instance.cipher = pow(instance.msg, instance.e, instance.n)

        decrypted = pow(instance.cipher, instance.d, instance.n)

        assert decrypted == instance.msg

        return instance


def generate_instance():
    prime_list = []
    for prime in primes():
        prime_list.append(prime)
    grading_json = {
        "compute_key": [generate_params(prime_list) for i in range(5)],
        "encryption": [generate_params(prime_list) for i in range(5)],
        "decryption": [generate_params(prime_list) for i in range(5)],
    }
    with open("grading.json", "w", encoding="utf-8") as output:
        json.dump(grading_json, output, default=lambda x: x.toJson(), indent=4)


generate_instance()
# for i in range(2, 1260):
#     if gcd(i, 1260) == 1:
#         print(i)
