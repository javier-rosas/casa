from pyteal import *
from ..helper_contract_functions import is_creator, local_put



'''
Add pool: 

    1) Give it a pool id in global state 
    2) Send it LCASA ( 1:1 with loan goal )
    3) Send it DCASA ( 1:1 with loan goal + interest )

'''
@Subroutine(TealType.none)
def add_pool(goal, interest_rate, term):
    
    # Pool address 
    pool_address = Txn.application_args[1]

    # Txn sender 
    sender = Txn.sender()

    return Seq[(
        
        Assert(     is_creator(sender) == Int(1) ),

        Assert(     Global.group_size() == Int(1) ),

        Assert(     Txn.type_enum() == TxnType.ApplicationCall ),

        Assert(     Txn.application_args.length() == Int(1) ),

        local_put(      pool_address, "is_pool", 1 ),
        local_put(      pool_address, "goal", goal ),
        local_put(      pool_address, "interest_rate", interest_rate ),
        local_put(      pool_address, "term", term ),
        

        Return()
    )]

