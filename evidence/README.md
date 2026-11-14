# Network and Application Test Evidence

This folder contains screenshots from the SDN-based UDP multiplayer game experiments.

## Existing screenshots

- **Player communication (P1 and P2):** Player registration, game-state updates, acknowledgements and communication between both players.
- **SDN controller (flow installation):** Switch connection and OpenFlow flow installation.

## Additional experiment evidence identified

The submitted `cn evidence.docx` contains these screenshots:

| Evidence | Source location | What it demonstrates |
|---|---|---|
| Mininet connectivity | Page 1, top | `pingall`: 0% packet loss (6/6 received). |
| Normal communication | Page 1, middle and bottom; page 2, top | Registration and normal player updates/ACKs. |
| Congestion setup | Page 2 | Two 1.5 Mbps UDP streams (3 Mbps aggregate) against a 2 Mbps server-facing bottleneck. |
| Communication during congestion | Pages 2–3 | Server receives updates; clients show ACK, latency and RTT measurements. |
| Player 1 iperf3 | Page 4 | Receiver: 1.13 Mbps, 3.018 ms jitter, 17% packet loss. |
| Player 2 iperf3 | Page 5, top | Receiver: approximately 793 Kbps, 2.748 ms jitter, 42% packet loss. |
| Traffic-control statistics | Page 5, bottom | `s1-eth3`: 4,586 dropped packets, 10,957 overlimits, 0 requeues. |

**Note:** These additional screenshots are documented from the submitted Word evidence file, but are not yet stored as individual image files in this repository. Page references identify the correct screenshots for upload.

## Measurement distinction

iperf3 jitter is a network-level measurement. Jitter calculated from application one-way latency samples is a separate application-level measurement; do not combine the two.
