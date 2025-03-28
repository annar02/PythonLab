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

def main():
    print("Выберите какую задачу хотите решить:")
    print("1. Найти индексы двух наименьших элементов массива")
    print("2. Найти все пропущенные числа в массиве")
    print("3. Найти количество локальных максимумов в массиве")
    print("4. Проверить чередование целых и вещественных чисел")
    print("5. Среднее непростых элементов, больших среднего простых")
    
    choice = input("Введите номер задачи (1-5): ")
    
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

if __name__ == "__main__":
    main()