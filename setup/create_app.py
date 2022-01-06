import sys
import os
import json 

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
    global_schema,
    local_schema,
    extra_pages,
    creator_private_key_list:list,
):

  
    # define sender as creator
    sender = creator_address

    # declare on_complete as NoOp
    on_complete = transaction.OnComplete.OptInOC.real

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
                                        app_args=None,
                                        accounts=None,
                                        foreign_apps=None,
                                        foreign_assets=None,
                                        note=None,
                                        lease=None,
                                        rekey_to=None,
                                        extra_pages=extra_pages,
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
    wait_for_confirmation(client, tx_id)

    # transaction response
    transaction_response = client.pending_transaction_info(tx_id)

    # application id 
    app_id = transaction_response["application-index"]

    # application address
    application_address = logic.get_application_address(app_id)

    with open("keys.json", "r+") as jsonFile:
        data = json.load(jsonFile)

        data['app_id'] = app_id
        data['app_address'] = application_address

        jsonFile.seek(0)  # bring cursor to the top
        json.dump(data, jsonFile, indent = 6)
        jsonFile.truncate()

    


    # return application_id and application_address
    return (app_id, application_address)


def create_app(algod_client, creator_address, creator_private_key_list):

    # declare application state storage (immutable)
    local_ints = 8
    local_bytes = 8
    global_ints = 8
    global_bytes = 8
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)


    approval_program_compiled = compile_approval_program(algod_client)

    clear_state_program_compiled = compile_clear_state_program(algod_client)


    # create new application
    app_id = helper(
        algod_client,
        creator_address,
        approval_program_compiled,
        clear_state_program_compiled,
        global_schema,
        local_schema,
        extra_pages=3,
        creator_private_key_list=creator_private_key_list,
    )

    return app_id


