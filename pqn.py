def czy_jest_liczba_pierwsza(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def rozklad_na_czynniki_pierwsze(n):
    czynniki_pierwsze = []
    for i in range(2, n + 1):
        while czy_jest_liczba_pierwsza(i) and n % i == 0:
            czynniki_pierwsze.append(i)
            n //= i
    return czynniki_pierwsze

n = int(input("Podaj liczbę do rozkładu: "))

if n < 2:
    print("Liczba musi być większa lub równa 2.")
else:
    czynniki = rozklad_na_czynniki_pierwsze(n)
    if len(czynniki) == 2:
        print(f"Rozkład liczby {n} na dwa czynniki pierwsze: {czynniki[0]} i {czynniki[1]}")
    else:
        print("Nie można znaleźć dwóch czynników pierwszych.")
