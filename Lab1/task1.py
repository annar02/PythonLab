#Задание 1. Составить 3 функции для работы с цифрами или делителями числа
""""Вариант 8. 
Функция 1. Найти количество чисел, взаимно простых с заданным. 
Функция 2. Найти сумму цифр числа, делящихся на 3. 
Функция 3. Найти делитель числа, являющийся взаимно простым с 
суммой цифр данного числа."""
import math

def count_simple(n):
    if n <= 0:
        return 0
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n = n // p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def sum_digits(n):
    return sum(int(digit) for digit in str(n) if int(digit) % 3 == 0)

# Функция 3: Делитель числа, взаимно простой с суммой цифр
def divisor(n):
    digit_sum = sum(int(digit) for digit in str(n))
    for divisor in range(1, n + 1):
        if n % divisor == 0 and math.gcd(divisor, digit_sum) == 1:
            return divisor
    return None 

if __name__ == "__main__":
    # Функция 1
    print("Количество взаимно простых чисел:", count_simple(10))

    # Функция 2
    print("Сумма цифр числа, делящихся на 3:", sum_digits(136))

    # Функция 3
    print("Делитель числа, взаимно простой с суммой цифр:", divisor(15))