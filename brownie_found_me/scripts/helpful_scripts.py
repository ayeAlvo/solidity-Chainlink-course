from brownie import MockV3Aggregator, network, config, accounts
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = Web3.toWei(2000, "ether")

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

def get_account():
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS 
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    
def deploy_mocks():
     #price feed falso, a traves de
        print(f"The active network is {network.show_active()}")
        print(f"Deploying the mocks!")
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
        print(f"Mocks Deployed")