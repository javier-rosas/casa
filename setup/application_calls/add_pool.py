from ..call_app import call_app

def add_pool(
    client, 
    app_args, 
    creator_address, 
    creator_private_key, 
    #accounts,
    app_id):



    # call app with msig=True (manager address is a multisig account)
    result = call_app(
                    client=client, 
                    creator_address=creator_address, 
                    private_key=creator_private_key, 
                    index=app_id, 
                    #accounts=accounts,
                    app_args=app_args, 
                    msig=True)    

    return result 




    