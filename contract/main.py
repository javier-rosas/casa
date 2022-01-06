# This version has not been audited for security.


from pyteal import *
from .helper_functions import *


def approval_program():



    # send USDC to lender_usdc_pool
    lender_deposit_usdc = Seq([

        #deposit_usdc_func(),
        Approve()

    ])


    # add a rekeyed pool to the global storage of the application
    add_pool = Seq([
        add_pool_func(),
        Approve()

    ])

    
    # call application. 
    # conditional: 
    #   1) Add pool (only kyc account can do this)
    #   2) Deposit usdc (lenders send usdc to lender_usdc_pool)
    handle_noop = Cond(
        [       Txn.application_args[0] == Bytes("add_pool"),  add_pool                            ],
        [       Txn.application_args[0] == Bytes("lender_deposit_usdc"), lender_deposit_usdc       ],
    )
    


    # On creation, the kyc_account (or creator account) is placed in global storage 
    # Returns 1
    on_creation = Seq([
        
        Assert( Global.group_size() == Int(1)                              ),

        Assert( Txn.application_args.length() == Int(0)                    ),

        Approve()
    ])



    '''
    USER OPT IN: 
        - Does not do anything. 
    '''
    handle_optin = Seq([
        #optin_func(),
        Approve()
    ])



    '''
    ON CLOSEOUT: 
        - Return 0
    '''
    handle_closeout = Return(Int(0))



    '''
    ON UPDATE: 
        - Check if the sender is the creator of the applicaiton  
    '''
    handle_updateapp = Seq([

        updateapp_func(),
        Approve()
        
    ])



    '''
    ON DELETE:
        - Does not do anything
    '''
    handle_deleteapp = Seq([

        updateapp_func(),
        Approve()

    ])



    '''
    MAIN PROGRAM CONDITIONAL:
    '''
    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop],
    )
    return program


# Clears local state for the sender (not recommended as they will loose local variables 
# that will affect their ability to retrieve their LCASA index tokens)
def clear_state_program():
    program = Return(Int(1))
    return program


# compile approval and clear_state programs, and write them to directory: casa/contract/raw_teal
if __name__ == "__main__":
    with open("contract/raw_teal/casa_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=5)
        f.write(compiled)

    with open("contract/raw_teal/casa_clear.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=5)
        f.write(compiled)