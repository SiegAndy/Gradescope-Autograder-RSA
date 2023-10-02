# Place your imports here


from math import gcd
from typing import List


class RSA:
    """
    RSA Encryption/Decryption Algorithm

    Parameters:
    p, q        : int       prime numbers
    n           : int       modulus for public&private key
    phi         : int       lambda(n)
    e           : int       public key
    d           : int       private key

    public_key  : int, int  (n, e)
    private_key : int, int  (n, d)

    Method:
    compute_key  : int, int -> None     compute public private key from p, q
    encrypt     : int -> int            encrypte msg
    decrypt     : int -> int            decrypt cipher text
    """

    p: int
    q: int
    n: int
    phi: int
    e: int
    d: int

    public_key: List[int]
    private_key: List[int]

    def encrypt(self, msg: int) -> int:
        """Enrypt the message"""
        # c = m^e mod n
        return pow(msg, self.e, self.n)

    def decrypt(self, cipher_text: int) -> int:
        """Decrypt the cipher text"""
        # m = c^d mod n
        return pow(cipher_text, self.d, self.n)

    def compute_key(self, p: int, q: int, coprime_index: int = 0) -> None:
        """Compute Public&Private Key and assign them to class attribute"""
        self.p = p
        self.q = q
        # modulus n
        self.n = p * q
        # eular totient of n
        self.phi = (p - 1) * (q - 1)

        # pick e as the coprime_index-th coprime for phi
        self.e = 0
        coprime_count = 0
        for i in range(2, self.phi):
            if gcd(i, self.phi) == 1:
                coprime_count += 1
            if coprime_count == coprime_index:
                self.e = i
                break
        if self.e == 0:
            raise AttributeError(
                "compute_key: Not enough coprimes to satisfy coprime index"
            )
        # compute d by e^{-1} mod phi
        self.d = pow(self.e, -1, self.phi)

        # assign public key and private key
        self.public_key = [
            self.n,
            self.e,
        ]
        self.private_key = [
            self.n,
            self.d,
        ]


# rsa = RSA()
# rsa.compute_key(67, 83, 3)
# cipher = rsa.encrypt(24)
# msg = rsa.decrypt(cipher)
# print(cipher, msg)
