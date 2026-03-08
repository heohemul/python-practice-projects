# Факторіал числа N

N = int(input("Введіть число N: "))

fact = 1
for i in range(1, N + 1):
    fact *= i

print("Факторіал числа", N, "дорівнює:", fact)