from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint
import rsa
import hashlib
from BBlock import Block, choose_blockchain_diffi, is_valid_new_block, is_valid_chain, generate_next_block, find_block, choose_blockchain_ts
import time
from datetime import datetime

blockchain = []
wyrzucone_z_utxo_transakcje = []
class Client(DatagramProtocol):
    def __init__(self, host, port, pub_key, priv_key):
        if host == "localhost":
            host = "127.0.0.1"
        self.id = host, port, pub_key, priv_key
        self.address = None
        self.pub_key = pub_key
        self.priv_key = priv_key
        self.server = '127.0.0.1', 9000
        print("Working on id:", self.id)

    def startProtocol(self):
        self.transport.write("ready".encode("utf-8"), self.server)
        
    def datagramReceived(self, datagram, addr):
        if addr == self.server:
            datagram = datagram.decode("utf-8")
            if datagram.startswith("Jestem") == False:
                print("Choose a client from these\n", datagram)
                nazwa_hosta = '127.0.0.1'
                numer_portu = 2000
                self.address = nazwa_hosta, numer_portu
                reactor.callInThread(self.send_message)

        else:
            datagram = datagram.decode("utf-8")
            print(addr, ":", datagram)
            print(datagram)
            if datagram.startswith("$"):
                datagram = datagram[1:]
                flag2 = 1
            else:
                flag2 = 0
            blockchain.append(json.loads(datagram))
            data = blockchain[-1]['data']
            if type(data) != dict:
                data = data.replace("'tx_ins'", '"tx_ins"')
                data = data.replace("'tx_outs'", '"tx_outs"')
                data = data.replace("'amount'", '"amount"')
                data = data.replace("'tx_out_id'", '"tx_out_id"')
                data = data.replace("'tx_out_index'", '"tx_out_index"')
                data = data.replace("'address'", '"address"')
                data = data.replace(f"'{str(data[27:91])}'", f'"{str(data[27:91])}"')
                data = data.replace(f"'{str(data[140:396])}'", f'"{str(data[140:396])}"')
                data = json.loads(data)
            blockchain[-1]['data'] = data
            # if len(blockchain) > 1 and (blockchain[-1]['index'] <= blockchain[-2]['index']):
            #     print('Mamy konflikt')
            #     if blockchain[-1]['timestamp'] < blockchain[-2]['timestamp']:
            #         print('Co jest wywalane?', blockchain2[-2].index, blockchain2[-2].hash)
            #         blockchain.pop(-2)
            #         print('Dodano blok')
            #     else:
            #         blockchain.pop()
            #         print('Nie dodano bloku bo zapóźno wykopany')

            print(len(blockchain2))
            nowy_blok = Block(blockchain[-1]['index'], blockchain[-1]['hash'],
                              blockchain[-1]['previous_hash'], blockchain[-1]['timestamp'],
                              blockchain[-1]['data'], blockchain[-1]['nonce'], blockchain[-1]['difficulty'])
            print(type(nowy_blok))
            if nowy_blok.index != blockchain2[-1].index:
                blockchain2.append(nowy_blok)
            for i in range(len(blockchain2)-1):
                if blockchain2[i].hash == blockchain2[i+1].previous_hash:
                    print('Łańcuch zgodny pod względem hashy')
                    flag = 1
                else:
                    if flag2 != 1:
                        print(f'Niezgodne bloki {i} oraz {i+1}, należy wycofać blok {i} i poprosić resztę sieci o blok {i}')
                        flag = 0
                        # blockchain2.pop(i)
                        self.transport.write(f"Wyślij mi blok nr {i}".encode("utf-8"), ('127.0.0.1', 3000))
                        print('Utxo przed odrzuceniem orphan blocka', utxo_set)
                        utxo_set.pop() #wyrzucenie tej transakcji że node2000 może coś wydać
                        utxo_set.append(wyrzucone_z_utxo_transakcje[0])
                        wyrzucone_z_utxo_transakcje.pop()
                        Node2000.saldo -= 100
                        Node1000.saldo += 100
                        print('Utxo po odrzuceniu orphan blocka', utxo_set)
                        print('Stany kont po wycofaniu orphan block:', '\n', 'Saldo Node1000:',Node1000.saldo,'\n', 'Saldo Node2000:',Node2000.saldo)
                    break
            for i in range(len(blockchain2)-1):
                # print('tututuutut', blockchain2[i].index)
                if blockchain2[i].index != blockchain2[i+1].index-1:
                    print(blockchain2[i].index, blockchain2[i+1].index-1)
                    blockchain2[-3] = blockchain2[-1]
                    blockchain2.pop()
                    # print('Tutaj sie naprawi')
                else:
                    pass
                    # print('legancko po kolei')
            if flag == 1 and flag2 != 1:
                bzyt = blockchain2[-1].data
                if type(bzyt) == str:
                    json_string_fixed = bzyt.replace("'", "\"")
                    bzyt = json.loads(json_string_fixed)
                transakcja = Transaction([TxIn(bzyt['tx_ins'][0]['tx_out_id'],0)], [TxOut(bzyt['tx_outs'][0]['address'], 100)])
                # print('transakcja', transakcja)
                print('utxo przed', utxo_set)
                print('Salda przed transakcją:', '\n', 'Saldo Node1000:',Node1000.saldo,'\n', 'Saldo Node2000:',Node2000.saldo)
                # print('adres utxo', utxo_set[0]['address'])
                if zweryfikuj_transakcje2(transakcja, utxo_set):
                    Node2000.saldo += transakcja.tx_outs[0].amount
                    Node1000.saldo -= transakcja.tx_outs[0].amount
                    wyrzucone_z_utxo_transakcje.append({'txOutId': get_transaction_id(TRANSACTION_CB), 'txOutIndex': 0, 'amount': TRANSACTION_CB.tx_outs[0].amount, 'address': TRANSACTION_CB.tx_outs[0].address})
                else:
                    blockchain2.pop()
                    print('Nie zweryfikowano transakcji, nie dodano bloku do łańcucha')
                print('Salda po transakcji:', '\n', 'Saldo Node1000:', Node1000.saldo, '\n', 'Saldo Node2000:',
                      Node2000.saldo)
                # print('utxo po', utxo_set)
            for ele in blockchain2:
                print('Tutaj','numer bloku:',ele.index, 'hash:', ele.hash,'poprzedni hash:', ele.previous_hash)


        if addr == self.server:
            if datagram.startswith("Jestem"):
                print(datagram, 'Tu jest ten nowy')


    def send_message(self):
        while True:
            msg = input('Pisz wiadomosc:')
            if msg.startswith("[Add nodes]"):
                nowy_host = '127.0.0.1'
                nowy_port = int(input("write port:"))
                self.address = self.address + (nowy_host,) + (nowy_port,)
                print(len(self.address), 'Ile elementow w self adresie')

            if msg.startswith("[Add nodes]") == False and msg.startswith("[Add block]") == False:
                port = int(input('Podaj port wezla'))
                self.transport.write(msg.encode("utf-8"), ('127.0.0.1', port))
                for i in range(0,len(self.address),3):
                    if i < len(self.address) - 2:
                        self.transport.write(f"Wezeł {self.id[1]} wysłał wiadomość do wezła {port}".encode("utf-8"), (self.address[i], self.address[i+1]))
                # self.transport.write((block.to_json_prev_hash()+'$'+block.to_json_data()+'$'+block.to_json_nonce()).encode("utf-8"), ('127.0.0.1', port))
            if msg.startswith("[Add block]"):
                bn3 = generate_next_block(str(TRAN_1.to_json()), blockchain2, 2)
                blockchain2.append(bn3)
                # spr = is_valid_chain(blockchain2, bG2)
                bn3 = str(bn3.to_json())
                msg = bn3
                port = int(input('Podaj port wezla'))
                self.transport.write(msg.encode("utf-8"), ('127.0.0.1', port))



class Transaction:
    def __init__(self, tx_ins, tx_outs):
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs


    def to_json(self):
        return {
            "tx_ins": [tx_in.__dict__ for tx_in in self.tx_ins],
            "tx_outs": [tx_out.__dict__ for tx_out in self.tx_outs]
        }



def get_transaction_id(transaction):
    tx_insy = ''.join([f"{ele.tx_out_id}{ele.tx_out_index}" for ele in transaction.tx_ins])
    tx_outsy = ''.join([f"{ele.address}{ele.amount}" for ele in transaction.tx_outs])
    razem = tx_insy + tx_outsy
    sha256 = hashlib.sha256()
    sha256.update(razem.encode('utf-8'))
    return sha256.hexdigest()

class TxIn:
    def __init__(self, tx_out_id, tx_out_index):
        self.tx_out_id = tx_out_id
        self.tx_out_index = tx_out_index

    def to_json(self):
        return self.__dict__

class TxOut:
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount

    def to_json(self):
        return self.__dict__


def podpisz(T,numer_klucza):
    nazwa_pliku = f"{numer_klucza}private.pem"
    with open(nazwa_pliku, 'rb') as f:
        klucz_prywatny = rsa.PrivateKey.load_pkcs1(f.read())
        h = hashlib.sha256(get_transaction_id(T).encode('utf-8')).digest()
        signature = rsa.sign(h, klucz_prywatny, 'SHA-256')
        with open('1000signature', 'wb') as podpis_file:
            podpis_file.write(signature)
    return signature


tx_ins_cb = [TxIn(bytes.fromhex('00' * 32),  int('ffffffff', 16))]
tx_outs_cb = [TxOut('Adres1', 10)]
TRANSACTION_CB = Transaction(tx_ins_cb, tx_outs_cb)


# with open("1871public.pem", 'rb') as f:
#     publikey = f.read()
# with open("1753public.pem", 'rb') as f:
#     publikey_zlodzieja = f.read()


# TRAN_1 = Transaction([TxIn(get_transaction_id(TRANSACTION_CB),0)], [TxOut(publikey.decode('utf-8'), 100)])
# utxo_set = [{'txOutId': get_transaction_id(TRANSACTION_CB), 'txOutIndex': 0, 'amount': 100, 'address': publikey.decode('utf-8')}]
# podpis = podpisz(TRAN_1, 1871)
# TRAN_1 = Transaction([TxIn(get_transaction_id(TRANSACTION_CB),0)], [TxOut(publikey_zlodzieja.decode('utf-8'), 100)])
def update_utxo(utxo, last_T):
    utxo.pop()
    utxo.append({})
    utxo[0]['txOutId'] = get_transaction_id(last_T)
    utxo[0]['txOutIndex'] = 0
    utxo[0]['amount'] = last_T.tx_outs[0].amount
    utxo[0]['address'] = last_T.tx_outs[0].address
    return utxo

def zweryfikuj_transakcje(T, podpis,utxo_set):
    for i in range(len(utxo_set)):
        print('Dla i równego:', i)
        if utxo_set[i]['txOutId'] == T.tx_ins[0].tx_out_id and utxo_set[i]['txOutIndex'] == T.tx_ins[0].tx_out_index:
            print('     Taka transakcja znajduje się w UTXO')
            a = 1
            try:
                do_weryfikacji = get_transaction_id(T).encode('utf-8')
                h = hashlib.sha256(do_weryfikacji).digest()
                rsa.verify(h, podpis, rsa.PublicKey.load_pkcs1(utxo_set[i]['address'].encode('utf-8')))
                print('     Podpis zgodny')
                b = 1
            except rsa.VerificationError:
                print("     Błąd weryfikacji podpisu")
                b = 0
            if T.tx_outs[0].amount == utxo_set[i]['amount']:
                print('     Kwoty zgodne')
                c = 1
            else:
                print('     Niezgodne kwoty z podanym UTXO')
                c = 0
        else:
            print('     Transakcji nie ma w UTXO', utxo_set[i]['txOutId'] , T.tx_ins[0].tx_out_id, utxo_set[i]['txOutIndex'] == T.tx_ins[0].tx_out_index)
            a = 0
        if a == 1 and b == 1 and c == 1:
            utxo_set = update_utxo(utxo_set, T)
            return True

        else:
            return False

def zweryfikuj_transakcje2(T,utxo_set):
    for i in range(len(utxo_set)):
        print('Dla i równego:', i)
        if utxo_set[i]['txOutId'] == T.tx_ins[0].tx_out_id and utxo_set[i]['txOutIndex'] == T.tx_ins[0].tx_out_index:
            print('     Taka transakcja znajduje się w UTXO')
            a = 1
            try:
                with open("1000signature", 'rb') as f:
                    podpis = f.read()
                do_weryfikacji = get_transaction_id(T).encode('utf-8')
                h = hashlib.sha256(do_weryfikacji).digest()
                # print('do weryfikacji', do_weryfikacji)
                # print('Wyswietlam', utxo_set[i]['address'].encode('utf-8'))
                rsa.verify(h, podpis, rsa.PublicKey.load_pkcs1(utxo_set[i]['address'].encode('utf-8')))
                print('     Podpis zgodny')
                b = 1
            except rsa.VerificationError:
                print("     Błąd weryfikacji podpisu")
                b = 0
            if T.tx_outs[0].amount == utxo_set[i]['amount']:
                print('     Kwoty zgodne')
                c = 1
            else:
                print('     Niezgodne kwoty z podanym UTXO')
                c = 0
        else:
            print('     Transakcji nie ma w UTXO', utxo_set[i]['txOutId'] , T.tx_ins[0].tx_out_id, utxo_set[i]['txOutIndex'] == T.tx_ins[0].tx_out_index)
            a = 0
        if a == 1 and b == 1 and c == 1:
            utxo_set = update_utxo(utxo_set, T)
            return True

        else:
            return False


class Node():
    def __init__(self, adres, saldo):
        self.adres = adres
        self.saldo = saldo

with open("1000public.pem", 'rb') as f:
    publikey1000 = f.read()
with open("2000public.pem", 'rb') as f:
    publikey2000 = f.read()
# with open("3000public.pem", 'rb') as f:
#     publikey3000 = f.read()
# with open("4000public.pem", 'rb') as f:
#     publikey4000 = f.read()
# with open("5000public.pem", 'rb') as f:
#     publikey5000 = f.read()




tx_ins_cb = [TxIn(bytes.fromhex('00' * 32),  int('ffffffff', 16))]
tx_outs_cb = [TxOut(publikey1000.decode('utf-8'), 100)]
TRANSACTION_CB = Transaction(tx_ins_cb, tx_outs_cb)

global utxo_set
utxo_set = [{'txOutId': get_transaction_id(TRANSACTION_CB), 'txOutIndex': 0, 'amount': TRANSACTION_CB.tx_outs[0].amount, 'address': TRANSACTION_CB.tx_outs[0].address}]
print('id coinbase', get_transaction_id(TRANSACTION_CB))
print('utxo na poczatku', utxo_set)
# print('UTXO PRZED 1 TRANSAKCJA', utxo_set)
Node1000 = Node(publikey1000, 100)
Node2000 = Node(publikey2000, 0)
# Node3000 = Node(publikey3000, 0)
# Node4000 = Node(publikey4000, 0)
# Node5000 = Node(publikey5000, 0)
Nodes = [Node1000, Node2000]

#TRANSACTION_CB = TRANSACTION_CB
# print('utxo przed', utxo_set)
TRAN_1 = Transaction([TxIn(get_transaction_id(TRANSACTION_CB),0)], [TxOut(publikey2000.decode('utf-8'), 100)])
# print('Id tran1', TRAN_1.tx_ins[0].tx_out_id)
# print('halo', TRAN_1.tx_ins[0].tx_out_id)
# print('halo', TRAN_1.tx_outs[0].address)
# TRAN_1_probna = Transaction([TxIn(TRAN_1.tx_ins[0].tx_out_id,0)], [TxOut(TRAN_1.tx_outs[0].address, 100)])
podpis_1 = podpisz(TRAN_1, 1000)
# zweryfikuj_transakcje(TRAN_1_probna, podpis_1,utxo_set)
# zweryfikuj_transakcje(TRAN_1_probna, podpis_1)
# utxo_set = update_utxo(utxo_set, TRAN_1)
# print('UTXO PO 1 TRANSAKCJI', utxo_set)

# #
# TRAN_2 = Transaction([TxIn(get_transaction_id(TRAN_1),0)], [TxOut(publikey1000.decode('utf-8'), 100)])
# podpis_2 = podpisz(TRAN_2, 2000)
# zweryfikuj_transakcje(TRAN_2, podpis_2,utxo_set)
# # utxo_set = update_utxo(utxo_set, TRAN_2)
# print('UTXO PO 2 TRANSAKCJI', utxo_set)

# TRAN_3 = Transaction([TxIn(get_transaction_id(TRAN_2),0)], [TxOut(publikey4000.decode('utf-8'), 100)])
# podpis_3 = podpisz(TRAN_3, 3000)
# zweryfikuj_transakcje(TRAN_3, podpis_3)
# utxo_set = update_utxo(utxo_set, TRAN_3)
# print('UTXO PO 3 TRANSAKCJI', utxo_set)
#
# TRAN_4 = Transaction([TxIn(get_transaction_id(TRAN_3),0)], [TxOut(publikey5000.decode('utf-8'), 100)])
# podpis_4 = podpisz(TRAN_4, 4000)
# zweryfikuj_transakcje(TRAN_4, podpis_4)
# utxo_set = update_utxo(utxo_set, TRAN_4)
# print('UTXO PO 4 TRANSAKCJI', utxo_set)
#
# TRAN_5 = Transaction([TxIn(get_transaction_id(TRAN_4),0)], [TxOut(publikey3000.decode('utf-8'), 100)])
# podpis_5 = podpisz(TRAN_5, 5000)
# zweryfikuj_transakcje(TRAN_5, podpis_5)
# utxo_set = update_utxo(utxo_set, TRAN_5)
# print('UTXO PO 5 TRANSAKCJI', utxo_set)







def sum_amounts(lyst):
    result_dict = {}
    for ele in lyst:
        address = ele.get('address')
        amount = ele.get('amount', 0)
        if address:
            result_dict[address] = result_dict.get(address, 0) + amount
    return result_dict




# print(Node3000.adres)
# print(sum_amounts(utxo_set))

import json
txjson = json.dumps(TRAN_1.to_json(), indent=1)
bG2 = Block(index=0, previous_hash= '5vh21v85232v0P1v08g5081vhh023n2b085', hash = 'h318f3fh98f3h',
            timestamp=datetime.now().timestamp(), data=TRAN_1.to_json() ,nonce=10,difficulty=1)
difi = 2
blockchain2 = []
blockchain2.append(bG2)
# #
# bn2 = generate_next_block(str(TRAN_1.to_json()), blockchain2, difi)
# blockchain2.append(bn2)
# spr = is_valid_chain(blockchain2,bG2)
# print(spr)
# print(bn2.timestamp)
# print(bn2.to_json())
# choose_blockchain_ts(blockchain,blockchain2)
# choose_blockchain_diffi(blockchain,blockchain2)






if __name__ == '__main__':
    port = 1000
    # pub_key, priv_key = rsa.newkeys(1024)
    nazwa_pliku = f"{port}public.pem"
    with open(nazwa_pliku, "rb") as f:
        pub_key = rsa.PublicKey.load_pkcs1(f.read())

    nazwa_pliku1 = f"{port}private.pem"
    with open(nazwa_pliku1, "rb") as f:
        priv_key = rsa.PrivateKey.load_pkcs1(f.read())


    reactor.listenUDP(port, Client('localhost', port, pub_key, priv_key))
    reactor.run()

    
    
    
            
