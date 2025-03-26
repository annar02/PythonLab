#Задание 5. Дана строка. Необходимо найти все даты, которые описаны в 
#виде "31 февраля 2007".
import re

def find_dates(text):
    date_pattern = r'\b(\d{1,2})\s+([а-яА-Я]+)\s+(\d{4})\b'
    dates = re.findall(date_pattern, text)
    
    return dates

def main():
    text = input("Введите текст для поиска дат: ")
    found_dates = find_dates(text)
    
    if found_dates:
        print("Найденные даты:")
        for day, month, year in found_dates:
            print(f"{day} {month} {year}")
    else:
        print("Даты не найдены")

if __name__ == "__main__":
    main()