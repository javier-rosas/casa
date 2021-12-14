from pyteal import * 

@Subroutine(TealType.none)
def lender_cash_out_func():

    amount_to_deposit = Gtxn[1].amount()
    new_amount = current_amount_deposited + amount_to_deposit

    return Seq([

        Assert( Global.group_size() == Int(2)                              ),
        Assert( Gtxn[0].type_enum() == TxnType.ApplicationCall             ),
        Assert( Gtxn[0].application_args.length() == Int(1)                ),
        Assert( Gtxn[1].type_enum() == TxnType.Payment                     ),
        Assert( Gtxn[1].close_remainder_to() == Global.zero_address()      ),
        Assert( Gtxn[1].rekey_to() == Global.zero_address()                ),

        Assert(  Global.current_application_address() == Gtxn[1].receiver() ),
        App.localPut(  Gtxn[1].sender(), Bytes("user_deposited"), new_amount       ),
        Return()
    ])   


