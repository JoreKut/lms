from pydantic import SecretBytes

from app.internal.pkg.handlers import password


class EncryptedSecretBytes(SecretBytes):
    min_length = 6
    max_length = 256

    def crypt_password(self) -> None:
        self._secret_value = password.crypt_password(self._secret_value)
