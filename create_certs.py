import os
import subprocess
from pathlib import Path


def create_private_and_public_keys() -> None:
    """
    Генерирует закрытый и открытый ключи в директории certs, если их нет
    """
    PATH = Path(__file__).parent / "src" / "core" / "certs"
    if (len(os.listdir(PATH)) == 0) is False:
        return
    subprocess.run(["openssl", "genrsa", "-out", PATH / "private.pem", "2048"])
    subprocess.run(
        [
            "openssl",
            "rsa",
            "-in",
            PATH / "private.pem",
            "-outform",
            "PEM",
            "-pubout",
            "-out",
            PATH / "public.pem",
        ]
    )


if __name__ == "__main__":
    create_private_and_public_keys()
