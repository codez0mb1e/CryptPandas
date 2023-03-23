import os
from abc import ABC, abstractmethod
from typing import List, Union
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError
from azure.keyvault.secrets import SecretClient


class BaseKeyVaultManager(ABC):
    """Key Vault manager abstraction"""

    @abstractmethod
    def get_secret(self, key: str, as_bytes: bool = False) -> Union[str, bytes]:
        """Request secret value by its key"""
        raise NotImplementedError

class KeyVaultException(Exception):
    """Key Vault base exception"""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AzureKeyVaultManager(BaseKeyVaultManager):
    """Azure KeyVault service manager"""

    def __init__(self, key_vault_name: str) -> None:
        """Initialize Key Vault manager
        
        :param key_vault_name: name of the Key Vault
        :raises KeyVaultException: if environment variables are not set
        """
        for env_var in ["AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_TENANT_ID"]:
            try:
                _ = os.environ[env_var]
            except KeyError:
                raise KeyVaultException(f"Environment variable {env_var} is not set")

        self._client = SecretClient(
            vault_url=f"https://{key_vault_name}.vault.azure.net",
            credential=DefaultAzureCredential(),
        )

    @property
    def api_version(self) -> str:
        """Return current API version

        :returns: string with api version
        """
        return self._client.api_version

    def list_keys(self) -> List[Union[str, None]]:
        """Return list of available key names

        :returns: List of key names or None if no keys in Vault
        """
        keys = self._client.list_properties_of_secrets()
        return [key.name for key in keys]

    def get_secret(self, key: str, as_bytes: bool = False) -> Union[str, bytes]:
        """Request secret by label

        :param secret_name: name of the key
        :param as_byte: return value as bytes (default: as string)
        :raises KeyVaultException: if secret key not found
        :returns: value of the secret
        """
        try:
            secret = self._client.get_secret(key).value
        except ResourceNotFoundError:
            raise KeyVaultException(f"Key {key} not found in Key Vault")

        if as_bytes:
            secret = secret.encode("ascii")

        return secret

    def dispose(self) -> None:
        """Close connection with Key Vault"""
        self._client.close()
