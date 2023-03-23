
# %% Set env
from dataclasses import dataclass
from typing import Tuple
from pandas import DataFrame

from cryptpandas.key_vaults import BaseKeyVaultManager
from cryptpandas.encrypt_decrypt import to_encrypted, read_encrypted


@dataclass
class DataframeProtectorSettings:
    encrypted_file_path: str
    password_key: str
    salt_key: str


class DataframeProtector:
    def __init__(self, settings: DataframeProtectorSettings, key_vault_manager: BaseKeyVaultManager) -> None:
        self._settings = settings
        self._key_vault_manager = key_vault_manager

    def _get_secrets(self) -> Tuple[str, bytes]:
        pwd = self._key_vault_manager.get_secret(self._settings.password_key, as_bytes=False)
        salt = self._key_vault_manager.get_secret(self._settings.salt_key, as_bytes=True)
        return pwd, salt

    def encrypt(self, df: DataFrame) -> None:
        pwd, salt = self._get_secrets()
        to_encrypted(df, path=self._settings.encrypted_file_path, password=pwd, salt=salt)

    def decrypt(self) -> DataFrame:
        pwd, salt = self._get_secrets()
        return read_encrypted(path=self._settings.encrypted_file_path, password=pwd, salt=salt)
