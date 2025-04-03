# Вариант 20. 
"""Дан файл вещественных чисел. Заменить в файле каждый элемент, кроме начального и конечного, 
на его среднее арифметическое с предыдущим и последующим элементом."""
def process_file(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as file:
            numbers = [float(line.strip()) for line in file if line.strip()]
        
        if len(numbers) <= 2:
            print("Файл содержит менее 3 чисел")
            return
        
        processed_numbers = numbers.copy()
        for i in range(1, len(numbers) - 1):
            processed_numbers[i] = (numbers[i-1] + numbers[i] + numbers[i+1]) / 3
        
        with open(output_filename, 'w') as file:
            for number in processed_numbers:
                file.write(f"{number}\n")
        
        print(f"Результат записан в файл {output_filename}")
    
    except FileNotFoundError:
        print(f"Ошибка: файл {input_filename} не найден")
    except ValueError:
        print("Ошибка: в файле содержатся нечисловые данные")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

input_filename = "D:\\Python LR\\Lab1\\PythonLab\\Lab4\\input.txt"  
output_filename = "D:\\Python LR\\Lab1\\PythonLab\\Lab4\\output.txt" 
process_file(input_filename, output_filename)