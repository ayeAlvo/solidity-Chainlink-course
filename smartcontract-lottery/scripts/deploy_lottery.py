from brownie import Lottery, config, network
from scripts.helpful_scripts import get_account, get_contract, fund_with_link
import time
def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
         config["networks"][network.show_active()]["keyhash"],
         {"from": account},
         publish_source=config["networks"][network.show_active()].get("verify", False)
    )
    print("Lottery Deployed!")
    return lottery

def start_lottery():
    account=get_account()
    lottery=Lottery[-1]
    starting_txn = lottery.startLottery({"from": account})
    starting_txn.wait(1)
    print("Lottery Started!")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    enter_txn = lottery.enter({"from": account, "value": value})
    enter_txn.wait(1)
    print("You have entered the lottery!")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # lottery.endLottery({"from": account})
    txn = fund_with_link(lottery.address)
    txn.wait(1)
    ending_txn = lottery.endLottery({"from": account})
    ending_txn.wait(1)
    # time.sleep(60)
    print(f"{lottery.recentWinner()} is the new Winner!")
    print("Lottery Ended!")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()