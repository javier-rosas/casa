import sys
import os

from algosdk import logic
from algosdk.future import transaction
from algosdk.future.transaction import  MultisigTransaction




# get current working directory
curr_dir = os.getcwd()

# setup/helper_functions.py imports 
sys.path.append(curr_dir)
from setup.helper_functions import (wait_for_confirmation, 
                                    compile_approval_program, 
                                    compile_clear_state_program)

sys.path.remove(curr_dir)

# setup/account_generation/generate_creator_multisig.py import multisig
sys.path.append(curr_dir + '/setup/')
from account_generation.get_creator_multisig import multisig
sys.path.remove(curr_dir + '/setup/')



# create new application
def helper(
    client,
    creator_address,
    approval_program,
    clear_program,
    app_id,
    creator_private_key_list:list
):


    # define sender as creator
    sender = creator_address


    # get node suggested parameters
    params = client.suggested_params()


    # create unsigned transaction
    txn = transaction.ApplicationUpdateTxn(
            
        sender,
        params,
        app_id,
        approval_program,
        clear_program,
        app_args=None,
        accounts=None,
        foreign_apps=None,
        foreign_assets=None,
        note=None,
        lease=None,
        rekey_to=None,
    )

    msig = multisig(creator=True)

    
    # create a SignedTransaction object
    multisig_transaction = MultisigTransaction(txn, msig)

    # sign transaction
    for private_key in creator_private_key_list: 
        multisig_transaction.sign(private_key)
    
    tx_id = multisig_transaction.transaction.get_txid()

    # send transaction
    client.send_transactions([multisig_transaction])

    # await confirmation
    result = wait_for_confirmation(client, tx_id)

    # transaction response
    transaction_response = client.pending_transaction_info(tx_id)

  
    # application address
    application_address = logic.get_application_address(app_id)

    print("Application was modified with app_id:", app_id, "and with application address:", application_address)

    # return application_id and application_address
    return result


def update_app(algod_client, creator_address, creator_private_key_list, app_id):

   
    approval_program_compiled = compile_approval_program(algod_client)

    clear_state_program_compiled = compile_clear_state_program(algod_client)


    # create new application
    helper(
        algod_client,
        creator_address,
        approval_program_compiled,
        clear_state_program_compiled,
        app_id,
        creator_private_key_list=creator_private_key_list
    )

    return app_id





