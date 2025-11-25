price = float(input("цена"))
discount = float(input("скидка"))
vat = float(input("налог"))
base = price * (1 - discount / 100)
vat_amount = base * (vat / 100)
total = base + vat_amount
print(f"База после скидки:{base:.2f}")
print(f"НДС:{vat_amount:.2f}")
print(f"И того с оплате:{total:.2f}")
