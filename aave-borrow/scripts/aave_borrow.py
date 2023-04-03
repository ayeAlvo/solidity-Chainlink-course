from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import interface, config, network
from web3 import Web3

# 0.1
AMOUNT = Web3.toWei(0.1, "ether")

def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        get_weth()

    lending_pool = get_lending_pool()
    # Aprobar transferencia
    approve_erc20(AMOUNT, lending_pool.address, erc20_address, account )

    print("Depositing...")
    tx = lending_pool.deposit(erc20_address, AMOUNT, account.address, 0, {"from": account})
    tx.wait(1)
    print("Deposited!")
    get_borrowable_data(lending_pool, account)

    # Account status
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    # DAI en terminos de ETH
    dai_eth_price = get_asset_price(config["networks"][network.show_active()]["dai_eth_price_feed"])
    # borrowable_eth -> borrowable_dai * 95%\
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")

    dai_token = config["networks"][network.show_active()]["dai_token"]
    borrow_txn = lending_pool.borrow(dai_token, Web3.toWei(amount_dai_to_borrow, "ether"), 1, 0, account.address, {"from": account})
    borrow_txn.wait(1)
    print("We borrowed some DAI!")
    get_borrowable_data(lending_pool, account)

    # Repay all
    repay_all(Web3.toWei(amount_dai_to_borrow, "ether"), lending_pool, account)
    get_borrowable_data(lending_pool, account)
    print("You just deposited, borrowed, and repayed with Aave, Brownie, and Chainlink!")

def get_lending_pool():
    # ABI
    # Address
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(config["networks"][network.show_active()]["lending_pool_addresses_provider"])
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account} )
    print("Approved ERC20!")
    return tx

 # ...how much?
def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth, # Garantía
        total_debt_eth, # Total prestado
        available_borrow_eth, # Total que se nos permite pedir prestado
        current_liquidation_threshold, # Nuestro umbral de liquidación
        ltv,
        health_factor, # Indice de salud
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    return (float(available_borrow_eth), float(total_debt_eth))

def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The DAI/ETH price is {converted_latest_price}")
    return float(converted_latest_price)

def repay_all(amount, lending_pool, account):
    # Approve payback
    dai_token = config["networks"][network.show_active()]["dai_token"]
    approve_erc20(Web3.toWei(amount, "ether"), lending_pool, dai_token, account)
    repay_txn = lending_pool.repay(dai_token, amount, 1, account.address, {"from": account})
    repay_txn.wait(1)
    print("Repaid!")