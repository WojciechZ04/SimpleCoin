from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Server(DatagramProtocol):
    def __init__(self):
        self.clients = set()

    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode()
        if datagram == "ready":
            adresses = "\n".join([str(x) for x in self.clients])
            print(addr,'prynt')
            print(self.clients)

            if len(self.clients) > 0:
                lista = list(self.clients)
                print(lista, 'lista')
                for i in range(len(lista)):
                    print(lista[i])
                    self.transport.write(('Jestem nowym nodem, oto moj adres' +str(addr)).encode(), lista[i])

            self.transport.write(adresses.encode(), addr)
            self.clients.add(addr)





if __name__ == '__main__':
    reactor.listenUDP(9991, Server())
    reactor.run()

            
            
