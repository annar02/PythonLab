#Задание 10. Дан список строк с клавиатуры. Упорядочить по количеству слов в строке.
def read_and_sort_by_word_count():
    strings = []
    print("Введите строки (для завершения введите пустую строку):")
    while True:
        s = input().strip()
        if s == "":
            break
        strings.append(s)
    
    sorted_strings = sorted(strings, key=lambda x: len(x.split()))
    
    return sorted_strings

def main():
    sorted_strings = read_and_sort_by_word_count()
    print("\nСтроки, упорядоченные по количеству слов:")
    for i, s in enumerate(sorted_strings, 1):
        print(f"{i}. '{s}' (слов: {len(s.split())})")

if __name__ == "__main__":
    main()