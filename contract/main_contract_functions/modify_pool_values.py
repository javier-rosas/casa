from pyteal import * 

'''
MODIFY POOL VALUES AFTER BORROW FUNCTION:
'''
@Subroutine(TealType.none)
def modify_pool_values_borrow(user_borrow_amount):
    
    # amount borrowed in the pool
    pool_amount_borrowed = App.localGet(Gtxn[1].sender(), Bytes('pool_borrowed'))

    # amount borrowed in the pool after borrow
    new_pool_amount_borrowed = pool_amount_borrowed + user_borrow_amount

    return Seq([
        
        App.localPut( Gtxn[1].sender(), Bytes("pool_borrowed"), new_pool_amount_borrowed  ),

        Return()
    ])


'''
MODIFY POOL VALUES AFTER DEPOSIT FUNCTION:
'''
@Subroutine(TealType.none)
def modify_pool_values_deposit(user_deposit_amount):
    
    # APP_ID 
    asset_id = Gtxn[0].application_args[1]

    # Ex: "user_deposited | APP_ID: 02141"
    user_deposited_key = Concat(Bytes('deposited | APP_ID: '), asset_id)

    # total amount deposited in the pool
    pool_amount_deposited = App.globalGet(user_deposited_key)

    # amount deposited in the pool after deposit
    new_pool_amount_deposited = pool_amount_deposited + user_deposit_amount

    return Seq([
        
        App.globalPut( user_deposited_key, new_pool_amount_deposited  ),

        Return()
    ])