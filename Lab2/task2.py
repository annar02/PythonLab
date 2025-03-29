# Вариант 7. Страны и города 
def country_city_dict():
    countries = {}
    print("Введите список стран и их городов (пустая строка для завершения):")
    while True:
        line = input().strip()
        if not line:
            break
        parts = line.split()
        country = parts[0]
        cities = parts[1:]
        countries[country] = cities
    return countries

def city_country_dict(country_dict):
    city_dict = {}
    for country, cities in country_dict.items():
        for city in cities:
            city_dict[city] = country
    return city_dict

def main():
    country_dict = country_city_dict()
    
    city_dict = city_country_dict(country_dict)
    
    print("\nВведите названия городов для поиска (пустая строка для завершения):")
    while True:
        city = input().strip()
        if not city:
            break
        country = city_dict.get(city, "Город не найден")
        print(f"{city} - {country}")

if __name__ == "__main__":
    main()