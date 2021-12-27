from algosdk.future import transaction
from algosdk import account
from pyteal import compileTeal, Mode
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



# create new application
def helper(
    client,
    private_key,
    approval_program,
    clear_program,
    global_schema,
    local_schema,
    app_args,
    extra_pages
):
    # define sender as creator
    sender = account.address_from_private_key(private_key)

    # declare on_complete as NoOp
    on_complete = transaction.OnComplete.NoOpOC.real

    # get node suggested parameters
    params = client.suggested_params()


    # create unsigned transaction
    txn = transaction.ApplicationCreateTxn(
        sender,
        params,
        on_complete,
        approval_program,
        clear_program,
        global_schema,
        local_schema,
        app_args,
        extra_pages
    )

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response["application-index"]
    print("Created new app-id:", app_id)

    return app_id


def create_app(algod_client, creator_private_key):

    # declare application state storage (immutable)
    local_ints = 6
    local_bytes = 0
    global_ints = 1
    global_bytes = 3
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)


    approval_program_compiled = compile_approval_program(algod_client)

    clear_state_program_compiled = compile_clear_state_program(algod_client)


    # create list of bytes for app args
    app_args = []

    # create new application
    app_id = helper(
        algod_client,
        creator_private_key,
        approval_program_compiled,
        clear_state_program_compiled,
        global_schema,
        local_schema,
        app_args,
        extra_pages=3
    )

    # read global state of application
    print( "Global state:", read_global_state( algod_client, address_from_private_key(creator_private_key), app_id) )

    return app_id


