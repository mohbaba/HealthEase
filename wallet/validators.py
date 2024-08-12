def validate_amount(amount):
    if amount < 0:
        return True
    return False


def validate_balance(balance, amount):
    if balance < amount:
        return True
    return False
