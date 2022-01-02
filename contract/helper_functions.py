
from pyteal import * 



# Checks if the transaction sender is the creator (kyc_account) of the application
@Subroutine(TealType.uint64)
def is_creator(address: TealType.bytes):

    is_creator = address == App.globalGet( Bytes("kyc_account") )

    return is_creator







@Subroutine(TealType.none)
def optin_func():

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
def updateapp_func():

    is_sender_kyc_account = is_creator( Txn.sender() )

    return Seq([

        Assert( is_sender_kyc_account == Int(1) ),
        Assert( Global.group_size() == Int(1)   ),
        Return()
    ])



@Subroutine(TealType.none)
def deposit_usdc_func(pool_address: TealType.bytes, amount: TealType.uint64):

    is_creator_var = Int(1)

    return Seq([
        Assert(is_creator_var == Int(1)),

        Return()
    ])



# add pool function. 
# The sender must be the creator (kyc account)
# Adds the pool to global storage
# Returns nothing
@Subroutine(TealType.none)
def add_pool_func(pool_name: TealType.bytes, address: TealType.bytes, ):

    is_sender_kyc_account = is_creator( Txn.sender() )

    return Seq([

        Assert( is_sender_kyc_account == Int(1) ),
        Assert( Global.group_size() == Int(1)   ),
        App.globalPut( pool_name, address       ),
        Return()
    ])
    




# 
@Subroutine(TealType.uint64)
def timelock_func():

    #one_day = Int(86400)
    one_day = Int(10)
    latest_timestamp = Global.latest_timestamp()
    latest_timestamp_plus_a_day = Global.latest_timestamp() + one_day
    get_user_timestamp = App.localGet(Txn.sender(), Bytes("user_timestamp"))
    put_user_timestamp = App.localPut(Txn.sender(), Bytes("user_timestamp"), latest_timestamp_plus_a_day)

    return Seq([
            
            If(get_user_timestamp == Int(0))

                .Then(

                    Seq([
                        put_user_timestamp,
                        Return( Int(0) ) 
                    ]))

            .ElseIf( get_user_timestamp != Int(0) )

                .Then(

                    If( get_user_timestamp - one_day > latest_timestamp )

                        .Then(

                            Seq([
                                Log( Bytes("need to wait") ),
                                Return( Int(0) )
                            ])
                        )

                    .Else(

                        If( get_user_timestamp - one_day <= latest_timestamp )

                            .Then(

                                Seq([
                                    Log( Bytes("good to go!") ),
                                    put_user_timestamp,
                                    Return( Int(1) )
                                ])
                            )
                    )
                ),

                Return( Int(0) )
                    
                
    ])

    







