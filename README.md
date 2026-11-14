# SDN-Based UDP Multiplayer Game with Latency, Jitter and Congestion Analysis

## 1. Project Overview

This project implements a UDP-based multiplayer game communication system using Software-Defined Networking (SDN) and Mininet.

Two players communicate with a central game server through an SDN-controlled network. The application supports player registration, game-state updates, acknowledgements and player-to-player update forwarding.

The project also evaluates network performance by measuring latency, Round-Trip Time (RTT), jitter and packet loss under normal and congested network conditions.

## 2. Objectives

- Implement a UDP-based multiplayer client-server application.
- Establish communication between multiple players and a central server.
- Configure a custom Mininet topology using traffic-controlled links.
- Use an SDN controller to manage network forwarding.
- Measure application-level latency and RTT.
- Analyse jitter in communication between players and the server.
- Generate network congestion and observe its effect on performance.
- Compare network behaviour under normal and congested conditions.

## 3. System Architecture

The system consists of three Mininet hosts connected to an OpenFlow switch:

- **h1:** Player 1
- **h2:** Player 2
- **h3:** Central game server
- **s1:** OpenFlow switch
- **Controller:** OS-Ken SDN controller

Both players communicate with the server using UDP on port 5000.

The server processes incoming game-state updates, acknowledges messages and forwards updates to the other player.

## 4. Network Topology

The project uses a custom Mininet topology implemented using `TCLink`.

| Link | Bandwidth | Delay |
|---|---:|---:|
| h1 – s1 | 10 Mbps | 5 ms |
| h2 – s1 | 10 Mbps | 5 ms |
| h3 – s1 | 2 Mbps | 10 ms |

The server link has a lower bandwidth, creating a bottleneck when traffic exceeds its capacity.

All hosts belong to the `10.0.0.0/24` network.

## 5. Technologies Used

- Python 3
- UDP sockets
- Mininet
- Open vSwitch
- OpenFlow 1.3
- OS-Ken SDN controller
- Linux traffic control (`TCLink`)
- iperf3
- CSV-based data logging

## 6. UDP Multiplayer Application

The application consists of a client and a central server.

### Client

Each player client:

- Connects to the server using UDP.
- Registers itself with a player ID.
- Sends game-state updates with sequence numbers.
- Records the time at which updates are sent.
- Receives acknowledgements from the server.
- Calculates RTT using the send and acknowledgement timestamps.
- Stores latency measurements in a CSV file.

### Server

The server:

- Receives player registration messages.
- Maintains information about connected players.
- Receives and processes game-state updates.
- Tracks sequence numbers to identify duplicate or out-of-order updates.
- Sends acknowledgements to clients.
- Forwards received updates to the other player.
- Records server-side timestamps and latency information.

## 7. Latency and RTT Measurement

Latency and RTT are measured during application communication.

**One-way latency:**

The time difference between the client sending an update and the server receiving it.

**Round-Trip Time (RTT):**

The time between sending an update and receiving its acknowledgement.

RTT is calculated using the client's local monotonic clock, avoiding the need for synchronized clocks.

One-way latency uses timestamps from the client and server. Accurate one-way measurements therefore require synchronized clocks across the hosts.

The application generates the following CSV files during execution:

- `latency_P1.csv` – Player 1 measurements
- `latency_P2.csv` – Player 2 measurements
- `latency_server.csv` – Server-side measurements

These files are generated inside the `app/` directory when the application records measurements. They do not need to be created manually.

## 8. Jitter Measurement

Jitter represents the variation in packet delay over time.

For consecutive latency measurements, jitter is calculated as:

$$
J_i = |L_i - L_{i-1}|
$$

where:

- \(L_i\) is the current latency measurement.
- \(L_{i-1}\) is the previous latency measurement.

Average jitter is calculated as:

$$
J_{\text{avg}} =
\frac{\sum_{i=2}^{n}|L_i-L_{i-1}|}{n-1}
$$

Jitter is calculated from consecutive one-way latency measurements for each player.

## 9. Congestion Testing

Network congestion is introduced using UDP traffic generated with iperf3.

Two background traffic streams are configured:

| Traffic source | Destination | Offered rate |
|---|---|---:|
| h1 | h3 | 1.5 Mbps |
| h2 | h3 | 1.5 Mbps |

The combined offered traffic is 3 Mbps, which exceeds the server link capacity of 2 Mbps.

The congestion experiment runs for 60 seconds.

During the experiment, the following are observed:

- UDP packet loss
- Bandwidth received
- Traffic-control queue statistics
- Multiplayer application communication

The `congestion_test.py` script provides functions to start, display and stop the background congestion traffic.

### Running the Congestion Test

After starting Mininet, execute the following commands in the **Mininet CLI**:

```python
py from congestion_test import start_congestion, show_congestion_output, stop_congestion
```

Start the congestion traffic:

```python
py start_congestion(net)
```

Display the iperf3 results and congestion statistics:

```python
py show_congestion_output(net)
```

Stop the background congestion traffic:

```python
py stop_congestion(net)
```

Run these commands in the given order. The congestion traffic runs for the configured 60-second experiment.

## 10. Experimental Results

### Normal Network Conditions

- All Mininet hosts communicated successfully.
- `pingall` reported 0% packet loss.
- Both players registered successfully with the server.
- Game-state updates were exchanged between the players.
- Acknowledgements were received successfully.
- Latency, RTT and jitter measurements were recorded.

### Congested Network Conditions

The following results were observed during the congestion experiment:

| Metric | Player 1 traffic | Player 2 traffic |
|---|---:|---:|
| Received bandwidth | 0.732 Mbps | 1.13 Mbps |
| Packet loss | 47% | 18% |

### Bottleneck Link Statistics

The traffic-control statistics for the server-facing link showed:

- Dropped packets: 7,657
- Overlimits: 20,914
- Requeues: 0

Game-state messages continued to appear in the application logs during the observed congested run.

### Application-Level Latency Measurements

The following are the average values calculated from the recorded normal-condition samples:

| Metric | Player 1 | Player 2 |
|---|---:|---:|
| Average one-way latency | 16.525 ms | 19.498 ms |
| Average RTT | 39.200 ms | 56.700 ms |
| Average jitter | 0.647 ms | 3.149 ms |

The normal-condition averages are based on four samples per player. Congested application-level measurements were limited, with available observations around 5.96 seconds. These should be treated as observations rather than statistically conclusive averages.

## 11. Evidence

The `evidence/` directory contains screenshots and a live test report demonstrating:

- Player registration and communication
- SDN controller connection and flow installation
- Communication during congestion
- iperf3 bandwidth and packet-loss results
- Mininet host connectivity using `pingall`
- Traffic-control statistics

Refer to `evidence/README.md` for the evidence list and `evidence/LIVE_TEST_REPORT.md` for the live communication test report.

## 12. How to Run the Project

### Requirements

The project requires:

- Ubuntu
- Python 3
- Mininet
- Open vSwitch
- OS-Ken
- iperf3

### Start the SDN Controller

From the project directory, run:

```bash
~/osken-venv/bin/python -c "from os_ken.base import app_manager; app_manager.AppManager.run_apps(['controller'])"
```

### Start Mininet

Open another terminal in the project directory:

```bash
sudo mn --custom topology.py --topo gamenet --controller=remote,ip=127.0.0.1,port=6653 --switch ovs,protocols=OpenFlow13
```

### Test Network Connectivity

From the Mininet CLI:

```bash
pingall
```

### Start the Game Server

From the Mininet CLI:

```bash
h3 python3 -u app/server.py
```

### Start Player 1

Open another Mininet CLI terminal or use the Mininet CLI to run:

```bash
h1 python3 -u app/client.py P1 10.0.0.3
```

### Start Player 2

```bash
h2 python3 -u app/client.py P2 10.0.0.3
```

Enter the game-state values in the format:

```text
x y score
```

For example:

```text
10 20 0
```

## 13. Repository Structure

```text
cn-sdn-multiplayer-game/
│
├── README.md
├── .gitignore
├── controller.py
├── topology.py
├── congestion_test.py
│
├── app/
│   ├── client.py
│   └── server.py
│
├── tests/
│   └── test-results.md
│
└── evidence/
    ├── README.md
    ├── LIVE_TEST_REPORT.md
    ├── Player communication (P1 and P2).png
    ├── SDN controller (flow installation).png
    ├── congestion_communication.png
    ├── iperf_player1.png
    ├── iperf_player2.png
    ├── pingall.png
    └── tc_statistics.png
```

## 14. Conclusion

The project demonstrates a UDP-based multiplayer communication system operating over an SDN-controlled Mininet network.

The application supports player registration, game-state exchange, acknowledgement handling and player-to-player update forwarding.

Performance measurements under normal and congested conditions demonstrate how bandwidth limitations and competing traffic affect latency, jitter, packet loss and communication performance.

The experiments highlight the importance of network performance analysis when designing real-time multiplayer applications.
