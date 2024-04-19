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
Скопировать файл с клиента на сервер - clienttoserver <filename>
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
        file_name = req.split()[1]
        with open(os.path.join(dirname, file_name), 'wb') as f:
            data = conn.recv(1024)
            while data:
                f.write(data)
                data = conn.recv(1024)
        return f"File {file_name} copied from client successfully."
    elif req.startswith('servertoclient'):
        file_name = req.split()[1]
        with open(os.path.join(dirname, file_name), 'rb') as f:
            data = f.read(1024)
            while data:
                conn.send(data)
                data = f.read(1024)
        return f"File {file_name} copied to client successfully."
    elif req == 'exit':
        return 'exit'

    return 'bad request'


PORT = 8080

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

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
