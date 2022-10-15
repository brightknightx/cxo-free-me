#import dependencies
import os
import traceback
from argparse import ArgumentParser

import web3 as web3
from eth_account import Account
from web3 import Web3
from web3.middleware import geth_poa_middleware

# Const configuration
RPC_URL="https://polygon-rpc.com"
CXO_CONTRACT_ADDRESS='0xe957a692C97566EfC85f995162Fa404091232B2E'
CXO_RELAY_ABI = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"uint256","name":"nonce","type":"uint256"},{"indexed":true,"internalType":"bytes32","name":"encodedFunctionHash","type":"bytes32"}],"name":"TransactionRelayed","type":"event"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"bytes","name":"encodedFunction","type":"bytes"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"uint256","name":"reward","type":"uint256"},{"internalType":"address","name":"rewardRecipient","type":"address"},{"internalType":"bytes","name":"rewardSignature","type":"bytes"}],"name":"relayCall","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

# global vars
w3 = None
private_key = None
relayer_contract = None
my_matic_address = None


def setup():
    # instantiate a web3 remote provider
    global w3
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    # make sure this is called before all other middleware_onion calls
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # start a contract instance
    global relayer_contract
    relayer_contract = w3.eth.contract(address=CXO_CONTRACT_ADDRESS, abi=CXO_RELAY_ABI)

    # parse input
    parser = ArgumentParser()
    parser.add_argument("-p", "--private-key", dest="private_key",
                        help="Private key", metavar="12345678")
    parser.add_argument("-g", "--gas-price", dest="gas_price",
                        help="Private key", metavar="500")

    args = vars(parser.parse_args())

    global private_key
    global gas_price
    private_key = args['private_key']
    gas_price = args['gas_price']
    
    if private_key is None:
        print('Private key not specified!')
        parser.print_help()
        exit(1)

    if gas_price is None:
        print('Gas price not specified! Using 500 as default')
        gas_price = 500

    # get the address from pk
    global my_matic_address
    private_account = Account.from_key(private_key)
    my_matic_address = private_account.address

    # set as default
    web3.eth.defaultAccount = my_matic_address

def prep_transaction(nonce):
    return relayer_contract.functions.relayCall('0x000000000000000000000000000000000000dEaD',
            '0x000000000000000000000000000000000000dEaD',
            "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            0,
            "0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            Web3.toInt(text="0"),
            '0x000000000000000000000000000000000000dEaD',
            "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000").buildTransaction(
        {
            'chainId': 137,
            'gas': 2100000,
            'gasPrice': w3.toWei("500", 'gwei'),
            'nonce': nonce
        }
    )

def boost_transaction(tx_boost, private_key):
    signedTxn = w3.eth.account.sign_transaction(tx_boost, private_key)
    
    hash = w3.eth.sendRawTransaction(signedTxn.rawTransaction)
    
    print(f'Boost sent with hash: {hash.hex()}')
    
def free_my_doc(private_key=private_key):
    print(f'Boosting {my_matic_address}')

    try:
        nonce = w3.eth.getTransactionCount(my_matic_address)
        print(f"Actual nonce to boost: {nonce}")

        # load tx_ids to be boosted
        tx_boost = prep_transaction(nonce=nonce)

        # send the transaction
        boost_transaction(tx_boost=tx_boost, private_key=private_key)
    except:
        print(traceback.format_exc())

    print(f"1 transactions were boosted")


if __name__ == "__main__":
    # prepare
    setup()

    # boost the gas
    free_my_doc(private_key=private_key)
