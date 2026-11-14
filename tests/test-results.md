# Integration and Test Results

## 1. Test Environment

- Network: Mininet
- Controller: OS-Ken
- Switch: Open vSwitch (OpenFlow 1.3)
- Protocol: UDP
- Application port: 5000
- Player 1: h1 (10.0.0.1)
- Player 2: h2 (10.0.0.2)
- Game server: h3 (10.0.0.3)

## 2. Functional Testing

| Test | Result |
|---|---|
| Network topology initialization | Successful |
| Host connectivity using `pingall` | 0% packet loss |
| SDN controller connection | Verified |
| Player registration | Successful |
| Game-state transmission | Successful |
| Server acknowledgements | Received |
| Player-to-player update forwarding | Verified |
| Sequence number handling | Implemented |

## 3. Performance Testing

| Measurement | Result |
|---|---|
| Average one-way latency – Player 1 | 16.525 ms |
| Average one-way latency – Player 2 | 19.498 ms |
| Average RTT – Player 1 | 39.200 ms |
| Average RTT – Player 2 | 56.700 ms |
| Average jitter – Player 1 | 0.647 ms |
| Average jitter – Player 2 | 3.149 ms |

*Normal-condition latency and jitter values are based on four samples per player.*

## 4. Congestion Testing

The server-facing link was configured at 2 Mbps. Two simultaneous UDP streams generated an aggregate offered load of 3 Mbps for 60 seconds.

| Metric | Player 1 (h1 → h3) | Player 2 (h2 → h3) |
|---|---:|---:|
| Received bandwidth | 1.13 Mbps | 0.793 Mbps |
| Jitter | 3.018 ms | 2.748 ms |
| Packet loss | 17% | 42% |

Traffic-control statistics:

- Dropped packets: 7,657
- Overlimits: 20,914
- Requeues: 0

Game-state messages continued to appear in the application logs during the observed congested run.

*Congestion measurements represent one test run and may vary across repetitions.*

## 5. Conclusion

Testing demonstrated successful multiplayer communication over the SDN-controlled network. Performance measurements showed the effects of congestion on bandwidth, jitter and packet delivery. The application also continued exchanging game-state messages during the observed congestion experiment.
