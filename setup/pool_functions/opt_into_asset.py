from algosdk.future.transaction import AssetTransferTxn
from ..helper_functions import wait_for_confirmation


# opt pools into assets (USDC, INDEX TOKEN)
def opt_into_asset(client, sender, private_key, asset_id):

    txn = AssetTransferTxn(
        sender,
        sp=client.suggested_params(),
        receiver=sender,
        amt=0,
        index=asset_id,
        close_assets_to=None,
        revocation_target=None,
        note=None,
        lease=None,
        rekey_to=None,
    )

    signed_transaction = txn.sign(private_key)
    tx_id = client.send_transaction(signed_transaction)

    # await confirmation
    result = wait_for_confirmation(client, tx_id)


    return result



