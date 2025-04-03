import re

# Проверяет является ли введенная строка доменом
def is_domain(url: str) -> bool:
    pattern = r'^https?://(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)/?$'
    return bool(re.fullmatch(pattern, url))

# Возвращает домен из URL-адреса
def extract_domain(url: str) -> str:
    pattern = r'^https?://(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)/?$'
    match = re.fullmatch(pattern, url)
    if not match:
        raise ValueError("Некорректный URL-адрес. Ожидается домен в формате http(s)://example.com")
    return match.group(1)

if __name__ == "__main__":
    test_urls = [
        "http://example.com",
        "https://example.com",
        "http://sub.example.com",
        "https://www.example.com/",
        "http://example.com/path",
        "ftp://example.com",
        "example.com",
        "http://example..com",
        "http://-example.com"
    ]
    
    print("Является ли введенная строка доменом из URL-адреса:")
    for url in test_urls:
        print(f"{url}: {is_domain(url)}")
    
    print("\nДомен из URL-адреса:")
    test_extract_urls = [
        "http://example.com",
        "https://sub.example.com",
        "http://www.example.com/",
        "https://invalid.url",
        "example.com"
    ]
    
    for url in test_extract_urls:
        try:
            print(f"{url}: {extract_domain(url)}")
        except ValueError as e:
            print(f"{url}: Ошибка - {e}")