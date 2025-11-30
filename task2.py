def filter_strings(filter_func, strings):
    return list(filter(filter_func, strings))

strings = ["apple", "banana pie", "cherry", "pear", "grape"]

no_spaces = filter_strings(lambda s: ' ' not in s, strings)
not_a_start = filter_strings(lambda s: not s.lower().startswith('a'), strings)
long_enough = filter_strings(lambda s: len(s) >= 5, strings)

print(*no_spaces, sep=', ')
print(*not_a_start, sep=', ')
print(*long_enough, sep=', ')