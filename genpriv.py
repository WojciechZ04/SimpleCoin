e = 7
numbers = list(range(100000))
print(numbers)

for ele in numbers:
    if ((e*ele)%120) == 1:
        print('Klucz prywatny to:' , ele)
