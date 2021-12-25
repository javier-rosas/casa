
import base64 
from algosdk import mnemonic, encoding
from algosdk import account





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



def print_log(log):
    strlog = base64.b64decode(log)

    strlog = strlog.decode('utf-8')
    print(int(strlog.hex(), 16))
    print(type(strlog))
    #print("\t{}".format(strlog))



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
def is_opted_in_asset(algod_client, asset_id, private_key): 

    account_info = algod_client.account_info(private_key)
    holding = None
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1    
        if (scrutinized_asset['asset-id'] == asset_id):
            holding = True
            break
    
    return holding



def address_from_private_key(private_key):
    return account.address_from_private_key(private_key)