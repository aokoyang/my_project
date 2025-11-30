import time
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция '{func.__name__}' выполнена за {end_time - start_time:.6f} секунд")
        return result
    return wrapper

@timing_decorator
def add_and_print(a: float, b: float):
    result = a + b
    print(f"Сумма {a} и {b} = {result}")
    return result

@timing_decorator
def add_from_file():
    try:
        with open('input.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) < 2:
                raise ValueError("Файл input.txt должен содержать как минимум две строки с числами.")
            a = float(lines[0].strip())
            b = float(lines[1].strip())
        
        result = a + b

        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(f"{result}\n")
        
        print(f"Результат {a} + {b} = {result} записан в output.txt")
        return result
    except FileNotFoundError:
        print("Ошибка: файл input.txt не найден.")
    except ValueError as e:
        print(f"Ошибка при чтении чисел: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        
if __name__ == "__main__":
    # Тест 1: простая функция
    add_and_print(10, 20)

    print("-" * 40)

    # Тест 2: работа с файлами
    add_from_file()