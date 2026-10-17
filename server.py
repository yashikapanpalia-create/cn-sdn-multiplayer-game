import socket

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print(f"Game Server started on UDP port {PORT}")
print("Waiting for players...")

players = {}

while True:
    data, address = server.recvfrom(1024)

    message = data.decode()

    print(f"Received from {address}: {message}")

    # Store player address
    if message.startswith("PLAYER"):
        player_id = message.split(",")[0]
        players[player_id] = address

    # Send received game state to all other players
    for player_id, player_address in players.items():
        if player_address != address:
            server.sendto(data, player_address)
