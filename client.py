import socket
import threading
import sys

SERVER = "10.2.123.95"
PORT = 5555

def receive_messages(sock, nickname):
    """Приём сообщений от сервера."""
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break

            if message == "NICK":
                sock.send(nickname.encode('utf-8'))
            else:
                print(f"\r{message}\n{nickname}: ", end="")
        except (socket.error, ConnectionResetError):
            print("\nПотеря соединения с сервером.")
            break
    sock.close()
    sys.exit(0)

def send_messages(sock, nickname):
    """Отправка сообщений на сервер."""
    while True:
        try:
            message = input(f"{nickname}: ")
            if message.lower() == "/exit":
                print("Отключение...")
                sock.close()
                sys.exit(0)

            sock.send(message.encode('utf-8'))
        except (socket.error, BrokenPipeError):
            print("\nНе удалось отправить сообщение.")
            break

def main():
    nickname = input("Ваше имя: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER, PORT))
        print(f"Подключено к {SERVER}:{PORT}")
    except socket.error as e:
        print(f"Ошибка подключения: {e}")
        return

    # Поток для приёма сообщений
    recv_thread = threading.Thread(target=receive_messages, args=(sock, nickname), daemon=True)
    recv_thread.start()

    # Основной поток для отправки
    send_messages(sock, nickname)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nЗавершено пользователем.")
        sys.exit(0)
