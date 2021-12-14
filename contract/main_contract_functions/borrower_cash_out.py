from pyteal import *

'''
BORROW ALGOS FUNCTION: 
'''
@Subroutine(TealType.none)
def borrower_cash_out():

    # string: [pool address] | user_deposited 
    user_deposited_key = Concat(Gtxn[1].receiver(), Bytes(" | "), Bytes("user_deposited"))

    # gets current amount deposited by user (stored in the user's local storage)
    current_amount_deposited = App.localGet(Gtxn[1].sender(), user_deposited_key)

    # string: [pool address] | user_borrowed
    user_borrowed_key = Concat(Gtxn[1].receiver(), Bytes(" | user_borrowed"))
    # gets current amount borrowed by user (stored in the user's local storage)
    current_amount_borrowed = App.localGet(Gtxn[1].sender(), user_borrowed_key)

    user_borrow_amount = Btoi(Txn.application_args[1])

    user_new_borrowed_amount = current_amount_borrowed + user_borrow_amount

    max_amount_allowed_to_borrow = (current_amount_deposited / Int(10)) * Int(8)
        
    
    return Seq([
        
        Assert( Global.group_size() == Int(1)                              ),
        Assert( Txn.type_enum() == TxnType.ApplicationCall                 ),
        Assert( Txn.application_args.length() == Int(2)                    ),


        Assert( user_new_borrowed_amount <= max_amount_allowed_to_borrow ), 
        
        modify_pool_values_borrow(user_borrow_amount),

        App.localPut( Gtxn[1].receiver(), user_borrowed_key, user_new_borrowed_amount  ),
        Return()
    ])