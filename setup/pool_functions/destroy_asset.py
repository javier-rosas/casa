from algosdk.future.transaction import AssetConfigTxn
from ..helper_functions import wait_for_confirmation

def destroy_asset(client, sender, private_key, asset_id):

    txn = AssetConfigTxn(
            sender,
            sp=client.suggested_params(),
            index=asset_id,
            total=None,
            default_frozen=None,
            unit_name=None,
            asset_name=None,
            manager=None,
            reserve=None,
            freeze=None,
            clawback=None,
            url=None,
            metadata_hash=None,
            note=None,
            lease=None,
            strict_empty_address_check=False,
            decimals=0,
            rekey_to=None,
    )

    signed_transaction = txn.sign(private_key)
    tx_id = client.send_transaction(signed_transaction)

    # await confirmation
    result = wait_for_confirmation(client, tx_id)


    return result

