import os
from argparse import ArgumentParser
from typing import TextIO

from rsa import RSA

parser = ArgumentParser(prog="RSA Test", description="RSA Test")
parser.add_argument(
    "-i",
    "--input",
    help="input file containing p, q, msg",
    nargs="?",
    # default="input.txt",
    type=lambda x: is_path_valid(
        arg=x,
        default_path="input.txt",
        mode="r",
    ),
)


def is_path_valid(
    arg,
    default_path: str,
    mode: str,
    encoding: str = "utf-8",
):
    if not os.path.exists(arg):
        if not os.path.exists(default_path):
            return
        arg = default_path
        # parser.error(f"The file {arg} does not exist!")
    return open(arg, mode, encoding=encoding)  # return an open file handle


def read_from_stdin():
    print("Reading parameters in terminal...")
    rsa = RSA()
    while True:
        try:
            line = input("Type in order: p q coprime_index msg\n")
            if line == "" or line == "\n":
                print("No input detected, terminating...")
                return
            p, q, cp_index, msg = line.strip("\n").strip(" ").split(" ")
            rsa.compute_key(int(p), int(q), int(cp_index))
            encrypted = rsa.encrypt(int(msg))
            decrypted = rsa.decrypt(encrypted)
            print(
                f"p: {p}, q: {q}, phi: {rsa.phi}, pu: ({rsa.n}, {rsa.e}), pr: ({rsa.n}, {rsa.d}), message: {msg}, encrypted: {encrypted}, decrypted: {decrypted}"
            )
        except KeyboardInterrupt:
            return
        except ValueError as e:
            print("Error Format. Example input: 67 83 3 24. Detail:", e)
        except Exception as e:
            print("Error: ", e)


def read_from_file(file_handler: TextIO):
    rsa = RSA()
    p = 0
    q = 0
    for index, line in enumerate(file_handler.readlines()):
        try:
            if line == "":
                continue
            if index % 6 == 0:
                p, q = line.strip("\n").split(" ")
                # using third coprime
                rsa.compute_key(int(p), int(q), 3)
            else:
                msg = line.strip("\n")
                encrypted = rsa.encrypt(int(msg))
                decrypted = rsa.decrypt(encrypted)
                print(
                    f"p: {p}, q: {q}, phi: {rsa.phi}, pu: ({rsa.n}, {rsa.e}), pr: ({rsa.n}, {rsa.d}), message: {msg}, encrypted: {encrypted}, decrypted: {decrypted}"
                )
        except KeyboardInterrupt:
            return
        except ValueError as e:
            print(
                "Error Format. Should have first line be (p, q) and following five lines be msg. Detail:",
                e,
            )
            file_handler.close()
            return
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    namespace = parser.parse_args()

    file_handler: TextIO = namespace.input
    if not file_handler:
        read_from_stdin()
    else:
        read_from_file(file_handler)
