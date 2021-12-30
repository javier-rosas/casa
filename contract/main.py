# This version has not been audited for security.


from pyteal import *
from .helper_functions import *


def approval_program():



    '''
    DEPOSIT ALGOS:
    '''
    deposit = Seq([

        handle_deposit_function(),
        Approve()

    ])


    '''
    CALL APPLICATION:
        - Conditional with 3 options: 
            1) Deposit 
            2) Borrow 
            3) Cash out 
    '''
    
    handle_noop = Cond(
        [       Txn.application_args[0] == Bytes("deposit"),  deposit       ]
    )

    


    # On creation, the kyc_account (or creator account) is placed in global storage 
    # Returns 1
    on_creation = Seq([
        
        App.globalPut( Bytes("kyc_account"), Txn.sender() ),
        Assert( Global.group_size() == Int(1)                              ),
        Return( Int(1) )
    ])



    '''
    USER OPT IN: 
        - Does not do anything. 
    '''
    handle_optin = Seq([
        #handle_optin_func(),
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

        handle_updateapp_function(),
        Approve()
        
    ])



    '''
    ON DELETE:
        - Does not do anything
    '''
    handle_deleteapp = Return(Int(1))



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