import socket
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

HOST = 'localhost'
PORT = 8080

while True:
    request = input('>')
    
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    sock.send(request.encode())
    if request == 'exit':
        sock.close()
        break

    response = sock.recv(1024).decode()
    print(response)
