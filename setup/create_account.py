from algosdk import account, mnemonic


# generate algorand public and private keys 
def generate_algorand_keypair():

    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))
    return address, mnemonic.from_private_key(private_key)


generate_algorand_keypair()