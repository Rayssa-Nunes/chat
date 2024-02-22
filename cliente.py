import socket 
import threading
from tkinter import simpledialog, Tk, Text, Entry, Button


class Chat:
    def __init__(self):
        HOST = '127.0.0.1'
        PORT = 55555
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((HOST, PORT))

        login = Tk()
        login.withdraw()

        self.janela_carregada = False
        self.ativo = True

        self.nome = simpledialog.askstring('Nome', 'Digite seu nome:', parent=login)
        self.sala = simpledialog.askstring('Nome', 'Digite seu nome:', parent=login)

        thread = threading.Thread(target=self.conecta, daemon=True)
        thread.start()
        self.janela()

    def janela(self):
        self.root = Tk()
        self.root.geometry('800x800')
        self.root.title('Chat')

        self.caixa_texto = Text(self.root)
        self.caixa_texto.place(relx=0.05, rely=0.01, width=700, height=600)

        self.envia_mensagem = Entry(self.root)
        self.envia_mensagem.place(relx=0.05, rely=0.8, width=500, height=30)

        self.btn_enviar = Button(self.root, text='Enviar', command=self.enviar_mensagem)
        self.btn_enviar.place(relx=0.7, rely=0.8, width=100, height=30)
        self.root.protocol('WM_DELETE_WINDOW', self.fechar)

        self.root.mainloop()
    
    def fechar(self):
        self.ativo = False
        self.root.destroy()
        self.cliente.close()

    def conecta(self):
        while self.ativo:
            recebido = self.cliente.recv(1024)
            if recebido == 'SALA'.encode():
                self.cliente.send(f'{self.nome}, {self.sala}'.encode())
            else:
                try:
                    self.caixa_texto.insert('end', recebido.decode())
                except:
                    pass

    def enviar_mensagem(self):
        messagem = self.envia_mensagem.get()
        self.cliente.send(messagem.encode())

chat = Chat()