import socket
import os
import threading
import urllib.parse
import mimetypes

def serve_directory(client_socket, directory):
    try:
        files = os.listdir(directory)
        file_list = ""
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                file_extension = os.path.splitext(file_path)[1].lower()

                if file_extension in ['.c', '.cpp', '.java', '.py', '.rb', '.js', '.txt']:
                    file_link = f"<a href='view/{urllib.parse.quote(file)}' target='_blank'>{file}</a>"
                    file_list += f"<li class='file code'><i class='fas fa-file-code'></i>{file_link}  <a href='download/{urllib.parse.quote(file)}'><i class='fas fa-download'></i></a> </li>"
                elif file_extension in ['.mp3', '.mp4', '.mkv']:
                    file_link = f"<a href='view/{urllib.parse.quote(file)}' target='_blank'>{file}</a>"
                    file_list += f"<li class='file media'><i class='fas fa-file-media'></i>{file_link} <a href='download/{urllib.parse.quote(file)}'><i class='fas fa-download'></i></a></li>"
                else:
                    file_link = f"<a href='view/{urllib.parse.quote(file)}' target='_blank'>{file}</a>"
                    file_list += f"<li class='file'><i class='fas fa-file'></i>{file_link} <a href='download/{urllib.parse.quote(file)}'><i class='fas fa-download'></i></a></li>"
            elif os.path.isdir(file_path):
                folder_link = f"<a href='{urllib.parse.quote(file)}/'>{file}</a>"
                file_list += f"<li class='folder'><i class='fas fa-folder'></i>{folder_link}</li>" 

        response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        response_content = "<html><head>"
        response_content += "<meta charset='UTF-8'>"
        response_content += "<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'>"
        response_content += "<style>"
        response_content += "body { background: linear-gradient(to bottom right, blue, black); color: #FFFFFF; }"
        response_content += ".navbar { display: flex; justify-content: space-between; align-items: center; background-color: #212121; padding: 10px; }"
        response_content += ".navbar .left-items { display: flex; align-items: center; }"
        response_content += ".navbar .left-items a { color: #FFFFFF; margin-right: 10px; text-decoration: none; }"
        response_content += ".navbar .left-items a:first-child { margin-right: auto; font-size: 24px; }"
        response_content += ".navbar .left-items a:hover { color: #FFC107; }"
        response_content += ".navbar .right-items { display: flex; align-items: center; }"
        response_content += ".navbar .right-items a { color: #FFFFFF; margin-right: 10px; text-decoration: none; }"
        response_content += ".navbar .right-items a:hover { color: #FFC107; }"
        response_content += ".navbar .search-form { display: flex; align-items: center; margin-left: auto; margin-right: auto; }"
        response_content += ".navbar .search-form input[type='text'] { padding: 8px; border-radius: 5px; border: none; }"
        response_content += ".navbar .search-form button { background-color: transparent; border: none; color: #FFFFFF; padding: 5px; margin-left: 5px; }"
        response_content += ".navbar .search-form button:hover { color: #FFC107; }"
        response_content += ".container { max-width: 800px; margin: 50px auto; background-color: #212121; border-radius: 5px; padding: 20px; }"
        response_content += ".container ul { list-style: none; padding: 0; }"
        response_content += ".container .file { display: flex; align-items: center; margin-bottom: 10px; }"
        response_content += ".container .file i { margin-right: 10px; }"
        response_content += ".container .file a { color: #FFFFFF; text-decoration: none; }"
        response_content += ".container .file a:hover { color: #FFC107; }"
        response_content += ".container .folder { display: flex; align-items: center; margin-bottom: 10px; }"
        response_content += ".container .folder i { margin-right: 10px; }"
        response_content += ".container .folder a { color: #FFFFFF; text-decoration: none; }"
        response_content += ".container .folder a:hover { color: #FFC107; }"
        response_content += "</style>"
        response_content += "</head><body>"
        response_content += "<div class='navbar'>"
        response_content += "<div class='left-items'>"
        response_content += "<a href='/'>SERVESID</a>"
        response_content += "</div>"
        response_content += "<div class='right-items'>"
        response_content += "<form class='search-form' method='GET' action='/search'>"
        response_content += "<input type='text' name='q' placeholder='Search...'>"
        response_content += "<button type='submit'><i class='fas fa-search'></i></button>"
        response_content += "<a href='/header'>HEADER</a>"
        response_content += "<a href='/'>HOME</a>"
        response_content += "</form>"
        response_content += "</div>"
        response_content += "</div>"
        response_content += "<div class='container'>"
        response_content += "<ul>"
        response_content += file_list
        response_content += "</ul>"
        response_content += "</div>"
        response_content += "</body></html>"

        response = response_headers + response_content

        client_socket.send(response.encode())
    except OSError:
        response_headers = "HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        response_content = "<html><body><h1>500 Internal Server Error</h1><p>An error occurred while serving the directory.</p></body></html>"
        response = response_headers + response_content

        client_socket.send(response.encode())
    finally:
        client_socket.close()

def handle_request(client_socket, root_directory):
    request = client_socket.recv(1024).decode()
    request_lines = request.split('\r\n')

    # Lendo a primeira linha da requisição
    request_line = request_lines[0]

    # Dividindo a linha do cabeçalho em partes
    request_parts = request_line.split(' ')

    # Verificando o método HTTP e o caminho da requisição
    if len(request_parts) > 1 and request_parts[0] == 'GET':
        request_path = request_parts[1][1:]

        if request_path == '':
            serve_directory(client_socket, root_directory)
        elif request_path == 'header':
            response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"

            # Obtendo os cabeçalhos da requisição
            headers = "\n".join(request_lines[1:])  # Concatena todos os cabeçalhos, exceto o primeiro (linha de requisição)

            # Enviando os cabeçalhos na resposta
            response = response_headers + headers
            client_socket.send(response.encode())
        elif request_path.startswith("view/"):
            file_name = request_path.split("/")[1]
            file_path = os.path.join(root_directory, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    mime_type, _ = mimetypes.guess_type(file_path)
                    if mime_type and mime_type.startswith("text/"):
                        response_headers = "HTTP/1.1 200 OK\r\nContent-Type: {}\r\n\r\n".format(mime_type)
                        client_socket.send(response_headers.encode())
                        content = file.read()
                        client_socket.send(content)
                    else:
                        response_headers = "HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Disposition: inline; filename={}\r\n\r\n".format(file_name)
                        client_socket.send(response_headers.encode())
                        content = file.read()
                        client_socket.send(content)
            else:
                response_headers = "HTTP/1.1 404 Not Found\r\n\r\n"
                client_socket.send(response_headers.encode())
                client_socket.send("Recurso não encontrado.".encode())
        elif request_path.startswith("download/"):
            file_name = request_path.split("/")[1]
            file_path = os.path.join(root_directory, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    content = file.read()
                response_headers = "HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Disposition: attachment; filename={}\r\n\r\n".format(file_name)
                client_socket.send(response_headers.encode())
                client_socket.send(content)
            else:
                response_headers = "HTTP/1.1 404 Not Found\r\n\r\n"
                client_socket.send(response_headers.encode())
                client_socket.send("Recurso não encontrado.".encode())
        else:
            file_path = os.path.join(root_directory, request_path)
            if os.path.isdir(file_path):
                serve_directory(client_socket, file_path)
            else:
                response_headers = "HTTP/1.1 404 Not Found\r\n\r\n"
                client_socket.send(response_headers.encode())
                client_socket.send("Recurso não encontrado.".encode())
    else:
        response_headers = "HTTP/1.1 400 Bad Request\r\n\r\n"
        client_socket.send(response_headers.encode())
        client_socket.send("Requisição inválida.".encode())

    
def start_server(host, port, directory):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor escutando em {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexão estabelecida com {client_address}.")
        thread = threading.Thread(target=handle_request, args=(client_socket, directory))
        thread.start()

if __name__ == '__main__':
    host = '172.18.133.207'
    port = 8000
    directory = 'arquivos'

    start_server(host, port, directory)
