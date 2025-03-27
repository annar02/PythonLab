#Задания 2-4. Решить задачи по вариантам.
"""Вариант 8. Задачи 2, 10, 17
2. Дана строка, состоящая из символов латиницы. Необходимо 
проверить, упорядочены ли строчные символы этой строки по возрастанию. 
10. Дана строка. Необходимо подсчитать количество букв "А" в этой 
строке. 
17. Дана строка в которой записан путь к файлу. Необходимо найти имя 
файла без расширения."""
def check_lowercase(s):
    lowercase_chars = [c for c in s if c.islower()]
    return lowercase_chars == sorted(lowercase_chars)

def count_a(s):
    return s.upper().count('A')

def get_filename(path):
    import os
    filename = os.path.basename(path)
    return os.path.splitext(filename)[0]

def main():
    print("Выберите задачу для решения:")
    print("1. Проверить, упорядочены ли строчные символы строки по возрастанию")
    print("2. Подсчитать количество букв 'А' в строке")
    print("3. Найти имя файла без расширения в пути")
    choice = input("Введите номер задачи (1-3): ")
    
    if choice == '1':
        s = input("Введите строку: ")
        if check_lowercase(s):
            print("Строчные символы упорядочены по возрастанию")
        else:
            print("Строчные символы НЕ упорядочены по возрастанию")
    elif choice == '2':
        s = input("Введите строку: ")
        count = count_a(s)
        print(f"Количество букв 'А' в строке: {count}")
    elif choice == '3':
        path = input("Введите путь к файлу: ")
        filename = get_filename(path)
        print(f"Имя файла без расширения: {filename}")
    else:
        print("Некорректный выбор")

if __name__ == "__main__":
    main()