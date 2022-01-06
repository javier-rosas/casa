
from pyteal import * 



# Checks if the transaction sender is the creator (kyc_account) of the application
@Subroutine(TealType.uint64)
def is_creator(address: TealType.bytes):

    is_creator = address == App.globalGet( Bytes("creator_address") )

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

    is_sender_creator_account = is_creator( Txn.sender() )

    return Seq([

        Assert( is_sender_creator_account == Int(1)   ),
        Assert( Global.group_size() == Int(1)         ),
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
def put_pool_args():
    """
    put_pool_args: 

        - stores pool variables in global & local storage

        - Returns: None
    """


    '''
    kyc_address in global storage
    '''
    kyc_address_bytes = Bytes("kyc_address")
    kyc_address = Addr("XRH2VHWTWNOXNYJ3WMBE467KJXYS3E4GVKCYSVD2UM4KIIWXFHJPB6SDAM")

    '''
    creator_address in global storage
    '''
    creator_address_bytes = Bytes("creator_address")
    creator_address = Addr("XQKVERLU6YCTVDIBKOILU7L6ERZPJCYONRVPLRG2II4PNX74CNC7XGBE24")

    '''
    lender_usdc_pool_address in global storage 
        goal in local storage
        curr_amount in local storage 
        local_rate in local storage 

    '''
    lender_usdc_pool_address_bytes = Bytes("lender_usdc_pool_address")
    lender_usdc_pool_address = Addr("7IUEUCQAOPLWGRYPKB6X4VVUCHEG5KCGSB37BP4AFAI6NKODQFPXRLT7EU")

    goal_key = Bytes("goal") 
    goal_value = Int(0) 

    curr_amount_key = Bytes("curr_amount")
    curr_amount_value = Int(0)

    local_rate_key = Bytes("local_rate")
    local_rate_value = Int(0)

    '''
    payback_pool_address in global storage
    '''
    payback_pool_address_bytes = Bytes("payback_pool_address")
    payback_pool_address = Addr("W2CLHER4FQJUURUWSTCMYMER34GE7AX57H4SZ6C55YXJ3AGPMALT3W5ATI")

    in_key = Bytes("in")
    in_value = Int(0)

    in_to_drop_key = Bytes("in_to_drop")
    in_to_drop_value = Int(0)

    out_key = Bytes("out")
    out_value = Int(0)
 
    '''
    token_reserve_pool_address in global storage
    '''
    token_reserve_pool_address_bytes = Bytes("token_reserve_pool_address")
    token_reserve_pool_address = Addr("NKJC2Y2SVO7MP5RD2H36RGQFRXXAI6YLUXV6I6X3T6653I753PB6XLNSVE")

    '''
    token_active_pool_address in global storage
    '''
    token_active_pool_address_bytes = Bytes("token_active_pool_address")
    token_active_pool_address = Addr("PAUO4UB7HEKTVGKMY7E2DS7PDOZTOESLTEH5C2OIXVYNSLF5JB245U3C24")

    '''
    token_stake_pool_address in global storage
    '''
    token_stake_pool_address_bytes = Bytes("token_stake_pool_address")
    token_stake_pool_address = Addr("XEIYOL33Q6FRPZLIXX2C4YOEN64NSGN5EDGNUOQNUBWZEMG4ZOBGHM7JHI")




    '''
    total_index_tokens_sent in global storage
    '''
    total_index_tokens_sent_key = Bytes("total_index_tokens_sent")
    total_index_tokens_sent_value = Int(0)



    '''
    global_current_amount in global storage
    '''
    global_current_amount_key = Bytes("global_current_amount")
    global_current_amount_value = Int(0)


    '''
    current_loans_funded in global storage
    '''
    current_loans_funded_key = Bytes("current_loans_funded")
    current_loans_funded_value = Int(0)


    '''
    index_token_id in global storage
    '''

    index_token_id_key = Bytes("index_token_id")
    index_token_id_value = Int(56862605)



    '''
    usdc_id in global storage 
    '''
    usdc_id_key = Bytes("usdc_id")
    usdc_id_value = Int(10458941)





    return Seq([

        # ------- kyc_address  -------

        App.globalPut( kyc_address_bytes, kyc_address ),



        # ------- creator_address  -------

        App.globalPut( creator_address_bytes, creator_address ),



        # ------- total_index_tokens_sent  -------

        App.globalPut( total_index_tokens_sent_key, total_index_tokens_sent_value ),



        # ------- global_current_amount  -------

        App.globalPut( global_current_amount_key, global_current_amount_value ),



        # ------- current_loans_funded  -------

        App.globalPut( current_loans_funded_key, current_loans_funded_value ),



        # ------- index_token_id  -------

        App.globalPut( index_token_id_key, index_token_id_value ),



        # ------- usdc_id  -------

        App.globalPut( usdc_id_key, usdc_id_value ),



        # ------- lender_usdc_pool_address  -------

        App.globalPut( lender_usdc_pool_address_bytes, lender_usdc_pool_address ),

        App.localPut( lender_usdc_pool_address, goal_key , goal_value ),

        App.localPut( lender_usdc_pool_address, curr_amount_key , curr_amount_value ),

        App.localPut( lender_usdc_pool_address, local_rate_key , local_rate_value ),



        # ------- payback_pool_address -------

        App.globalPut( payback_pool_address_bytes, payback_pool_address ),

        App.localPut( payback_pool_address, in_key , in_value ),

        App.localPut( payback_pool_address, in_to_drop_key , in_to_drop_value ),

        App.localPut( payback_pool_address, out_key , out_value ),



        # ------- token_reserve_pool_address -------

        App.globalPut( token_reserve_pool_address_bytes, token_reserve_pool_address ),



        # ------- token_active_pool_address -------

        App.globalPut( token_active_pool_address_bytes, token_active_pool_address ),



        # ------- token_stake_pool_address -------

        App.globalPut( token_stake_pool_address_bytes, token_stake_pool_address ),





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
        #Assert( is_sender_kyc_account == Int(1) ),
        Assert( Global.group_size() == Int(1)   ),
        put_pool_args(),

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

    







