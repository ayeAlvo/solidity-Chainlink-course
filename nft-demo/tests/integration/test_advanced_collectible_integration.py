from brownie import network, AdvancedCollectible
import time
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    # get_contract,
    get_account,
    fund_with_link
)
# from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible_integration():
    # deploy the contract
    # create an NFT
    # get a random breed back
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    # Act
    # advanced_collectible, creation_transaction = deploy_and_create()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address)
    creating_txn = advanced_collectible.createCollectible({"from": get_account()})
    creating_txn.wait(1)
    time.sleep(60)
    # Assert
    print(advanced_collectible.tokenCounter())
    assert advanced_collectible.tokenCounter() > 1