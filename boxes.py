
from algosdk import *
from pyteal import *
from beaker import *
from beaker.lib.storage import Mapping
from algosdk.account import generate_account
from algosdk.encoding import decode_address
from algosdk.atomic_transaction_composer import AccountTransactionSigner

names = ["Camilo", "Laura", "Daniel", "Pilar", "Jairo"] 

class UserSave(Application):

    users = Mapping(abi.Address, abi.String)

    @external
    def add_member(self, name: abi.String):
        return Seq(
            self.users[Txn.sender()].set(name.get()),
            App.box_put(Txn.sender(), name.get())  
            )

if __name__ == "__main__":
    creator = sandbox.get_accounts()[0]
    app_client = client.ApplicationClient(
        sandbox.get_algod_client(), 
        UserSave(), 
        signer=creator.signer
    )

    app_client.create()
    #app_client.fund(100 * consts.algo) """
    print("APP ID")
    print(app_client.app_id)

    addrs = []
    for _ in range(5):
        [sk, addr] = generate_account()
        addrs.append(addr)
        signer = AccountTransactionSigner(sk)

        app_client.fund(101_000, addr)
        # Fund contract with box MBR
        app_client.fund(118500)

        result = app_client.call(
            UserSave.add_member,
            name= names[_],
            signer=signer,
            boxes=[[app_client.app_id, encoding.decode_address(addr)]],
        )


    for box in app_client.get_box_names():
            print(f"{box}: {app_client.get_box_contents(box)}")

    UserSave().dump('./artifacts')

