from typing import ByteString
from eth_utils.conversions import to_hex
from eth_utils.currency import from_wei
from web3 import Web3
import json
import requests
from decimal import *


ganache_url = "https://mainnet.infura.io/v3/e54a286f7ec04607b570c19c804dc6a8"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# infura_url= "https://mainnet.infura.io/v3/8a422fe86e44c0ab9fdc4aea947b15b6"
# web3 = Web3(Web3.HTTPProvider(infura_url))


# check connecting web3 to Ganache
# print(web3.is_connected())
if  web3.is_connected() == True:
    print("started")
else :
    print("error connecting...")

# get gas price
# try :
#     gas_url= "https://www.gasnow.org/api/v3/gas/price"
#     r = requests.get(gas_url)
#     r = r.json()
#     r = r['data']
#     r = r['fast']
#     r = web3.fromWei(r, "Gwei")
# except:
#     print("error gas")

#accounts value and private key
print("Done gas")
account_1 = "0xe18CeB3369558A4c6334d99C788A09381E9bFCf4"
account_2 = "0x9371185B2C055cB46C23bEcCf93e0894765e9398"
private_key = "91ec42ba989500ecf32e6ad8066af193b266dc776a23500131dfb91f1c1270b2"

balance=0
gas_fee = 21000*56  # You can change gasfee value
gas_fee = Decimal(gas_fee)
gas_fee = web3.from_wei(gas_fee,'Gwei')
print("get balance...","gas fee is : ", gas_fee)
def get_balance_loop():
    balance=0
    while True:
        while 0.0005>balance:
            # Get balance account
            try:
                balance = web3.eth.get_balance(account_1)
                balance = web3.from_wei(balance, "ether") #convert to ether value
                # print(balance)
            #     exit
            except Exception as Ex:
                print(Ex)
                print("error , i can't get balance...")
                exit()

        try:
            balance = balance-gas_fee
            print(balance)
            # print(balance)
            # print(web3.fromWei(balance, "ether"))
            build_transaction(balance)
        except:
            print("Error, check balance and Gasfee again")
            exit()
            


def build_transaction(balance):
    try:
        #get nonce number
        nonce = web3.eth.get_transaction_count(account_1)
        #build transaction
        tx = {
            'nonce':nonce,
            'to':account_2,
            'value':web3.to_wei(balance,'ether'),
            'gas':21000,
            'gasPrice':web3.to_wei('56','gwei')
        }

        #sign transaction with private key
        signed_tx = web3.eth.account.sign_transaction(tx,private_key)
        #send Transaction
        tx_hash= web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        print(web3.to_hex(tx_hash))
        print("Transaction Completed\n GET Balance Again...")
        get_balance_loop()
    except:
        print("ERROR, check buldTransction Funcation")
        exit()

get_balance_loop()
