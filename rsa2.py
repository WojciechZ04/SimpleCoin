import rsa

# Wczytaj klucz prywatny z pliku PEM
with open('private_key.pem', 'rb') as private_key_file:
    private_key_data = private_key_file.read()
    private_key = rsa.PrivateKey.load_pkcs1(private_key_data)

# Wygeneruj hasło do zaszyfrowania klucza prywatnego
password = 'Twoje_hasło'.encode('utf-8')

# Zaszyfruj klucz prywatny
encrypted_private_key = rsa.encrypt(private_key_data, rsa.PublicKey(65537, 2048))

# Zapisz zaszyfrowany klucz prywatny do pliku
with open('encrypted_private_key.pem', 'wb') as encrypted_private_key_file:
    encrypted_private_key_file.write(encrypted_private_key)


# with open("2438public.pem", "rb") as f:
#     public_key = rsa.PublicKey.load_pkcs1(f.read())
#
# with open("2438private.pem", "rb") as f:
#     private_key = rsa.PrivateKey.load_pkcs1(f.read())
#
# msg = "Hejka byku"
# enc_msg = rsa.encrypt(msg.encode(), public_key)
# clear_message =  rsa.decrypt(enc_msg, private_key)
# print(clear_message.decode())
# print(private_key)
# print(public_key)