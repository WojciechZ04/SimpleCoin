import rsa



with open("1046public.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

with open("1046private.pem", "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

msg = "Hejka byku"
enc_msg = rsa.encrypt(msg.encode(), public_key)
clear_message =  rsa.decrypt(enc_msg, private_key)
print(clear_message.decode())
print(private_key)
print(public_key)