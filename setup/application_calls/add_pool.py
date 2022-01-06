from ..call_app import call_app

def add_pool(
    client, 
    app_args, 
    creator_address, 
    app_id,
    creator_private_key_list,
    accounts=None,
    ):



    # call app with msig=True (manager address is a multisig account)
    result = call_app(
                    client=client, 
                    creator_address=creator_address, 
                    index=app_id, 
                    app_args=app_args, 
                    creator_private_key_list=creator_private_key_list,
                    creator=True,
                    msig=True,
                    accounts=accounts
                    )    

    return result 




    