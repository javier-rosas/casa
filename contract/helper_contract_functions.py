
from pyteal import * 

# Checks if the transaction sender is the creator of the application
@Subroutine(TealType.bytes)
def is_creator(address: TealType.bytes):

    is_creator = address == App.globalGet(Bytes("Creator"))

    return is_creator


# App local put simplified (bytes)
@Subroutine(TealType.none)
def local_put_bytes(address: TealType.bytes, key, value):

    Seq([
        App.localPut(address, Bytes(key), Bytes(value)),
        Return()
    ])

# App local put simplified (uints)
@Subroutine(TealType.none)
def local_put_bytes(address: TealType.bytes, key, value: TealType.uint64):

    Seq([
        App.localPut(address, Bytes(key), Int(value)),
        Return()
    ])


    







