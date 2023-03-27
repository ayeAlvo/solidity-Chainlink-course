from brownie import accounts, config, SimpleStorage, network
# import os

def deploy_simple_storage():
    # distintas formas para agregar cuentas:
    # para ver la cuenta en el indice 0 de ganache
    # account = accounts[0]
    # para acceder a la cuenta de metamask agregada por CLI LA MAS SEGURA
    # account = accounts.load("metamask-course-account")
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # desde el archivo de configuracion
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(42, {"from": account})
    transaction.wait(1)
    update_storage_value = simple_storage.retrieve()
    print(update_storage_value)

def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def main():
    deploy_simple_storage()