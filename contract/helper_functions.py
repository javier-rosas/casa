
from pyteal import * 



# Checks if the transaction sender is the creator (kyc_account) of the application
@Subroutine(TealType.uint64)
def is_creator(address: TealType.bytes):

    is_creator = address == App.globalGet(Bytes("kyc_account"))

    return is_creator



@Subroutine(TealType.none)
def handle_optin_func():

    is_kyc_account = is_creator( Gtxn[0].sender() )
    kyc_approved = Int(1)

    return Seq([

        Assert( Global.group_size() == Int(2)                                     ),
        Assert( is_kyc_account == Int(1)                                          ),
        Assert( Gtxn[0].application_args.length() == Int(0)                       ),

        Assert( Gtxn[1].application_args.length() == Int(0)                       ),

        App.localPut( Gtxn[1].sender(), Bytes("kyc_approved"), kyc_approved       ),
        Return()
    ])



@Subroutine(TealType.none)
def handle_updateapp_function():

    is_creator_var = is_creator( Txn.sender() )

    return Seq([

        Assert( is_creator_var == Int(1) ),
        Return()
    ])



@Subroutine(TealType.none)
def handle_deposit_function():

    is_creator_var = Int(1)

    return Seq([

        App.globalPut( Bytes("kyc_account"), Txn.sender() ),
        Assert( is_creator_var == Int(1) ),
        Return()
    ])
    






    







