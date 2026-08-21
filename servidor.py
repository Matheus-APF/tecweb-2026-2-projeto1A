import socket
from pathlib import Path
from utils import extract_route, read_file, build_response
from views import index

CUR_DIR = Path(__file__).parent
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}') # indenficador da porta

while True:
    client_connection, client_address = server_socket.accept() # abre socket: porta no local host aguardando request

    request = client_connection.recv(1024).decode() # String formato verbo HTTP
    print('*'*100)
    print(request)

    route = extract_route(request) # Extrai rota da URL

    filepath = CUR_DIR / route # Concatenacao do tipo File
    
    if filepath.is_file(): # Verifica se arquivo existe 
        response = build_response() + read_file(filepath) # Monta Response ; Read file entra como Body ; em Byte
    # Caminho Vazio --> Home
    elif route == '':      
        response = index(request)
    # Nao Arquivo / Nao Encontrado
    else:
        response = build_response() # Nao devolve nada

    client_connection.sendall(response) # Envia response montada

    # Aguarda novas requests

server_socket.close() # Fecha a porta e arquivo p/ bugs / ctrl C