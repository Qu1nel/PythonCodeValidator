"""Program with magic numbers."""

PRICE = 100

def calculate_tax(amount):
    # 0.2 - это магическое число
    tax = amount * 0.2 
    return tax

def get_status_code():
    # 200 - это магическое число
    return 200