from algosdk.future.transaction import PaymentTxn

from ..helper_functions import wait_for_confirmation


def rekey_pool_to_application(client, application_address, pool_address, pool_private_key):
    
    
    # To rekey an account to a new address, add the `rekey_to` argument to creation.
    # After sending this rekeying transaction, every transaction needs to be signed by the private key of the new address
    rekeying_txn = PaymentTxn(
        sender=pool_address,
        sp=client.suggested_params(),
        receiver=pool_address,
        amt=0,
        close_remainder_to=None,
        note=None,
        lease=None,
        rekey_to=application_address,
    )
    
    # sign transaction
    signed_txn = rekeying_txn.sign(pool_private_key)
    tx_id = client.send_transaction(signed_txn)

    # await confirmation
    result = wait_for_confirmation(client, tx_id)

    print("Account", pool_address, "has been rekeyed to", application_address)

    return result