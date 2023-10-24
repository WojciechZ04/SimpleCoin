import rsa

with open("4805public.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())
    
with open("4805private.pem", "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())



msg = "Wiadomosc"
signature = rsa.sign(msg.encode(), private_key, "SHA-256")

with open("signature", "wb") as f:
    f.write(signature)


stara_krotka = (1, 2, 3)
nowy_element = 4
nowa_krotka = stara_krotka + (nowy_element,)
print(nowa_krotka)