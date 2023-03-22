
# %% 
import os
os.chdir("..")

# %%
AZURE_KEY_VAULT_NAME: str = "keymaker-akv"
os.environ["AZURE_CLIENT_ID"] = "***"
os.environ["AZURE_CLIENT_SECRET"] = "***"
os.environ["AZURE_TENANT_ID"] = "***"

# %%
import pytest
from cryptpandas.key_vaults import AzureKeyVaultManager, KeyVaultException


# %%
def test_azure_key_vault_manager() -> None:
    kv_mngr = AzureKeyVaultManager(AZURE_KEY_VAULT_NAME)
    assert(
        isinstance(kv_mngr, AzureKeyVaultManager) and
        kv_mngr.api_version == "7.4"
    )

@pytest.mark.parametrize("key", ["who-is-satoshi-nakamoto", "who-is-vitalik"])
def test_get_key_as_string(key: str) -> None:
    kv_mngr = AzureKeyVaultManager(AZURE_KEY_VAULT_NAME)
    secret = kv_mngr.get_secret(key)
    assert(
        isinstance(secret, str) and
        len(secret) > 0
    )

@pytest.mark.parametrize("key", ["who-is-satoshi-nakamoto", "who-is-vitalik"])
def test_get_key_as_byte(key: str) -> None:
    kv_mngr = AzureKeyVaultManager(AZURE_KEY_VAULT_NAME)
    secret = kv_mngr.get_secret(key, as_bytes=True)
    assert(
        isinstance(secret, bytes) and
        len(secret) > 0
    )


@pytest.mark.parametrize("key", ["iamnotexists", "(:"])
@pytest.mark.xfail(raises=KeyVaultException)
def test_get_not_exist_key(key: str) -> None:
    kv_mngr = AzureKeyVaultManager(AZURE_KEY_VAULT_NAME)
    _ = kv_mngr.get_secret(key, as_bytes=True)
