import rsa

public_key= rsa.newkeys(1024)
print(type(public_key[0]))
address = input("write host:"), int(input("write port"))
print(address)
print(type(address))