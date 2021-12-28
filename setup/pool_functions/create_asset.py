from algosdk.future.transaction import AssetConfigTxn, MultisigTransaction
from ..helper_functions import wait_for_confirmation, get_minted_asset_id
from ..account_generation.get_creator_multisig import multisig

def create_asset(client, creator_address, token_reserve_pool_address, token_reserve_pool_private_key):


    txn = AssetConfigTxn(
            sender=token_reserve_pool_address,
            sp=client.suggested_params(),
            total=10000000000000000000,
            decimals=0,
            default_frozen=False,
            manager=creator_address,
            reserve=token_reserve_pool_address,
            freeze=creator_address,
            clawback=creator_address,
            unit_name="LCASITA",
            asset_name="LCASA",
            url="",
            metadata_hash=None,
            note=None,
            lease=None,
            rekey_to=None,
    )

   

    # sign the transaction
    signed_transaction = txn.sign(token_reserve_pool_private_key)

    # Send the transaction to the network and retrieve the txid.
    txid = client.send_transaction(signed_transaction)
    
    # Wait for the transaction to be confirmed
    result = wait_for_confirmation(client,txid)


    get_minted_asset_id(client, txid, creator_address, token_reserve_pool_address)

    return result