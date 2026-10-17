#!/usr/bin/env python3
"""UDP multiplayer game server."""
import json
import socket

HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 4096
players = {}
last_seq = {}

def send_json(sock, data, address):
    try:
        sock.sendto(json.dumps(data).encode("utf-8"), address)
    except OSError as exc:
        print(f"[WARN] Send to {address} failed: {exc}", flush=True)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((HOST, PORT))
    except OSError as exc:
        print(f"[ERROR] Cannot bind UDP {HOST}:{PORT}: {exc}")
        sock.close()
        return
    print(f"Game server running on UDP port {PORT}...", flush=True)
    try:
        while True:
            raw, address = sock.recvfrom(BUFFER_SIZE)
            try:
                msg = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                send_json(sock, {"type": "error", "message": "Invalid JSON"}, address)
                continue
            if not isinstance(msg, dict):
                send_json(sock, {"type": "error", "message": "Expected JSON object"}, address)
                continue
            kind = msg.get("type")
            pid = str(msg.get("player_id", "")).strip()
            if kind == "register":
                if not pid:
                    send_json(sock, {"type": "error", "message": "player_id required"}, address)
                    continue
                players[pid] = address
                last_seq.setdefault(pid, 0)
                print(f"[REGISTER] {pid} from {address}", flush=True)
                send_json(sock, {"type": "registered", "player_id": pid}, address)
            elif kind == "update":
                if not pid or pid not in players:
                    send_json(sock, {"type": "error", "message": "Register before updating"}, address)
                    continue
                seq, state = msg.get("seq"), msg.get("game_state")
                if not isinstance(seq, int) or seq < 1 or not isinstance(state, dict):
                    send_json(sock, {"type": "error", "message": "Invalid update"}, address)
                    continue
                if seq <= last_seq.get(pid, 0):
                    send_json(sock, {"type": "error", "message": f"Duplicate/out-of-order sequence {seq}", "seq": seq}, address)
                    continue
                last_seq[pid] = seq
                update = {"type": "update", "player_id": pid, "seq": seq, "game_state": state}
                print(f"[UPDATE] {pid} seq={seq} state={state}", flush=True)
                send_json(sock, {"type": "ack", "player_id": pid, "seq": seq}, address)
                for other_id, other_address in list(players.items()):
                    if other_id != pid:
                        send_json(sock, update, other_address)
            else:
                send_json(sock, {"type": "error", "message": "Unknown message type"}, address)
    except KeyboardInterrupt:
        print("\nStopping game server...", flush=True)
    except OSError as exc:
        print(f"[ERROR] Server socket failed: {exc}", flush=True)
    finally:
        sock.close()

if __name__ == "__main__":
    main()
