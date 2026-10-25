from decimal import Decimal, getcontext

getcontext().prec = 50  # Define a precisão para 50 dígitos
resultado = Decimal(12345678910111213141516) / Decimal(2)
print(resultado)

