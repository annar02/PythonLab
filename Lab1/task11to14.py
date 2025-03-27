#Задания 11-14. Решить задачи по вариантам.
"""Вариант 8. Задачи 2, 4, 8, 10
Отсортировать строки в указанном порядке 
2. В порядке увеличения среднего веса ASCII-кода символа строки.
4. В порядке увеличения квадратичного отклонения среднего веса 
ASCII-кода символа строки от среднего веса ASCII-кода символа первой 
строки.  
8. В порядке увеличения квадратичного отклонения между средним 
весом ASCII-кода символа в строке и максимально среднего ASCII-кода 
тройки подряд идущих символов в строке. 
10. В порядке увеличения среднего количества «зеркальных» троек 
(например, «ada») символов в строке."""
def sort_by_weight(strings):
    def avg_weight(s):
        return sum(ord(c) for c in s) / len(s) if len(s) > 0 else 0
    
    return sorted(strings, key=avg_weight)

def sort_by_deviation(strings):
    if not strings:
        return []
    
    first_avg = sum(ord(c) for c in strings[0]) / len(strings[0]) if len(strings[0]) > 0 else 0
    
    def deviation(s):
        avg = sum(ord(c) for c in s) / len(s) if len(s) > 0 else 0
        return (avg - first_avg) ** 2
    
    return sorted(strings, key=deviation)

def sort_by_triple(strings):
    def max_triple_avg(s):
        max_avg = 0
        for i in range(len(s) - 2):
            triple_avg = (ord(s[i]) + ord(s[i+1]) + ord(s[i+2])) / 3
            if triple_avg > max_avg:
                max_avg = triple_avg
        return max_avg
    
    def deviation(s):
        avg = sum(ord(c) for c in s) / len(s) if len(s) > 0 else 0
        return (avg - max_triple_avg(s)) ** 2
    
    return sorted(strings, key=deviation)

def main():
    print("Выберете в каком порядке отсортировать строки:")
    print("1. В порядке увеличения среднего веса ASCII-кода символа строки")
    print("2. В порядке увеличения квадратичного отклонения от среднего веса первой строки")
    print("3. В порядке увеличения отклонения от максимального среднего тройки символов")
    print("4. В порядке увеличения среднего количества зеркальных троек символов")
    
    choice = input("Введите номер задачи (1-4): ")
    strings = input("Введите строки через запятую: ").split(',')
    strings = [s.strip() for s in strings]
    
    if choice == '1':
        result = sort_by_weight(strings)
    elif choice == '2':
        result = sort_by_deviation(strings)
    elif choice == '3':
        result = sort_by_triple(strings)
    print("Результат сортировки:")
    for s in result:
        print(s)

if __name__ == "__main__":
    main()