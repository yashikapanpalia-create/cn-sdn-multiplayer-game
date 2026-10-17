import socket
import threading
import time

SERVER_IP = "10.0.0.3"
SERVER_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sequence = 0


def receive_messages():
    while True:
        try:
            data, address = sock.recvfrom(1024)
            print(f"\n[Received] {data.decode()}")
        except:
            break


threading.Thread(target=receive_messages, daemon=True).start()

print("Player 2 started")
print("Sending game state to server...")

while True:
    sequence += 1

    message = f"PLAYER2,SEQ={sequence},X=50,Y={sequence * 10}"

    sock.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    print(f"[Sent] {message}")

    time.sleep(2)
