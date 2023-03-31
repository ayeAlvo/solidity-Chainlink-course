from brownie import network, accounts, config, Contract, MockV3Aggregator, VRFCoordinatorMock, LinkToken, interface

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}

def get_account(id=None, index=None):
    if id:
        return accounts.load(id)
    if index:
        return accounts[index]
    if(
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

def get_contract(contract_name):
    """
      Toma el addres de contrato desde brownie-config, si esta definido. En caso contrato
      despliega Mocks de ese contrato

      Args:
        contract_name (string):
      Returns:
        brownie.network.contract.ProjectContract -> Implementación más reciente de este contrato
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            # MockV3Aggregator.length
            deploy_mocks()
        contract = contract_type[-1]
        # MockV3Aggregator[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # MockV3Aggregator.abi
    return contract

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    #  a traves de la ABI
    tx = link_token.transfer(contract_address, amount, {"from": account})
    #  a traves de la interface
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Contract funded!")
    return tx

# DECIMALS: 8
# STARTING_PRICE = 200000000000
# no las estoy usando, las hardcodie, no me las lee. Ver

def deploy_mocks():
    account = get_account()
    MockV3Aggregator.deploy(8, 200000000000, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address,{"from": account})
    print("Mocks deployed")
