n = 143
e = 7
d = 43
fi = 120
numbers = list(range(10000))
print(numbers)

pot_keys = []

for ele in numbers:
    if ((e*ele) % fi) == 1:
        print('Klucz prywatny to:' , ele)
        pot_keys.append(ele)
        
        
msg = 15

S = (msg ** d) % n
print(S)

print((S**e) % n)

pot_keys1 = []

for ele in numbers:
    if ((msg**ele) % n) == S:
        print(ele)
        pot_keys1.append(ele)

for ele in pot_keys:
    for ele1 in pot_keys1:
        if ele == ele1:
            print(ele, '=', ele1)
