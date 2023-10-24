from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint
import rsa


class Client(DatagramProtocol):
    def __init__(self, host, port, pub_key, priv_key):
        if host == "localhost":
            host = "127.0.0.1"

        self.id = host, port, pub_key, priv_key
        self.address = None
        self.pub_key = pub_key
        self.priv_key = priv_key
        self.server = '127.0.0.1', 9999

        print("Working on id:", self.id)

    def startProtocol(self):
        self.transport.write("ready".encode("utf-8"), self.server)
        
    def datagramReceived(self, datagram, addr):
        if addr == self.server:
            datagram = datagram.decode("utf-8")
            print("Choose a client from these\n", datagram)
            nazwa_hosta = input("write host:")
            numer_portu = int(input("write port:"))

            nazwa_folderu_pub = f"{numer_portu}public.pem"
            with open(nazwa_folderu_pub, 'rb') as f:
                klucz_publiczny = rsa.PublicKey.load_pkcs1(f.read())

            self.address = nazwa_hosta, numer_portu, klucz_publiczny
            reactor.callInThread(self.send_message)
        else:
            # datagram = datagram.decode("utf-8")
            nazwa_folderu_priv = f"{self.id[1]}private.pem"
            with open(nazwa_folderu_priv, 'rb') as f:
                klucz_prywatny = rsa.PrivateKey.load_pkcs1(f.read())

            print('Odkodowujemy takim plkiem:', klucz_prywatny)
            datagram = rsa.decrypt(datagram, klucz_prywatny)
            datagram = datagram.decode("utf-8")
            print(addr, ":", datagram)
            if datagram.startswith("[ALL]"):
                while True:
                    enc_msg = rsa.encrypt(datagram.encode("utf-8"), self.address[2])
                    print('Zakodowuje takim kluczem publicznym:', self.address[2])
                    self.transport.write(enc_msg, (self.address[0], self.address[1]))
                    break


    def send_message(self):
        while True:
            msg = input()
            enc_msg = rsa.encrypt(msg.encode("utf-8"), self.address[2])
            print('Zakodowuje takim kluczem publicznym:', self.address[2])
            self.transport.write(enc_msg, (self.address[0], self.address[1]))

if __name__ == '__main__':
    port = randint(1000, 5000)
    pub_key, priv_key = rsa.newkeys(1024)
    nazwa_pliku = f"{port}public.pem"
    with open(nazwa_pliku, "wb") as f:
        f.write(pub_key.save_pkcs1("PEM"))

    nazwa_pliku1 = f"{port}private.pem"
    with open(nazwa_pliku1, "wb") as f:
        f.write(priv_key.save_pkcs1("PEM"))
    reactor.listenUDP(port, Client('localhost', port, pub_key, priv_key))
    reactor.run()
    
    
    
    
            
