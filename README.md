# UDP Multiplayer Game using Mininet and SDN

## 1. Project Overview

This project implements a UDP-based multiplayer game using Python sockets, Mininet, and a Software-Defined Networking (SDN) controller.

Two players send game-state updates to a central server. The server acknowledges updates and forwards them to the other registered player.

## 2. Network Architecture

- h1 — Player 1 (`10.0.0.1`)
- h2 — Player 2 (`10.0.0.2`)
- h3 — Game server (`10.0.0.3`)
- s1 — OpenFlow 1.3 switch
- Controller — OS-Ken SDN controller

UDP port: `5000`

### Communication Flow

Player 1 / Player 2 → Mininet hosts → SDN switch → Game server

The SDN controller manages the switch's forwarding rules.

## 3. Project Structure

- `app/client.py` — Interactive UDP player client using JSON messages
- `app/server.py` — UDP game server using JSON messages
- `topology.py` — Mininet network topology
- `controller.py` — SDN controller
- `player1.py` — Additional player client implementation
- `player2.py` — Additional player client implementation
- `server.py` — Additional server implementation

The JSON-based application in the `app/` directory is the intended implementation for integration testing. The additional application files may use a different message format and should not be mixed with the JSON-based implementation.

## 4. Application Protocol

The application uses UDP sockets for communication between the players and the game server.

### Player Registration

Each client sends a registration message containing its player ID.

### Game-State Updates

Each update contains:

- `player_id` — Identifies the player
- `seq` — Sequence number of the update
- `game_state` — Contains the player's `x`, `y`, and `score` values

### Server Responses

The server is expected to:

- Confirm successful player registration
- Acknowledge updates using their sequence numbers
- Forward game-state updates to other registered players
- Report errors when necessary

## 5. Technologies and Requirements

- Ubuntu
- Python 3
- Mininet
- Open vSwitch
- OS-Ken SDN controller
- UDP sockets
- JSON for message formatting
- OpenFlow 1.3

## 6. Network Configuration

The Mininet topology uses three hosts connected through an OpenFlow switch.

| Component | Role | IP Address |
|---|---|---|
| h1 | Player 1 | `10.0.0.1` |
| h2 | Player 2 | `10.0.0.2` |
| h3 | Game server | `10.0.0.3` |
| s1 | OpenFlow switch | — |
| OS-Ken | SDN controller | — |

The application uses UDP port `5000`.

## 7. Team Responsibilities

- Person 1: UDP client and server application
- Person 2: Mininet topology and SDN controller
- Person 3: Integration, testing, and documentation

## 8. Running the Project

The JSON-based application files are located in the `app/` directory.

- `app/server.py` — Game server
- `app/client.py` — Player client
- `topology.py` — Mininet topology
- `controller.py` — SDN controller

The server should run on host h3, while the player clients should run on h1 and h2.

For end-to-end testing, start the SDN controller, launch the Mininet topology, start the server on h3, and then start the clients on h1 and h2. Verify that registration, updates, acknowledgements, forwarding, and switch flow installation work as expected.

Use the commands and configuration appropriate to the installed Mininet and OS-Ken environment.

## 9. Testing and Validation

Integration testing was performed for the following functionality:

| Test Case | Observed Result |
|---|---|
| Player registration | Both players registered successfully |
| Single-client update | Game-state update was sent successfully |
| Multiple-client updates | Updates from the other player were displayed |
| Sequence-number acknowledgement | ACK received for sequence number 1 |
| Game-state forwarding | Update from the other player was visible |
| SDN controller | Controller output showed switch connection and flow installation |

Screenshots of the application and controller output are saved as test evidence. Further verification of packet forwarding through the SDN switch should be documented before final submission.

Detailed test results are available in [`tests/test-results.md`](tests/test-results.md).

## 10. Deliverable 1 (D1)

The first deliverable demonstrates the initial implementation and integration of the UDP multiplayer application with the Mininet-based SDN network.

The submission should include:

- Project source code
- Mininet topology
- SDN controller implementation
- UDP client and server implementation
- Network architecture and configuration
- Integration test cases and actual results
- Screenshots demonstrating verified functionality
- Instructions sufficient to reproduce the tests

## 11. Conclusion

This project combines UDP socket programming with Mininet and SDN to demonstrate communication between multiple players and a central game server over a software-defined network. Integration testing verifies application communication and SDN packet forwarding.
