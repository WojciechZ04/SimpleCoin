import random
import math


# n= p.q
#phi(n) = phi(p.q)=phi(p).phi(q) = (p-1). (q-1)
#phi(n) = (p-1.q-1)


def is_prime (number):
    if number < 2:
        return False
    for i in range (2, number // 2 +1):
        if number % i == 0:
            return False
    return True

def generate_prime (min_value, max_value):
    prime = random.randint (min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime


def mod_inverse(e, phi):
    for d in range (3, phi):
        if (d * e) % phi == 1:
            return d 
    raise ValueError ("Mod_inverse does not exist!")

p, q = generate_prime(1000, 50000), generate_prime ( 1000, 50000)
while p==q:
    q= generate_prime(1000, 50000)

n = p * q
phi_n = (p-1) * (q-1)

e = random.randint (3, phi_n-1)
while math.gcd(e, phi_n) != 1: #gcd=greater common denometer     != not equal
     e = random.randint (3, phi_n - 1)

d = mod_inverse(e, phi_n)


message = input("Enter your message to Encrypt ")


print ("Prime number P: ", p)
print ("Prime number q: ", q)
print ("Public Key: ", e)
print ("Private Key: ", d)
print ("n: ", n)
print ("Phi of n: ", phi_n, " Secret")




message_encoded = [ord(ch) for ch in message]

print ("Message in ASCII code: ", message_encoded)

# (m ^ e) mod n = c 
ciphertext = [pow(ch, e, n) for ch in message_encoded]

print (message," Ciphered in: ", ciphertext)

Decodemsg= [pow(ch, d, n) for ch in ciphertext] 
print ("back to ASCII: ", Decodemsg)
msg = "".join (chr(ch) for ch in Decodemsg)
print("from ASCII to TEXT: ", msg)
