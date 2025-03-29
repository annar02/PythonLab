# Вариант 10. Забастовки
def count_strikes(N, K, schedules):
    # Словарь для хранения дней забастовок каждой партии
    party_strikes = {}
    
    for i in range(K):
        a, b = schedules[i]
        party_strikes[i] = set()
        day = a
        while day <= N:
            if day % 7 != 6 and day % 7 != 0:
                party_strikes[i].add(day)
            day += b
    
    # Объединяем все дни забастовок в одно множество
    all_strikes = set()
    for strikes in party_strikes.values():
        all_strikes.update(strikes)
    
    return len(all_strikes)

def main():
    print("Программа подсчёта забастовок")
    print("-----------------------------")

    while True:
        try:
            N = int(input("Введите количество дней в году (N): "))
            if N <= 0:
                print("Ошибка: N должно быть положительным.")
                continue
            break
        except ValueError:
            print("Ошибка: введите целое число.")
    
    while True:
        try:
            K = int(input("Введите количество партий (K): "))
            if K <= 0:
                print("Ошибка: K должно быть положительным.")
                continue
            break
        except ValueError:
            print("Ошибка: введите целое число.")

    schedules = []
    for i in range(1, K + 1):
        print(f"\nПартия {i}:")
        while True:
            try:
                a = int(input("  Начальный день (a): "))
                if a <= 0 or a > N:
                    print(f"Ошибка: a должно быть от 1 до {N}.")
                    continue
                break
            except ValueError:
                print("Ошибка: введите целое число.")
        
        while True:
            try:
                b = int(input("  Периодичность (b): "))
                if b <= 0:
                    print("Ошибка: b должно быть положительным.")
                    continue
                break
            except ValueError:
                print("Ошибка: введите целое число.")
        
        schedules.append((a, b))
    
    total = count_strikes(N, K, schedules)
    print(f"\nВсего забастовок: {total}")

if __name__ == "__main__":
    main()