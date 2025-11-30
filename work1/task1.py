def is_palindrome(s: str) -> bool:
    
    """
    проверяет является ли строка палиндромом. 

    Игнорировать регистр букв, пробелы и неалфавитно-цифровые символы (например, знаки препинания).
    """
    
    cleaned = ''.join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]

print(is_palindrome("race a car"))                      # False
print(is_palindrome("Was it a car or a cat I saw?"))   # True
print(is_palindrome("Madam"))                           # True
print(is_palindrome(""))                                # True