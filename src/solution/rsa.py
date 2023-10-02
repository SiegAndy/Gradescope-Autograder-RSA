# Place your imports here


class RSA(object):
    """
    RSA Encryption/Decryption Algorithm

    Parameters:
    p, q        : int       prime numbers
    n           : int       modulus for public&private key
    phi         : int       lambda(n)
    e           : int       public key
    d           : int       private key

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

    def encrypt(self, msg: int) -> int:
        """Enrypt the message"""
        # TODO: Implement me
        pass

    def decrypt(self, cipher_text: int) -> int:
        """Decrypt the cipher text"""
        # TODO: Implement me
        pass

    def compute_key(self, p: int, q: int, coprime_index: int = 0) -> int:
        """
        Compute Public&Private Key and assign them to class attribute

        Compute nth coprime according to the coprime index (default to 0)
        """
        # TODO: Implement me
        pass
