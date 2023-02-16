import pytest
from app.calculations import add, BankAccount, InsufficientFunds


# 'fixture' is a function that runs before test function.
# here we are defining 'fixture' function to initialize a BankAccount() instance
@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


# naming matters for testing. because 'test_*' naming will allow Pytest to locate them automatically.
# we have to do according naming to testing functions as well as .py files.

@pytest.mark.parametrize("x, y, expected", [  # here we are setting multiple test cases.
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(x, y, expected):
    print("testing add function")
    assert add(x, y) == expected


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(30)
    assert bank_account.balance == 20


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55


@pytest.mark.parametrize("deposited, withdraw, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (189, 150, 39)
])
def test_bank_transaction(zero_bank_account, deposited, withdraw, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):  # expecting Exception as output
        bank_account.withdraw(200)
