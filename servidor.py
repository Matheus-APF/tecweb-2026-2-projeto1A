# START
import socket
from pathlib import Path
from utils import extract_route, read_file, build_response
from views import index, edit, notfound, delete
CUR_DIR = Path(__file__).parent
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()
print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}') # indenficador da porta

# LOOP WAIT REQUEST
while True:
    # Conexao
    client_connection, client_address = server_socket.accept() # abre socket: porta no local host aguardando request

    # Trata String Requisicao
    request = client_connection.recv(4096).decode() # String formato verbo HTTP # 1024 4096
    print('*'*100)
    print(request)
    route = extract_route(request) # Extrai rota da URL
    filepath = CUR_DIR / route # Concatenacao do tipo File

    # Direcionamento

    # Aruivo Existe
    print(route, "  AAAAAAAAAAAAAAAAAa")
    if filepath.is_file():  
        response = build_response() + read_file(filepath) # Monta Response ; Read file entra como Body ; em Byte

    # Caminho Vazio --> Home
    elif route == '':      
        response = index(request)

    # Rota Editação
    elif route.startswith('edit/'):
        id_note = int(route.split('/')[1])
        response = edit(request, id_note)

    # Rota Exclusão
    elif route.startswith('delete/'):
        id_note = int(route.split('/')[1])
        response = delete(request, id_note)

    # Nao Arquivo / Nao Encontrado
    else:
        response = notfound()

    client_connection.sendall(response) # Envia response montada

    # Aguarda novas requests

# Fecha
server_socket.close()