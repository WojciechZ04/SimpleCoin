import rsa

with open("1046public.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())
    
with open("1595private.pem", "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())



msg = "Wiadomosc"
signature = rsa.sign(msg.encode(), private_key, "SHA-256")

with open("signature", "wb") as f:
    f.write(signature)

print(rsa.verify(msg.encode(), signature, public_key))