# %%
from abc import ABC, abstractmethod
from typing import List, Union
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# %%
class BaseKeyVaultManager(ABC):
    """Key Vault manages"""

    @abstractmethod
    def get_secret(self, secret_key) -> str:
        raise NotImplementedError("Implement method")


class AzureKeyVaultManager(BaseKeyVaultManager):
    """Azure KeyVault manager"""

    def __init__(self, key_vault_name: str) -> None:
        self._client = SecretClient(
            vault_url=f"https://{key_vault_name}.vault.azure.net", 
            credential=DefaultAzureCredential()
            )

    @property
    def api_version(self) -> str:
        """Return current API version

        :returns: string with api version
        """
        return str(self._client.api_version.value)

    def list_keys(self) -> List[Union[str, None]]:
        """Return list of available key names

        :returns: List of key names or None if no keys in Vault
        """
        keys = self._client.list_properties_of_secrets()
        return [key.name for key in keys]

    def get_secret(self, secret_key: str) -> str:
        """Request secret by label

        :param secret_name: name of the key
        :returns: value of the secret
        """
        return self._client.get_secret(secret_key).value

    def dispose(self) -> None:
        """Close connection with Key Vault"""
        self._client.close()
