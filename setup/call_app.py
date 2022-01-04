from algosdk import account
from algosdk.future import transaction
from algosdk.future.transaction import  MultisigTransaction

from .helper_functions import wait_for_confirmation

# call application
def call_app(
            client, 
            creator_address, 
            private_key, 
            index, 
            app_args, 
            msig=False, 
            accounts=None):

    if not msig:
        # declare sender
        sender = account.address_from_private_key(private_key)
        print("Call from account:", sender)

        # get node suggested parameters
        params = client.suggested_params()
    
        # create unsigned transaction
        txn = transaction.ApplicationNoOpTxn(sender, params, index, app_args)

        # sign transaction
        signed_txn = txn.sign(private_key)
        tx_id = signed_txn.transaction.get_txid()

        # send transaction
        client.send_transactions([signed_txn])

        # await confirmation
        result = wait_for_confirmation(client, tx_id)

        return result

    if msig: 
        import sys
        import os

        # get current working directory
        curr_dir = os.getcwd()
        # setup/account_generation/generate_creator_multisig.py import multisig
        sys.path.append(curr_dir + '/setup/')
        from account_generation.get_creator_multisig import multisig
        sys.path.remove(curr_dir + '/setup/')
        

        # declare sender
        sender = creator_address
        print("Call from account:", sender)

        # get node suggested parameters
        params = client.suggested_params()
    
        # create unsigned transaction
        txn = transaction.ApplicationNoOpTxn(
                                            sender=sender,
                                            sp=params,
                                            index=index,
                                            app_args=app_args,
                                            accounts=accounts,
                                            foreign_apps=None,
                                            foreign_assets=None,
                                            note=None,
                                            lease=None,
                                            rekey_to=None)

        multisig_object = multisig('creator_multisig_accounts')

        # create a SignedTransaction object
        multisig_transaction = MultisigTransaction(txn, multisig_object)

        # sign transaction
        multisig_transaction.sign(private_key)

        tx_id = multisig_transaction.transaction.get_txid()

        # send transaction
        client.send_transactions([multisig_transaction])

        # await confirmation
        result = wait_for_confirmation(client, tx_id)

        # transaction response
        client.pending_transaction_info(tx_id)


        return result


