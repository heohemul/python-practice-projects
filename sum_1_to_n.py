# Сума чисел від 1 до N

N = int(input("Введіть число N: "))

suma = 0
for i in range(1, N + 1):
    suma += i

print("Сума чисел від 1 до", N, "дорівнює:", suma)