# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Base de um servidor HTTP (python 3)
#

# importacao das bibliotecas
import socket
import os.path

# definicao do host e da porta do servidor
HOST = '' # ip do servidor (em branco)
PORT = 8080 # porta do servidor

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# permite que seja possivel reusar o endereco e porta do servidor caso seja encerrado incorretamente
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print ('Serving HTTP on port %s ...' % PORT)

while True:
    
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket
    request = client_connection.recv(1024)
    request = request.decode('utf-8')
    # imprime na tela o que o cliente enviou ao servidor
    print ('Request: ',request)

    firstLine = request.split('\r\n')
   
    slised = firstLine[0].split(' ')
    
    method = slised[0]
    way = slised[1]
    version = slised[2]
    
    if(method == "GET" and  way[0] == '/' and  version.split('/')[0] == 'HTTP' and 
    (version.split('/')[1] == '0.9' or version.split('/')[1] == '1.0' or version.split('/')[1] == '1.1')):
        if(way == '/'):
            # abrir aquivo index.html
            index = open('index.html')
            # declaracao da resposta do servidor
            http_response = "HTTP/1.1 200 OK\r\n\r\n" + index.read() +'\r\n'
            # Fecha o arquivo index.html
            index.close()
        elif(way == '/favicon.ico'):
            pass
        elif(os.path.isfile('.' + way) == True):
            # abrir aquivo index.html
            index = open('.' + way)
            # declaracao da resposta do servidor
            http_response = "HTTP/1.1 200 OK\r\n\r\n" + index.read() +'\r\n'
            # Fecha o arquivo index.html
            index.close()
        elif(os.path.isfile('.' + way + 'index.html') == True):
            # abrir aquivo index.html
            index = open('.' + way + 'index.html')
            # declaracao da resposta do servidor
            http_response = "HTTP/1.1 200 OK\r\n\r\n" + index.read() +'\r\n'
            # Fecha o arquivo index.html
            index.close()
        else:
            # abrir aquivo index.html
            index = open('erro404.html')
            # declaracao da resposta do servidor
            http_response = "HTTP/1.1 404 OK\r\n\r\n" + index.read() +'\r\n'
            # Fecha o arquivo index.html
            index.close()
    else:
            # abrir aquivo index.html
            index = open('badResquest.html')
            # declaracao da resposta do servidor
            http_response = "HTTP/1.1 400 OK\r\n\r\n" + index.read() +'\r\n'
            # Fecha o arquivo index.html
            index.close()

    # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
    client_connection.send(http_response.encode('utf-8'))
    # encerra a conexao
    client_connection.close()
    
# encerra o socket do servidor
listen_socket.close()


