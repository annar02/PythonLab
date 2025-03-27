#Задание 9. Прочитать список строк с клавиатуры. Упорядочить по длине строки.
def read_and_sort():
    strings = []
    print("Введите строки (для завершения введите пустую строку):")
    while True:
        s = input()
        if s == "":
            break
        strings.append(s)
    
    # Сортировка списка на месте
    strings.sort(key=len)
    
    return strings

def main():
    sorted_strings = read_and_sort()
    print("\nСтроки, упорядоченные по длине:")
    for s in sorted_strings:
        print(s)

if __name__ == "__main__":
    main()