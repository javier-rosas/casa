
import base64 
import sys
import os

from algosdk import mnemonic, encoding, logic, account
from pyteal import compileTeal, Mode





# compiles and returns approval_program
def compile_approval_program(algod_client):

    curr_dir = os.getcwd()

    sys.path.append(curr_dir)
    from contract.main import approval_program
    sys.path.remove(curr_dir)
    
    # get PyTeal approval program
    approval_program_ast = approval_program()
    # compile program to TEAL assembly
    approval_program_teal = compileTeal(approval_program_ast, mode=Mode.Application, version=5)
    # compile program to binary
    approval_program_compiled = compile_program(algod_client, approval_program_teal)

    return approval_program_compiled


# compiles and returns clear_state_program
def compile_clear_state_program(algod_client):

    curr_dir = os.getcwd()

    sys.path.append(curr_dir)
    from contract.main import clear_state_program
    sys.path.remove(curr_dir)
    
   # get PyTeal clear state program
    clear_state_program_ast = clear_state_program()
    # compile program to TEAL assembly
    clear_state_program_teal = compileTeal(clear_state_program_ast, mode=Mode.Application, version=5)
    # compile program to binary
    clear_state_program_compiled = compile_program(algod_client, clear_state_program_teal)

    return clear_state_program_compiled




# helper function to compile program source
def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response["result"])


# helper function that converts a mnemonic passphrase into a private signing key
def get_private_key_from_mnemonic(mn):
    private_key = mnemonic.to_private_key(mn)
    return private_key


# helper function that waits for a given txid to be confirmed by the network
def wait_for_confirmation(client, txid):
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get("confirmed-round") and txinfo.get("confirmed-round") > 0):
        print("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print(
        "Transaction {} confirmed in round {}.".format(
            txid, txinfo.get("confirmed-round")
        )
    )
    return txinfo


# convert 64 bit integer i to byte string
def intToBytes(i):
    return i.to_bytes(8, "big")


def wait_for_round(client, round):
    last_round = client.status().get("last-round")
    print(f"Waiting for round {round}")
    while last_round < round:
        last_round += 1
        client.status_after_block(last_round)
        print(f"Round {last_round}")



def print_confirmation(result):
    print("Result confirmed in round: {}".format(result['confirmed-round']))



def print_single_log(log):
        
    # integer
    strlog = base64.b64decode(log)
    integer = int(strlog.hex(), 16)

    # string
    string = base64.b64decode(log).decode('UTF-8')

    # print
    dictionary = {"Int": integer, "String": string}

    print(dictionary) 



def print_logs(result):
    print("\nLogs:\n")
    for log in result['logs']:
        print_single_log(log)


def format_state(state):
    formatted = {}
    for item in state:
        key = item["key"]
        value = item["value"]
        try: 
            
            formatted_key = base64.b64decode(key).decode("utf-8")

        except Exception: 


            formatted_key = base64.b64decode(key)
            lst = formatted_key.split(b' | ')
            key_32_bytes = lst[0]
            user_deposited = lst[1]

            key_32_bytes = encoding.encode_address(key_32_bytes)
            key_32_bytes  = key_32_bytes.encode()
            formatted_key = key_32_bytes + b' | ' + user_deposited


        if value["type"] == 1:
            # byte string
      
            formatted_value = value["bytes"]
            formatted[formatted_key] = formatted_value
        else:
            # integer
            formatted[formatted_key] = value["uint"]
    return formatted



# read user local state
def read_local_state(client, addr, app_id):
    results = client.account_info(addr)
    for local_state in results["apps-local-state"]:
        if local_state["id"] == app_id:
            if "key-value" not in local_state:
                
                return {}
            
            return format_state(local_state["key-value"])
    return {}



# read app global state
def read_global_state(client, addr, app_id):
    results = client.account_info(addr)
    apps_created = results["created-apps"]
    for app in apps_created:
        if app["id"] == app_id:
            try:
                return format_state(app["params"]["global-state"])
            except KeyError: 
                return "No global state at this time."
    return {}

    
# returns true if the account has opted into the application, false otherwise
def is_opted_in_app(algod_client, user_address, app_id):
    account_info = algod_client.account_info(user_address)
    for a in account_info['apps-local-state']:
        if a['id'] == app_id:
            return True
    return False



# https://developer.algorand.org/docs/get-details/asa/
def is_opted_in_asset(algod_client, asset_id, address): 

    account_info = algod_client.account_info(address)
    holding = False
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1    
        if (scrutinized_asset['asset-id'] == asset_id):
            holding = True
            break
    return holding


def is_application_address(client, application_address, pool_address):

    account_info = client.account_info(pool_address)

    try:
        auth_address = account_info['auth-addr']

    except KeyError:
        
        return False


    return auth_address == application_address



def delete_all_apps_from_account(client, address, private_key, delete_app):

    account_info = client.account_info(address)
    for app in account_info['created-apps']: 
        delete_app(client, private_key, app['id'])

    print("Deleted all apps from account:", address)



def delete_all_apps_from_account_except_last(client, address, private_key, delete_app):

    account_info = client.account_info(address)
    for app in account_info['created-apps'][:-1]: 
        delete_app(client, private_key, app['id'])

    # application address
    application_address = logic.get_application_address(account_info['created-apps'][-1]['id'])
    app_id = account_info['created-apps'][-1]['id']

    print("Deleted all apps from account:", address, "except last app_id:", app_id, "app_address:", application_address)



def print_account_info(client, address):

    import pprint
    account_information = client.account_info(address)
    pprint.pprint(account_information)



def print_asset_holding(algodclient, account, assetid):
    import json
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1        
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break


def address_from_private_key(private_key):
    return account.address_from_private_key(private_key)


def mnemonic_to_public_key(mnemonic):
    return mnemonic.to_public_key(mnemonic)