from algosdk.future import transaction
from .helper_functions import wait_for_confirmation
import sys
import os


# relative imports 
curr_dir = os.getcwd()

sys.path.append(curr_dir)
from setup.helper_functions import (wait_for_confirmation, 
                                    read_global_state, 
                                    address_from_private_key,
                                    compile_approval_program, 
                                    compile_clear_state_program)
sys.path.remove(curr_dir)



# update application
def helper(
    client, 
    private_key, 
    app_id, 
    approval_program, 
    clear_program):

    # declare sender
    sender = address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationUpdateTxn(sender, params, app_id, approval_program, clear_program)

    # sign transaction
    signed_txn = txn.sign(private_key)

    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    result = wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Updated app-id:", transaction_response["txn"]["txn"]["apid"])

    return result


def update_app(algod_client, creator_private_key):


    approval_program_compiled = compile_approval_program(algod_client)

    clear_state_program_compiled = compile_clear_state_program(algod_client)


    # create list of bytes for app args
    app_id = int(input("App id for update: "))

    # create new application
    app_id = helper(
        algod_client, 
        creator_private_key, 
        app_id, 
        approval_program_compiled, 
        clear_state_program_compiled)

    # read global state of application
    print( "Global state:", read_global_state(algod_client, address_from_private_key(creator_private_key), app_id) )

    return app_id