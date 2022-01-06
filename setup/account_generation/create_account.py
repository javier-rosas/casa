import json

from algosdk import account, mnemonic


# generate algorand public and private keys 
def generate_algorand_keypair():

    private_key, address = account.generate_account()
    print()
    print("My address: {}".format(address))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))
    print()
    return address, mnemonic.from_private_key(private_key)


def generate_new_application_accounts():
    # USDC Lender Pool
    lender_usdc_pool_address, lender_usdc_pool_mnemonic = generate_algorand_keypair()

    # Token Reserve Pool 
    token_reserve_pool_address, token_reserve_pool_mnemonic = generate_algorand_keypair()

    # Token Active Pool
    token_active_pool_address, token_active_pool_mnemonic = generate_algorand_keypair()

    # Token Stake Pool 
    token_stake_pool_address, token_stake_pool_mnemonic = generate_algorand_keypair()

    # USDC Payback Pool 
    payback_pool_address, payback_pool_mnemonic = generate_algorand_keypair()


    with open("keys.json", "r+") as jsonFile:
        data = json.load(jsonFile)

        data["lender_usdc_pool_address"] = lender_usdc_pool_address
        data["lender_usdc_pool_mnemonic"] = lender_usdc_pool_mnemonic

        data["token_reserve_pool_address"] = token_reserve_pool_address
        data["token_reserve_pool_mnemonic"] = token_reserve_pool_mnemonic

        data["token_active_pool_address"] = token_active_pool_address
        data["token_active_pool_mnemonic"] = token_active_pool_mnemonic 

        data["token_stake_pool_address"] = token_stake_pool_address
        data["token_stake_pool_mnemonic"] = token_stake_pool_mnemonic 

        data["payback_pool_address"] = payback_pool_address
        data["payback_pool_mnemonic"] = payback_pool_mnemonic

        jsonFile.seek(0)  # bring cursor to the top
        json.dump(data, jsonFile, indent = 6)
        jsonFile.truncate()

