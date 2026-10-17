# D1 Integration Test Results

## Test Environment
- Network: Mininet
- Transport protocol: UDP
- UDP port: 5000
- Player 1: h1 (10.0.0.1)
- Player 2: h2 (10.0.0.2)
- Game server: h3 (10.0.0.3)
- SDN switch: s1
- Controller: OS-Ken

## Test Cases

| Test case | Expected result | Observed result |
|---|---|---|
| Player 1 registration | P1 registers with the server | Registration successful in screenshot |
| Player 2 registration | P2 registers with the server | Registration successful in screenshot |
| Game-state update | Client sends x, y and score | Update sent successfully |
| Sequence number | Server acknowledges the sequence number | ACK received for sequence 1 |
| Multiple players | Other player receives the game-state update | Update from the other player is visible |
| SDN controller | Switch connects and forwarding rules are installed | Controller output shows switch connection and flow installation |

## Evidence
- Screenshot 1: Player registration, game-state updates and acknowledgements.
- Screenshot 2: SDN controller connection and flow installation.

## Conclusion
Initial socket communication and player update exchange have been demonstrated. Further verification of packet forwarding through the SDN switch should be documented before final submission.
