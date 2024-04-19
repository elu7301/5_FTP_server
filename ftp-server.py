import socket
import os
import shutil
'''
Посмотреть название рабочей директории - pwd
Посмотреть содержимое папки - ls
Создать папку - mkdir <dirname>
Удалить папку - deldir <dirname>
Удалить файл -  rm <filename>
Переименовать файл - mv <oldname> <newname>
Скопировать файл с клиента на сервер - clienttoserver <filename> <content>
Скопировать файл с сервера на клиент - servertoclient <filename>
Выход (отключение клиента от сервера) - exit
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
    if req == 'pwd':
        return dirname

    elif req == 'ls':
        return '; '.join(os.listdir(dirname))

    elif req.startswith('mkdir'):
        dir_name = req.split()[1]
        os.mkdir(os.path.join(dirname, dir_name))
        return f"Directory {dir_name} created successfully."

    elif req.startswith('deldir'):
        dir_name = req.split()[1]
        shutil.rmtree(os.path.join(dirname, dir_name))
        return f"Directory {dir_name} deleted successfully."

    elif req.startswith('rm'):
        file_name = req.split()[1]
        os.remove(os.path.join(dirname, file_name))
        return f"File {file_name} deleted successfully."

    elif req.startswith('mv'):
        old_name, new_name = req.split()[1:]
        os.rename(os.path.join(dirname, old_name), os.path.join(dirname, new_name))
        return f"File {old_name} renamed to {new_name} successfully."

    elif req.startswith('clienttoserver'):
        _, file_name, content = req.split(maxsplit=2)
        file_path = os.path.join(dirname, file_name)
        with open(file_path, 'w') as f:
            f.write(content)
        return f"File {file_name} created on server."

    elif req.startswith('servertoclient'):
        file_name = req.split()[1]
        file_path = os.path.join(dirname, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                file_content = f.read()
            conn.send(file_content)
            return f"File {file_name} sent to client successfully."
        else:
            return f"File {file_name} does not exist on the server."

    elif req == 'exit':
        return 'exit'

    return 'bad request'


PORT = 8080

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Listening on port", PORT)

while True:
    conn, addr = sock.accept()

    request = conn.recv(1024).decode()
    print(request)

    response = process(request)
    if response == 'exit':
        conn.close()
        break
    conn.send(response.encode())

conn.close()
