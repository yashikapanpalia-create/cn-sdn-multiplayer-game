# UDP Multiplayer Game using Mininet and SDN

## 1. Project Overview

This project implements a UDP-based multiplayer game using Python sockets, Mininet, Open vSwitch, and an SDN controller.

Two players communicate with a central game server. Players register with the server, send game-state updates, receive acknowledgements, and receive updates from the other registered player.

## 2. Network Architecture

The network consists of three Mininet hosts connected to an OpenFlow switch controlled by OS-Ken.

| Component | Role | IP Address |
|---|---|---|
| h1 | Player 1 | `10.0.0.1` |
| h2 | Player 2 | `10.0.0.2` |
| h3 | Game server | `10.0.0.3` |
| s1 | OpenFlow 1.3 switch | — |
| OS-Ken | SDN controller | — |

Transport protocol: UDP  
Application port: `5000`

### Communication Flow

`Player 1 / Player 2 → Mininet hosts → SDN switch → Game server`

The SDN controller learns MAC addresses and installs forwarding rules as traffic passes through the switch.

## 3. Project Structure

```text
cn-sdn-multiplayer-game/
├── app/
│   ├── client.py
│   └── server.py
├── evidence/
│   ├── README.md
│   ├── Player communication (P1 and P2).png
│   └── SDN controller (flow installation).png
├── tests/
│   └── test-results.md
├── controller.py
├── topology.py
├── player1.py
├── player2.py
├── server.py
├── .gitignore
└── README.md
```

The JSON-based application in `app/` is the intended client-server implementation for this project. The additional root-level application files use a separate implementation and should not be mixed with the JSON-based application.

## 4. Application Protocol

The application uses UDP sockets and JSON-formatted messages.

### Registration

Each client sends a registration message containing its player ID.

### Game-State Updates

Each update contains:

- `player_id` — identifies the player
- `seq` — sequence number of the update
- `game_state` — player coordinates (`x`, `y`) and `score`

### Server Responses

The server:

- Confirms player registration
- Acknowledges accepted updates with their sequence numbers
- Forwards game-state updates to other registered players
- Returns error messages for invalid requests

## 5. Technologies and Requirements

- Ubuntu
- Python 3
- Mininet
- Open vSwitch
- OS-Ken SDN controller
- UDP sockets
- JSON
- OpenFlow 1.3

## 6. Setup and Execution

Run the project in the Ubuntu environment where Mininet and OS-Ken are installed.

### Step 1: Open the project directory

```bash
cd ~/multiplayer_sdn
```

If your project is stored elsewhere, use that directory instead.

### Step 2: Start the SDN controller

Open a terminal, activate the Python environment in which OS-Ken is installed, navigate to the project directory, and run:

```bash
osken-manager controller.py
```

Keep this terminal running.

### Step 3: Start Mininet

Open a second terminal and run:

```bash
sudo mn --custom ~/multiplayer_sdn/topology.py --topo gamenet --controller=remote --switch ovs,protocols=OpenFlow13
```

Wait for the `mininet>` prompt.

### Step 4: Start the game server

At the Mininet prompt, run:

```text
h3 python3 /home/yashika/multiplayer_sdn/app/server.py
```

Keep the server running. If your Ubuntu username or project location differs, replace the path accordingly.

### Step 5: Start the player clients

Open separate terminals or use Mininet host terminals to run the clients.

For Player 1:

```bash
python3 /home/yashika/multiplayer_sdn/app/client.py P1 10.0.0.3
```

For Player 2:

```bash
python3 /home/yashika/multiplayer_sdn/app/client.py P2 10.0.0.3
```

Run each client in its respective Mininet host, h1 and h2. Enter three integers for each game-state update, for example:

```text
10 20 0
```

The clients should display registration messages, acknowledgements, and updates received from the other player.

### Step 6: Verify connectivity and forwarding

At the Mininet prompt, check host connectivity:

```text
pingall
```

Inspect the switch's OpenFlow rules:

```text
sh ovs-ofctl -O OpenFlow13 dump-flows s1
```

Check the controller terminal for switch connection, table-miss flow installation, and forwarding-flow installation messages.

## 7. Testing and Validation

The following functionality was demonstrated in the recorded test sessions.

| Test Case | Observed Result |
|---|---|
| Player 1 registration | Registration successful |
| Player 2 registration | Registration successful |
| Game-state update | Client sent coordinates and score |
| Sequence-number acknowledgement | ACK received for sequence number 1 |
| Multiple-player communication | Each player received the other player's update |
| SDN controller | Switch connection and flow installation messages were displayed |

The controller logs demonstrate flow installation. The switch flow-table command above can be used to inspect the installed rules directly.

Detailed results are available in [`tests/test-results.md`](tests/test-results.md).

## 8. Test Evidence

The screenshots are stored in the repository's `evidence/` folder.

- [Player communication: registration, updates, and ACKs](evidence/Player%20communication%20(P1%20and%20P2).png)
- [SDN controller: switch connection and flow installation](evidence/SDN%20controller%20(flow%20installation).png)

The evidence folder also contains [`evidence/README.md`](evidence/README.md), which describes the screenshots.

## 9. Team Responsibilities

- Person 1: UDP client and server application
- Person 2: Mininet topology and SDN controller
- Person 3: Integration, testing, and documentation

## 10. Deliverable 1 (D1)

The first deliverable demonstrates the initial implementation of a UDP multiplayer application integrated with a Mininet-based SDN network.

The repository contains:

- UDP client and server source code
- Mininet topology
- SDN controller implementation
- Network architecture and application protocol
- Setup and execution instructions
- Integration test results
- Screenshots of player communication and controller output

## 11. Conclusion

This project demonstrates UDP socket communication between two players and a central game server in a Mininet environment controlled by an SDN controller. The recorded tests demonstrate player registration, game-state updates, acknowledgements, update forwarding, and controller flow installation.forwarding.
