import socket

def register(username, password):
    # Sunucuya "kayıt" talebini gönder
    server_socket.send("kayıt".encode())

    # Kullanıcı adı ve şifreyi sunucuya gönder
    credentials = f"{username}|{password}"
    server_socket.send(credentials.encode())

    # Sunucudan gelen yanıtı al
    response = server_socket.recv(1024).decode()
    print(response)

def login(username, password):
    # Sunucuya "giriş" talebini gönder
    server_socket.send("giriş".encode())

    # Kullanıcı adı ve şifreyi sunucuya gönder
    credentials = f"{username}|{password}"
    server_socket.send(credentials.encode())

    # Sunucudan gelen yanıtı al
    response = server_socket.recv(1024).decode()
    print(response)

# İstemci soketini oluştur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(('localhost', 12345))

while True:
    # Kullanıcıdan kayıt olma veya giriş yapma seçeneğini al
    choice = input("Kayıt olmak için 'kayıt', giriş yapmak için 'giriş', çıkmak için 'çıkış' yazın: ")

    if choice == 'kayıt':
        # Kullanıcıdan kullanıcı adı ve şifreyi al
        username = input("Kullanıcı Adı: ")
        password = input("Şifre: ")

        # Kayıt işlemini gerçekleştir
        register(username, password)
    elif choice == 'giriş':
        # Kullanıcıdan kullanıcı adı ve şifreyi al
        username = input("Kullanıcı Adı: ")
        password = input("Şifre: ")

        # Giriş işlemini gerçekleştir
        login(username, password)
        
        # Giriş yaptıktan sonra menüyü tekrar sorma, döngüyü sonlandır
        break
    elif choice == 'çıkış':
        # Çıkış yap
        break
    else:
        print("Geçersiz seçenek. 'kayıt', 'giriş' veya 'çıkış' yazın.")

def upload_file(file_path, username):
    # Sunucuya dosya yükleme talebini gönder
    server_socket.send("dosya_yükle".encode())

    # Dosyanın adını ve boyutunu sunucuya gönder
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_info = f"{file_name}|{file_size}"
    server_socket.send(file_info.encode())

    # Dosyayı sunucuya gönder
    with open(file_path, 'r') as file:
        file_content = file.read()
        server_socket.send(file_content.encode())

    # Sunucudan gelen yanıtı al
    response = server_socket.recv(1024).decode()
    print(response)

# Bağlantıyı kapat
server_socket.close()
