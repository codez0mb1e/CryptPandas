# %% Import dependencies
import os
import pandas as pd

from cryptpandas.key_vaults import AzureKeyVaultManager
from cryptpandas.protect import DataframeProtector, ProtectorSettings


# %% Set env
AZURE_KEY_VAULT_NAME: str = "cryptpandas-k"
os.environ["AZURE_CLIENT_ID"] = "***"
os.environ["AZURE_CLIENT_SECRET"] = "***"
os.environ["AZURE_TENANT_ID"] = "***"


# %% Tests
def test_e2e_protector():
    # prepare
    expected_df = pd.DataFrame({
         "X": range(5),
         "Y": ["a", "b", "c", "d", "e"],
         "Z": [True, False, True, False, True]
        })

    settings = ProtectorSettings("temp/encrypted.enc", "who-is-satoshi-nakamoto", "who-is-vitalik")
    protector = DataframeProtector(settings, AzureKeyVaultManager(AZURE_KEY_VAULT_NAME))

    # act
    protector.protect(expected_df)
    actual_df = protector.unprotect()

    # assert
    assert(
        isinstance(actual_df, pd.DataFrame) and
        (actual_df == expected_df).all().all()
    )
