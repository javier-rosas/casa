
from pyteal import * 



# Checks if the transaction sender is the creator (kyc_account) of the application
@Subroutine(TealType.uint64)
def is_creator(address: TealType.bytes):

    is_creator = address == App.globalGet( Bytes("kyc_account") )

    return is_creator







@Subroutine(TealType.none)
def optin_func():
    """
    opt in function:

        - checks that opt in is happening in a grouped transaction of size 2
            - Gtxn[0] is the txn made by the KYC account (after user has passed the KYC process)
            - Gtxn[1] is the user txn 
        - does safety checks 
        - puts bytes 'kyc_approved' = 1 in user's local storage if function succeeds 

        - Returns: None
    """

    is_kyc_account = is_creator( Gtxn[0].sender() )
    

    return Seq([

        Assert( Global.group_size() == Int(2)                                     ),
        Assert( is_kyc_account == Int(1)                                          ),

        Assert( Gtxn[0].application_args.length() == Int(0)                       ),
        Assert( Gtxn[0].applications.length() == Int(0)                             ),
        Assert( Gtxn[0].accounts.length() == Int(0)                             ),

        
        Assert( Gtxn[1].application_args.length() == Int(0)                       ),
        Assert( Gtxn[1].applications.length() == Int(0)                             ),
        Assert( Gtxn[1].accounts.length() == Int(0)                             ),


        App.localPut( Gtxn[1].sender(), Bytes("kyc_approved"), Int(1)             ),

        Return()

    ])





@Subroutine(TealType.none)
def updateapp_func():
    """
    update_app function:

        - asserts the account making the update txn is the manager account 
        - does safety checks 

        - Returns: None
    """

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



@Subroutine(TealType.none)
def loop_over_app_args():

    app_args_length = Txn.application_args.length()
    pool_name = Txn.application_args[1]
    pool_address = Txn.application_args[2]

    i = ScratchVar(TealType.uint64)

    return Seq([


        App.globalPut( pool_name, pool_address ),

        
        i.store(Int(3)),
        While(i.load() < ( app_args_length - Int(1) ) ).Do(Seq([
            #Log(pool_address),
            App.localPut(pool_address, Txn.application_args[i.load()], Txn.application_args[i.load() + Int(1) ]),
        
            If( Mod(i.load(), Int(2) ) == Int(0) )
                .Then(
                    
                    Seq([i.store(i.load() + Int(1)),

                    ])
            )
            .Else(
                
                Seq([i.store(i.load() + Int(2)),
                
                ])
            )
            
            

        ])),
    

        # 

        Return()
    ])


@Subroutine(TealType.none)
def add_pool_func():
    """
    add_pool_func: 

        - checks the sender of the txn is the manager account 
        - adds pool to global storage 
        
        - Returns: None
    """

    is_sender_kyc_account = is_creator( Txn.sender() )

    return Seq([
        Assert( is_sender_kyc_account == Int(1) ),
        Assert( Global.group_size() == Int(1)   ),
        loop_over_app_args(),

        Return()
    ])
    





@Subroutine(TealType.uint64)
def timelock_func():
    """
    timelock_func: 
        
        - user (lender) can only redeem from the payback pool every 24 hours 

        Pseudocode: 

            # user does not have a timestamp in local storage, so return 0
            if get_user_timestamp == 0: 
                put latest_timestamp + one day in local storage 
                return 0

            elif get_user_timestamp != 0:
                # user has NOT waited 24 hours since last txn to stake pool, so return 0
                if get_user_timestamp - one_day > latest_timestamp:
                    return 0
                # user has waited 24 hours since last txn to stake pool, so return 1
                elif get_user_timestamp - one_day <= latest_timestamp:
                    return 1

    """


    #one_day = Int(86400)
    one_day = Int(10) # actually just 10 seconds (for testing purposes)
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

    







