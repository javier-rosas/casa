
from pyteal import * 

# Checks if the transaction sender is the creator of the application
@Subroutine(TealType.bytes)
def is_creator(address: TealType.bytes):

    is_creator = address == App.globalGet(Bytes("Creator"))

    Return(is_creator)


# App local put simplified
@Subroutine(TealType.none)
def local_put(address: TealType.bytes, key, value):

    Seq([
        App.localPut(address, Bytes(key), Bytes(value)),
        Return()
    ])
    







