#!/usr/bin/env python3
"""Interactive UDP multiplayer client."""
import json
import socket
import sys
import threading

PORT = 5000
BUFFER_SIZE = 4096

def receiver(sock, stop):
    while not stop.is_set():
        try:
            raw, _ = sock.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            continue
        except OSError:
            break
        try:
            msg = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            print("[WARN] Invalid JSON received", flush=True)
            continue
        kind = msg.get("type")
        if kind == "registered":
            print("Registration successful!", flush=True)
        elif kind == "ack":
            print(f"ACK received for sequence {msg.get('seq')}", flush=True)
        elif kind == "update":
            print(f"Update from {msg.get('player_id')}: {msg.get('game_state')}", flush=True)
        elif kind == "error":
            print(f"[SERVER ERROR] {msg.get('message')}", flush=True)
        else:
            print(f"[SERVER] {msg}", flush=True)

def parse_state(line):
    parts = line.split()
    if len(parts) != 3:
        raise ValueError("Enter exactly three values: x y score.")
    try:
        x, y, score = (int(v) for v in parts)
    except ValueError as exc:
        raise ValueError("x, y, and score must be integers.") from exc
    return {"x": x, "y": y, "score": score}

def main():
    pid = (sys.argv[1] if len(sys.argv) > 1 else input("Enter player ID (e.g. P1): ")).strip()
    server_ip = (sys.argv[2] if len(sys.argv) > 2 else input("Enter server IP (e.g. 10.0.0.3): ")).strip()
    if not pid or not server_ip:
        print("[ERROR] Player ID and server IP are required.")
        return
    server = (server_ip, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.0)
    stop = threading.Event()
    try:
        threading.Thread(target=receiver, args=(sock, stop), daemon=True).start()
        sock.sendto(json.dumps({"type": "register", "player_id": pid}).encode("utf-8"), server)
        print(f"Registering {pid} with server {server_ip}:{PORT}...", flush=True)
        seq = 0
        while True:
            try:
                line = input("Enter x y score (example: 10 20 0): ")
            except EOFError:
                break
            try:
                state = parse_state(line)
            except ValueError as exc:
                print(str(exc), flush=True)
                continue
            seq += 1
            packet = {"type": "update", "player_id": pid, "seq": seq, "game_state": state}
            try:
                sock.sendto(json.dumps(packet).encode("utf-8"), server)
                print(f"Sent update with sequence number {seq}", flush=True)
            except OSError as exc:
                print(f"[ERROR] Could not send update: {exc}", flush=True)
    except KeyboardInterrupt:
        print("\nClient stopped.", flush=True)
    except OSError as exc:
        print(f"[ERROR] Client socket failed: {exc}", flush=True)
    finally:
        stop.set()
        sock.close()

if __name__ == "__main__":
    main()
