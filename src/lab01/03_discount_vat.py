price=float(input('цена'))
discount=float(input('скидка'))
vat=float(input(''))
base = price * (1 - discount/100)//0.01/100
vat_amount = (base * (vat/100))//0.01/100
total = (base + vat_amount)//0.01/100
print(f'База после скидки:{base}')
print(f'НДС:{vat_amount}')
print(f'И того с оплате:{total}')