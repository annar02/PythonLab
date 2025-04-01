#Задание 1. Вариант 10.
import os

def find_optimal_location(filename):
    try:
        with open(filename, 'r') as file:
            N = int(file.readline())
            capacities = [int(file.readline()) for _ in range(N)]
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

    total = sum(capacities)
    min_cost = float('inf')
    best_pos = 0
    current_cost = 0

    for j in range(N):
        distance = min(j, N - j)
        current_cost += capacities[j] * distance

    min_cost = current_cost
    best_pos = 1

    for i in range(1, N):
        current_cost = current_cost + total - N * capacities[i - 1]
        if current_cost < min_cost:
            min_cost = current_cost
            best_pos = i + 1

    return best_pos

file_a = "D:\\Python LR\\Lab1\\PythonLab\\Lab4\\27-99a.txt" 
file_b = "D:\\Python LR\\Lab1\\PythonLab\\Lab4\\27-99b.txt"

print("Обработка файла A...")
result_a = find_optimal_location(file_a)

print("Обработка файла B...")
result_b = find_optimal_location(file_b)

if result_a is not None and result_b is not None:
    print("Результат:", result_a, result_b)
else:
    print("Ошибка при обработке файлов.")