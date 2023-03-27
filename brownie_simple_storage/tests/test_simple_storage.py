from brownie import SimpleStorage, accounts

def test_deply():
    # Arrange -> organizar o arreglar
    account = accounts[0]
    # Act -> ejecutar una funcion, hacer algo
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    # Assert -> comprobar que algo ha ido bien
    assert starting_value == expected
    # Assert -> comprobar que algo ha ido bien

def test_updating_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act
    txn = simple_storage.store(42, {"from": account})
    txn.wait(1)
    expected = 42
    print(expected) # usar -s para ver los print
    # Assert
    assert simple_storage.retrieve() == expected

# --pbd si falla abre una consola de python para ejecutar lo que se estaba ejecutando