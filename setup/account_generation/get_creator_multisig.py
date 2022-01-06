import json
from algosdk.future.transaction import Multisig


def multisig(creator: bool):


    if creator:

        multisig_accounts = "creator_multisig_accounts"
        # keys for addresses that make up the multisig 
        address_1 = 'address_1'
        address_2 = 'address_2'
        address_3 = 'address_3'
        address_4 = 'address_4'
        address_5 = 'address_5'


        # open json file with address and mnemonic data
        f = open('keys.json')
        data = json.load(f)


        # create a multisig account
        version = 1  # multisig version
        threshold = 3  # how many signatures are necessary

        account_1 = data[multisig_accounts][address_1]

        account_2 = data[multisig_accounts][address_2]

        account_3 = data[multisig_accounts][address_3]

        account_4 = data[multisig_accounts][address_4]

        account_5 = data[multisig_accounts][address_5]

        msig = Multisig(version, threshold, [account_1, account_2, account_3, account_4, account_5])

        # Closing json file
        f.close()

        return msig

    else:

        multisig_accounts = "kyc_multisig_accounts"

        address_1 = 'address_1'
        address_2 = 'address_2'

        # open json file with address and mnemonic data
        f = open('keys.json')
        data = json.load(f)


        # create a multisig account
        version = 1  # multisig version
        threshold = 1  # how many signatures are necessary

        account_1 = data[multisig_accounts][address_1]

        account_2 = data[multisig_accounts][address_2]

        msig = Multisig(version, threshold, [account_1, account_2])

        # Closing json file
        f.close()

        return msig











