from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint
import rsa

class Client(DatagramProtocol):
    def __init__(self, host, port, pub_key, priv_key):
        if host == "localhost":
            host = "127.0.0.1"

        self.id = host, port, pub_key
        self.address = None
        self.pub_key = pub_key
        self.server = '127.0.0.1', 9999

        print("Working on id:", self.id)

    def startProtocol(self):
        self.transport.write("ready".encode("utf-8"), self.server)
        
    def datagramReceived(self, datagram, addr):
        if addr == self.server:
            datagram = datagram.decode("utf-8")
            print("Choose a client from these\n", datagram)
            self.address = input("write host:"), int(input("write port"))
            reactor.callInThread(self.send_message)
        else:
            #datagram = datagram.decode("utf-8")
            datagram = rsa.decrypt(datagram, self.priv_key)
            print(addr, ":", datagram)
            

    def send_message(self):
        while True:
            msg = input()
            enc_msg = rsa.encrypt(msg.encode("utf-8"), self.pub_key)
            self.transport.write(str(enc_msg).encode("utf-8"), self.address)

if __name__ == '__main__':
    port = randint(1000, 5000)
    pub_key, priv_key = rsa.newkeys(1024)
    reactor.listenUDP(port, Client('localhost', port, pub_key, priv_key))
    reactor.run()
    
    
    
    
            
