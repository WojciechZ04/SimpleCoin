from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import threading


class Server(DatagramProtocol):
    def __init__(self):
        self.clients = set()

    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode()
        if datagram == "ready":
            addresses = "\n".join([str(x) for x in self.clients])
            # print(addr, 'prynt')
            # print(self.clients)

            if len(self.clients) > 0:
                lista = list(self.clients)
                # print(lista, 'lista')
                for i in range(len(lista)):
                    # print(lista[i])
                    self.transport.write(('Jestem nowym nodem, o to moj adres' + str(addr)).encode(), lista[i])

            self.transport.write(addresses.encode(), addr)
            self.clients.add(addr)

    def get_nodes(self):
        return self.clients


class Terminal:
    def __init__(self):
        self.server = server
        self.commands = {
            'bch': self.show_blockchain,
            'nodes': self.show_nodes,
            'help': self.help
        }

    def run_terminal(self):
        while True:
            command = input(">>>")
            if command.lower() in self.commands:
                self.commands[command.lower()]()
            else:
                print("Unknown command. Type 'help' to see all commands.")

    def show_blockchain(self):
        exit()

    def show_nodes(self):
        nodes = self.server.get_nodes()
        print("Current nodes: ")
        for node in nodes:
            print(node)

    def help(self):
        print("Available commands: ")
        for command in self.commands:
            print(f"{command}")


def run_terminal():
    terminal = Terminal()
    terminal.run_terminal()


if __name__ == '__main__':
    server = Server()

    terminal_thread = threading.Thread(target=run_terminal)
    terminal_thread.start()

    reactor.listenUDP(9998, server)
    reactor.run()
