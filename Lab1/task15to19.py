#Задания 15-19. Решить задачи по вариантам.
"""Вариант 8. Задачи 8, 20, 32, 44, 56 
8. Дан целочисленный массив. Необходимо найти индексы двух 
наименьших элементов массива. 
20. Дан целочисленный массив. Необходимо найти все пропущенные 
числа.  
32. Дан целочисленный массив. Найти количество его локальных 
максимумов. 
44. Дан массив чисел. Необходимо проверить, чередуются ли в нем 
целые и вещественные числа.
56. Для введенного списка посчитать среднее арифметическое 
непростых элементов, которые больше, чем среднее арифметическое простых."""

def find_smallest_indices(arr):
    if len(arr) < 2:
        return []

    sorted_with_indices = sorted(enumerate(arr), key=lambda x: x[1])
    return sorted_with_indices[0][0], sorted_with_indices[1][0]

def find_missing_numbers(arr):
    if not arr:
        return []
    
    min_val = min(arr)
    max_val = max(arr)
    full_set = set(range(min_val, max_val + 1))
    arr_set = set(arr)
    return sorted(list(full_set - arr_set))

def count_max(arr):
    if len(arr) < 3:
        return 0
    
    count = 0
    for i in range(1, len(arr) - 1):
        if arr[i] > arr[i - 1] and arr[i] > arr[i + 1]:
            count += 1
    return count

def is_alternating(arr):
    if len(arr) < 2:
        return True
    
    for i in range(1, len(arr)):
        prev_is_int = isinstance(arr[i - 1], int)
        current_is_int = isinstance(arr[i], int)
        if prev_is_int == current_is_int:
            return False
    return True

def avg_nonprimes(arr):
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    primes = [x for x in arr if isinstance(x, int) and is_prime(x)]
    if not primes:
        return 0
    
    primes_mean = sum(primes) / len(primes)
    
    non_primes = [x for x in arr if not (isinstance(x, int) and is_prime(x)) and x > primes_mean]
    if not non_primes:
        return 0
    
    return sum(non_primes) / len(non_primes)

def main():
    print("Выберите какую задачу хотите решить:")
    print("1. Найти индексы двух наименьших элементов массива")
    print("2. Найти все пропущенные числа в массиве")
    print("3. Найти количество локальных максимумов в массиве")
    print("4. Проверить чередование целых и вещественных чисел")
    print("5. Среднее непростых элементов, больших среднего простых")
    
    choice = input("Введите номер задачи (1-5): ")

    if choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5':
        print("Выберите номер задачи от 1 до 5")
        return

    input_str = input("Введите числа через пробел: ")
    elements = input_str.split()
    
    arr = []
    for elem in elements:
        try:
            num = int(elem)
        except ValueError:
            try:
                num = float(elem)
            except ValueError:
                print(f"Ошибка: '{elem}' не является числом")
                return
        arr.append(num)
    
    if not arr:
        print("Ошибка: массив не может быть пустым")
        return
    
    if choice == '1':
        result = find_smallest_indices(arr)
        print(f"Индексы двух наименьших элементов: {result}")
    elif choice == '2':
        result = find_missing_numbers(arr)
        if len(result) == 0:
            print("Нет пропущенных чисел")
        else:
            print(f"Пропущенные числа: {result}")
    elif choice == '3':
        result = count_max(arr)
        if result == 0:
            print("В массиве нет локальных максимумов")
        else:
            print(f"Количество локальных максимумов: {result}")
    elif choice == '4':
        result = is_alternating(arr)
        print(f"Чередуются ли целые и вещественные числа: {'да' if result else 'нет'}")
    elif choice == '5':
        result = avg_nonprimes(arr)
        print(f"Среднее арифметическое: {result}")

if __name__ == "__main__":
    main()