
#!/usr/bin/env python3
"""UDP multiplayer game server with one-way latency measurement."""
import csv
import json
import socket
import time
from pathlib import Path

HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 4096
players = {}
last_seq = {}

SERVER_CSV = Path(__file__).resolve().parent / "latency_server.csv"
SERVER_CSV_FIELDS = [
    "player_id", "seq", "client_send_timestamp_ns",
    "server_receive_timestamp_ns", "one_way_latency_ms"
]


def append_csv(path, fields, row):
    """Append one measurement row, creating the CSV header if needed."""
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        if new_file:
            writer.writeheader()
        writer.writerow(row)


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
    print(f"Server-side latency CSV: {SERVER_CSV}", flush=True)

    try:
        while True:
            raw, address = sock.recvfrom(BUFFER_SIZE)
            # Capture as soon as recvfrom returns, before JSON parsing.
            server_receive_ns = time.time_ns()

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

                seq = msg.get("seq")
                state = msg.get("game_state")
                client_send_ns = msg.get("client_send_timestamp_ns")

                if (not isinstance(seq, int) or isinstance(seq, bool) or seq < 1
                        or not isinstance(state, dict)):
                    send_json(sock, {"type": "error", "message": "Invalid update"}, address)
                    continue

                if seq <= last_seq.get(pid, 0):
                    send_json(sock, {
                        "type": "error",
                        "message": f"Duplicate/out-of-order sequence {seq}",
                        "seq": seq
                    }, address)
                    continue

                # One-way latency estimate. Requires client and server clocks
                # to be synchronized (for example, by NTP/chrony).
                one_way_ms = None
                if isinstance(client_send_ns, int) and not isinstance(client_send_ns, bool):
                    one_way_ms = (server_receive_ns - client_send_ns) / 1_000_000
                    # A negative value indicates clock offset/skew; don't report it as latency.
                    if one_way_ms < 0:
                        one_way_ms = None

                last_seq[pid] = seq
                update = {
                    "type": "update",
                    "player_id": pid,
                    "seq": seq,
                    "game_state": state
                }

                print(
                    f"[UPDATE] {pid} seq={seq} state={state} "
                    f"one_way_latency_ms={one_way_ms if one_way_ms is not None else 'unavailable'}",
                    flush=True
                )

                if one_way_ms is not None:
                    append_csv(SERVER_CSV, SERVER_CSV_FIELDS, {
                        "player_id": pid,
                        "seq": seq,
                        "client_send_timestamp_ns": client_send_ns,
                        "server_receive_timestamp_ns": server_receive_ns,
                        "one_way_latency_ms": f"{one_way_ms:.3f}"
                    })

                # Echo the client's wall-clock timestamp so the client can
                # match this ACK to its pending send and calculate RTT using
                # its own monotonic clock.
                send_json(sock, {
                    "type": "ack",
                    "player_id": pid,
                    "seq": seq,
                    "client_send_timestamp_ns": client_send_ns,
                    "server_receive_timestamp_ns": server_receive_ns,
                    "one_way_latency_ms": one_way_ms
                }, address)

                # Preserve existing multiplayer forwarding behaviour.
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
