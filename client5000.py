from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from chain import Chain
import rsa
import threading

### Poziom trudności wydobycia
#Chain(10) - 2 zera na początku hasha
#Chain(15) - 4 zera na początku hasha itd.
chain = Chain(10)


class Client(DatagramProtocol):
    def __init__(self, host, port, pub_key, priv_key):
        if host == "localhost":
            host = "127.0.0.1"

        self.blockchain = chain.blocks
        self.id = host, port, pub_key, priv_key
        self.address = None
        self.pub_key = pub_key
        self.priv_key = priv_key
        self.server = '127.0.0.1', 9990

        print(self.blockchain)
        print("Working on id:", self.id)

    def startProtocol(self):
        self.transport.write("ready".encode("utf-8"), self.server)

    def datagramReceived(self, datagram, addr):
        if addr == self.server:
            datagram = datagram.decode("utf-8")
            if datagram.startswith("Jestem") == False:
                print("Choose a client from these\n", datagram)
                nazwa_hosta = '127.0.0.1'
                numer_portu = 5001
    #
    #             nazwa_folderu_pub = f"{numer_portu}public.pem"
    #             with open(nazwa_folderu_pub, 'rb') as f:
    #                 klucz_publiczny = rsa.PublicKey.load_pkcs1(f.read())
    #
    #             self.address = nazwa_hosta, numer_portu, klucz_publiczny
    #             # reactor.callInThread(self.send_message)
    #             # reactor.callInThread(self.create_block)
    #
    #     else:
    #         # datagram = datagram.decode("utf-8")
    #         nazwa_folderu_priv = f"{self.id[1]}private.pem"
    #         nazwa_folderu_pub = f"{addr[1]}public.pem"
    #
    #         ##########
    #
    #         with open(nazwa_folderu_priv, 'rb') as f:
    #             klucz_prywatny = rsa.PrivateKey.load_pkcs1(f.read())
    #         with open(nazwa_folderu_pub, 'rb') as f:
    #             klucz_publiczny = rsa.PublicKey.load_pkcs1(f.read())
    #         with open(f"{addr[1]}signature", "rb") as f:
    #             signature = f.read()
    #         print(f"Czy to port wysyłającego? {addr[1]}")
    #         print(rsa.verify(datagram, signature, klucz_publiczny))
    #         ###########
    #
    #         print('Odkodowujemy takim plkiem:', klucz_prywatny)
    #         # datagram1 = datagram.decode("utf-8")
    #         if 'wiadomo' in str(datagram):
    #             datagram = datagram.decode("utf-8")
    #         else:
    #             datagram = rsa.decrypt(datagram, klucz_prywatny)
    #             datagram = datagram.decode("utf-8")
    #
    #         print(addr, ":", datagram)
    #
    #     if addr == self.server:
    #         if datagram.startswith("Jestem"):
    #             print(datagram, 'Tu jest ten nowy')

    # def send_message(self):
    #     while True:
    #         msg = input()
    #         if msg.startswith("[Add nodes]"):
    #             nowy_host = '127.0.0.1'
    #             nowy_port = int(input("write port:"))
    #             nazwa_folderu_pub1 = f"{nowy_port}public.pem"
    #             with open(nazwa_folderu_pub1, 'rb') as f:
    #                 nowy_klucz_publiczny = rsa.PublicKey.load_pkcs1(f.read())
    #
    #             self.address = self.address + (nowy_host,) + (nowy_port,) + (nowy_klucz_publiczny,)
    #             print(len(self.address), 'Ile elementow w self adresie')
    #         # enc_msg = rsa.encrypt(msg.encode("utf-8"), self.address[2])
    #         # signature = rsa.sign(msg.encode(), private_key, "SHA-256")
    #         # with open("signature", "wb") as f:
    #         #     f.write(signature)
    #         if msg.startswith("[Add nodes]") == False:
    #             a = int(input('Chcesz wysłac do kadego? 0, Do konkretnego wezla? 1 '))
    #             if a == 0:
    #                 for i in range(0, len(self.address), 3):
    #                     if i < len(self.address) - 2:
    #                         enc_msg = rsa.encrypt(msg.encode("utf-8"), self.address[i + 2])
    #
    #                         signature = rsa.sign(enc_msg, self.priv_key, "SHA-256")
    #                         print(f"Port podpisującego/wysyłającego: {self.id[1]}")
    #                         with open(f"{self.id[1]}signature", "wb") as f:
    #                             f.write(signature)
    #
    #                         # print('Zakodowuje takim kluczem publicznym:', self.address[i+2])
    #                         self.transport.write(enc_msg, (self.address[i], self.address[i + 1]))
    #             if a == 1:
    #                 port = int(input('Podaj port wezla'))
    #                 with open(f"{port}public.pem", 'rb') as f:
    #                     kl_pub = rsa.PublicKey.load_pkcs1(f.read())
    #                 enc_msg = rsa.encrypt(msg.encode("utf-8"), kl_pub)
    #
    #                 signature = rsa.sign(enc_msg, self.priv_key, "SHA-256")
    #                 print(f"Port podpisującego/wysyłającego: {self.id[1]}")
    #                 with open(f"{self.id[1]}signature", "wb") as f:
    #                     f.write(signature)
    #
    #                 # print('Zakodowuje takim kluczem publicznym:', kl_pub)
    #
    #                 self.transport.write(enc_msg, ('127.0.0.1', port))
    #
    #                 for i in range(0, len(self.address), 3):
    #                     if i < len(self.address) - 2:
    #                         self.transport.write(f"Wezeł {self.id[1]} wysłał wiadomość do wezła {port}".encode("utf-8"),
    #                                              (self.address[i], self.address[i + 1]))
    #
    #         # print('Zakodowuje takim kluczem publicznym:', self.address[2])
    #         # self.transport.write(enc_msg, (self.address[0], self.address[1]))
    #         # if len(self.address) > 3:
    #         #     print('Zakodowuje takim kluczem publicznym:', self.address[5])
    #         #     self.transport.write(enc_msg, (self.address[3], self.address[4]))


class Terminal:
    def __init__(self):
        self.client = client
        self.commands = {
            'create': self.create_block,
            'show': self.show_blockchain,
            'verify': self.verify,
            'help': self.help
        }

    def run_terminal(self):
        while True:
            command = input(">>>")
            if command.lower() in self.commands:
                self.commands[command.lower()]()
            else:
                print("Unknown command. Type 'help' to see all commands.")

    def create_block(self):
        data = input("Write block data: ")
        chain.add_to_pool(data)
        block = chain.mine()
        #client.send_message(block)


    def show_blockchain(self):
        blocks = self.client.blockchain
        print("Current blockchain: ")
        for block in blocks:
            print("\nHash: ", block.hash.hexdigest())
            print("Previous Hash: ", block.prev_hash.hexdigest())
            print("Nonce: ", block.nonce)
            print("Data: ", block.data)

    def verify(self):
        exit()

    def help(self):
        print("Available commands: ")
        for command in self.commands:
            print(f"{command}")


def run_terminal():
    terminal = Terminal()
    terminal.run_terminal()


if __name__ == '__main__':
    port = 5000
    pub_key, priv_key = rsa.newkeys(1024)
    nazwa_pliku = f"{port}public.pem"
    with open(nazwa_pliku, "wb") as f:
        f.write(pub_key.save_pkcs1("PEM"))

    nazwa_pliku1 = f"{port}private.pem"
    with open(nazwa_pliku1, "wb") as f:
        f.write(priv_key.save_pkcs1("PEM"))

    client = Client('localhost', port, pub_key, priv_key)

    terminal_thread = threading.Thread(target=run_terminal)
    terminal_thread.start()

    reactor.listenUDP(port, client)
    reactor.run()
