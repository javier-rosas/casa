from pyteal import *

'''
DEPOSIT ALGOS FUNCTION:
'''
@Subroutine(TealType.none)
def deposit_func():

    # ASSET_ID
    asset_id = Gtxn[0].application_args[1]

    # Ex: "user_deposited | APP_ID: 02141"
    user_deposited_key = Concat(Bytes('user_deposited | APP_ID: '), asset_id)

    # gets current amount of asset deposited by user (stored in the user's local storage)
    user_total_current_amount_deposited = App.localGet(Gtxn[1].sender(), user_deposited_key)
    
    # amount sent in transaction 1
    user_deposit_amount = Gtxn[1].amount()

    # amount amount deposited by user 
    user_new_total_amount_deposited = user_total_current_amount_deposited + user_deposit_amount


    return Seq([

        
        Assert( Global.group_size() == Int(2)                                  ),

        # "deposit" and ASSET ID
        Assert( Txn.application_args.length() == Int(2)                ),

        Assert( Gtxn[0].sender() == Gtxn[1].sender()                           ),
        Assert( Gtxn[0].receiver() == Gtxn[1].receiver()                       ),
        Assert( Gtxn[0].type_enum() == TxnType.ApplicationCall             ),

        
        Assert( Gtxn[1].type_enum() == TxnType.Payment                     ),
        Assert( Gtxn[1].close_remainder_to() == Global.zero_address()      ),
        Assert( Gtxn[1].rekey_to() == Global.zero_address()                ),
        Assert( Gtxn[1].receiver() == Global.current_application_address()                              ),

        modify_pool_values_deposit(user_deposit_amount),


        App.localPut( Gtxn[1].sender(), user_deposited_key, user_new_total_amount_deposited       ),
        Return()

    ])