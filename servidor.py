import socket
import threading

HOST = 'localhost'
PORT = 55555

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((HOST, PORT))
servidor.listen()

salas = {}
def broadcast(sala, mensagem):
    for i in salas[sala]:
        if isinstance(mensagem, str):
            mensagem = mensagem.encode()

        i.send(mensagem)

def enviar_mensagem(nome, sala, cliente):
    while True:
        mensagem = cliente.recv(1024)
        mensagem = f'{nome}: {mensagem.decode()}\n'
        broadcast(sala, mensagem)

while True:
    cliente, addr = servidor.accept()
    cliente.send('SALA'.encode())
    data = cliente.recv(1024).decode()
    nome, sala = data.split(',')
    if sala not in salas.keys():
        salas[sala] = []
    salas[sala].append(cliente)
    print(f'{nome} se conectou na sala {salas}! INFO {addr}')
    broadcast(sala, f'{nome}: Entrou na sala!\n')
    thread = threading.Thread(target=enviar_mensagem, args=(nome, sala, cliente))
    thread.start()