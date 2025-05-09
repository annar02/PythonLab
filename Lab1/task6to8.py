#Задания 6-8. Решить задачи по вариантам.
"""Вариант 8. Задачи 2, 10, 17
2. Дана строка. Необходимо найти все строчные символы латиницы, 
которые в ней используются. 
10. Дана строка. Необходимо найти количество задействованных 
символов латиницы в этой строке (без дубликатов).
17. Дана строка в которой записан путь к файлу. Необходимо найти имя 
файла без расширения."""
def find_letters(text):
    lowercase_letters = sorted({char for char in text if char.islower() and char.isascii()})
    return lowercase_letters

def count_chars(text):
    latin_chars = {char.lower() for char in text if char.isalpha() and char.isascii()}
    return len(latin_chars)

def get_filename_without_extension(path):
    filename = path.split('/')[-1].split('\\')[-1]
    return filename.split('.')[0] if '.' in filename else filename

def main():
    print("Выберите задачу для решения:")
    print("1. Найти все строчные символы латиницы в строке")
    print("2. Найти количество уникальных символов латиницы в строке")
    print("3. Найти имя файла без расширения в пути")
    
    choice = input("Введите номер задачи (1-3): ")
    
    if choice == '1':
        text = input("Введите строку для анализа: ")
        letters = find_letters(text)
        print(f"Строчные символы латиницы в строке: {', '.join(letters)}" if letters else "Строчных символов латиницы не найдено")
    elif choice == '2':
        text = input("Введите строку для анализа: ")
        count = count_chars(text)
        print(f"Количество уникальных символов латиницы: {count}")
    elif choice == '3':
        path = input("Введите путь к файлу: ")
        filename = get_filename_without_extension(path)
        print(f"Имя файла без расширения: {filename}")
    else:
        print("Некорректный выбор")

if __name__ == "__main__":
    main()