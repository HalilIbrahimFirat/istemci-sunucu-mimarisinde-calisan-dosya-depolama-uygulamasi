import socket
import os


def check_user_existence(username):
    # Metin dosyasından kullanıcı adını kontrol et
    with open('user_credentials.txt', 'r') as file:
        for line in file:
            stored_username, _ = line.strip().split('|')
            if stored_username == username:
                return True
    return False

def handle_registration(client_socket):
    # İstemciden kullanıcı adı ve şifreyi al
    credentials = client_socket.recv(1024).decode().split('|')

    if len(credentials) == 2:
        username, password = credentials
        # Kullanıcı adının daha önce kullanılıp kullanılmadığını kontrol et
        if not check_user_existence(username):
            # Kullanıcı adıyla yeni bir klasör oluştur
            user_folder = os.path.join(os.getcwd(), username)
            os.makedirs(user_folder, exist_ok=True)

            # Kullanıcı bilgilerini metin dosyasına kaydet
            with open('user_credentials.txt', 'a') as file:
                file.write(f"{username}|{password}\n")

            # Başarılı kayıt mesajını gönder
            client_socket.send("Kayıt başarılı".encode())
        else:
            # Kullanıcı adı daha önce kullanılmışsa hata mesajı gönder
            client_socket.send("Bu kullanıcı adı zaten kullanımda".encode())

def handle_login(client_socket):
    # İstemciden kullanıcı adı ve şifreyi al
    credentials = client_socket.recv(1024).decode().split('|')

    if len(credentials) == 2:
        username, password = credentials
        # Kullanıcı adının ve şifrenin doğruluğunu kontrol et
        if check_user_existence(username):
            with open('user_credentials.txt', 'r') as file:
                for line in file:
                    stored_username, stored_password = line.strip().split('|')
                    if stored_username == username and stored_password == password:
                        client_socket.send("Giriş başarılı".encode())
                        return
            # Kullanıcı adı doğru ancak şifre yanlışsa hata mesajı gönder
            client_socket.send("Hatalı şifre".encode())
        else:
            # Kullanıcı adı metin dosyasında bulunmuyorsa hata mesajı gönder
            client_socket.send("Bu kullanıcı adı mevcut değil".encode())

def handle_file_upload(client_socket, username):
    # Sunucu, dosya yükleme talebini bekler
    request = client_socket.recv(1024).decode()

    if request == "dosya_yükle":
        # Sunucu, dosya adını ve boyutunu bekler
        file_info = client_socket.recv(1024).decode().split('|')

        if len(file_info) == 2:
            file_name, file_size = file_info
            file_size = int(file_size)

            # Sunucu, dosyayı alır
            file_content = client_socket.recv(file_size).decode()

            # Dosyayı kullanıcının klasörüne kaydet
            user_folder = os.path.join(os.getcwd(), username)
            file_path = os.path.join(user_folder, file_name)

            with open(file_path, 'w') as file:
                file.write(file_content)

            # Başarılı yükleme mesajını gönder
            client_socket.send("Dosya başarıyla yüklendi".encode())



# Sunucu soketini oluştur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

print("Sunucu başlatıldı. İstemci bekleniyor...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Bağlantı kabul edildi: {client_address}")

    # İstemci talebini al ve kayıt olma veya giriş yapma işlemini gerçekleştir
    request = client_socket.recv(1024).decode()
    if request == "kayıt":
        handle_registration(client_socket)
    elif request == "giriş":
        handle_login(client_socket)

    # Bağlantıyı kapatma işlemini bu while döngüsü içinde yapma
    client_socket.close()
