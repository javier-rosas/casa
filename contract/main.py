# This version has not been audited for security.


from pyteal import *


def approval_program():


    add_pool = Seq([

        Return(Int(1))

    ])



    '''
    BORROW ALGOS:
    '''
    borrow = Seq([

        Return(Int(1))

    ])


    '''
    DEPOSIT ALGOS:
    '''
    deposit = Seq([

        Return(Int(1))

    ])


    '''
    CALL APPLICATION:
        - Conditional with 3 options: 
            1) Deposit 
            2) Borrow 
            3) Cash out 
    '''
    '''
    handle_noop = Cond(
        [       Txn.application_args[0] == Bytes("add_pool"),  add_pool       ],
        [       Txn.application_args[0] == Bytes("user_deposit"), deposit       ],
        [       Txn.application_args[0] == Bytes("borrower_cashout"),  borrow       ],
        
    )

    '''
    handle_noop = Return(Int(1))
    


  
    '''
    ON CREATION: 
        - Does not do anything
    '''
    on_creation = Seq([
        
        #App.globalPut(Bytes("Creator"), Txn.sender()),

        Return(Int(1))
    ])



    '''
    USER OPT IN: 
        - Does not do anything. 
    '''
    handle_optin = Seq([

        Return(Int(1))

    ])



    '''
    ON CLOSEOUT: 
        - Return 0
    '''
    handle_closeout = Return(Int(1))



    '''
    ON UPDATE: 
        - Check if the sender is the creator of the applicaiton  
    '''
    handle_updateapp = Return(Int(1))



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


'''
CLEAR STATE PROGRAM:

    - Returns 0
'''
def clear_state_program():
    program = Return(Int(1))
    return program


if __name__ == "__main__":
    with open("contract/raw_teal/casa_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=5)
        f.write(compiled)

    with open("contract/raw_teal/casa_clear.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=5)
        f.write(compiled)