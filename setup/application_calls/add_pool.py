from ..call_app import call_app

def add_pool(
    client, 
    app_args, 
    creator_address, 
    creator_private_key, 
    app_id):


    # arg list 0 index = add_pool_arg, 1 index = pool_name_arg, 2 index = pool_name_address_arg
    args = app_args

    # call app with msig=True (manager address is a multisig account)
    result = call_app(client, creator_address, creator_private_key, app_id, args, msig=True)    

    return result 




    