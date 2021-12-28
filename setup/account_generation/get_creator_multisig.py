import json
from algosdk.future.transaction import Multisig


def multisig():
    # open json file with address and mnemonic data
    f = open('keys.json')
    data = json.load(f)


    # create a multisig account
    version = 1  # multisig version
    threshold = 1  # how many signatures are necessary

    account_1 = data['creator_multisig_accounts']['creator_address_1']

    account_2 = data['creator_multisig_accounts']['creator_address_2']

    msig = Multisig(version, threshold, [account_1, account_2])

    # Closing json file
    f.close()

    return msig







