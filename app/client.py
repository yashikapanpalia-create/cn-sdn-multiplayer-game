
#!/usr/bin/env python3
"""Interactive UDP multiplayer client with RTT and latency measurements."""
import csv
import json
import socket
import sys
import threading
import time
from pathlib import Path

PORT = 5000
BUFFER_SIZE = 4096
CSV_FIELDS = [
    "player_id", "seq", "client_send_timestamp_ns",
    "server_receive_timestamp_ns", "one_way_latency_ms", "rtt_ms"
]


def append_measurement(path, row, lock):
    with lock:
        new_file = not path.exists()
        with path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
            if new_file:
                writer.writeheader()
            writer.writerow(row)


def print_summary(measurements):
    values = [m["rtt_ms"] for m in measurements if m["rtt_ms"] is not None]
    if not values:
        print("[LATENCY] No RTT samples recorded yet.", flush=True)
        return
    print(
        f"[RTT SUMMARY] samples={len(values)} "
        f"avg={sum(values) / len(values):.3f} ms "
        f"min={min(values):.3f} ms max={max(values):.3f} ms",
        flush=True
    )


def receiver(sock, stop, pending, pending_lock, measurements,
             measurements_lock, csv_path, csv_lock, pid):
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
            seq = msg.get("seq")
            # RTT uses monotonic time at both ends of the measurement on
            # this client, so it is not affected by clock synchronization.
            with pending_lock:
                sent = pending.pop(seq, None)

            if sent is not None:
                rtt_ms = (time.monotonic_ns() - sent["monotonic_ns"]) / 1_000_000
                one_way_ms = msg.get("one_way_latency_ms")
                server_receive_ns = msg.get("server_receive_timestamp_ns")
                row = {
                    "player_id": pid,
                    "seq": seq,
                    "client_send_timestamp_ns": sent["wall_ns"],
                    "server_receive_timestamp_ns": server_receive_ns,
                    "one_way_latency_ms": (
                        f"{one_way_ms:.3f}"
                        if isinstance(one_way_ms, (int, float)) else ""
                    ),
                    "rtt_ms": f"{rtt_ms:.3f}"
                }
                append_measurement(csv_path, row, csv_lock)

                with measurements_lock:
                    measurements.append({"seq": seq, "rtt_ms": rtt_ms})

                one_way_display = (
                    f"{one_way_ms:.3f} ms"
                    if isinstance(one_way_ms, (int, float))
                    else "unavailable (sync clocks)"
                )
                print(
                    f"[ACK] seq={seq} | one-way≈{one_way_display} "
                    f"| RTT={rtt_ms:.3f} ms",
                    flush=True
                )
                with measurements_lock:
                    print_summary(measurements)
            else:
                print(f"ACK received for sequence {seq} (no pending send timestamp)", flush=True)

        elif kind == "update":
            print(
                f"Update from {msg.get('player_id')} "
                f"(seq={msg.get('seq')}): {msg.get('game_state')}",
                flush=True
            )
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
    pending = {}
    pending_lock = threading.Lock()
    measurements = []
    measurements_lock = threading.Lock()
    csv_lock = threading.Lock()
    csv_path = Path(__file__).resolve().parent / f"latency_{pid}.csv"

    try:
        threading.Thread(
            target=receiver,
            args=(sock, stop, pending, pending_lock, measurements,
                  measurements_lock, csv_path, csv_lock, pid),
            daemon=True
        ).start()

        sock.sendto(
            json.dumps({"type": "register", "player_id": pid}).encode("utf-8"),
            server
        )
        print(f"Registering {pid} with server {server_ip}:{PORT}...", flush=True)
        print(f"Client measurement CSV: {csv_path}", flush=True)

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
            # Wall clock is used only for cross-host one-way latency.
            client_send_wall_ns = time.time_ns()
            # Monotonic clock is used for accurate same-client RTT.
            client_send_monotonic_ns = time.monotonic_ns()

            packet = {
                "type": "update",
                "player_id": pid,
                "seq": seq,
                "game_state": state,
                "client_send_timestamp_ns": client_send_wall_ns
            }

            with pending_lock:
                pending[seq] = {
                    "wall_ns": client_send_wall_ns,
                    "monotonic_ns": client_send_monotonic_ns
                }

            try:
                sock.sendto(json.dumps(packet).encode("utf-8"), server)
                print(f"Sent update with sequence number {seq}", flush=True)
            except OSError as exc:
                with pending_lock:
                    pending.pop(seq, None)
                print(f"[ERROR] Could not send update: {exc}", flush=True)

    except KeyboardInterrupt:
        print("\nClient stopped.", flush=True)
    except OSError as exc:
        print(f"[ERROR] Client socket failed: {exc}", flush=True)
    finally:
        stop.set()
        sock.close()
        with measurements_lock:
            print_summary(measurements)
        print(f"Measurements saved to: {csv_path}", flush=True)


if __name__ == "__main__":
    main()
