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

**Transport protocol:** UDP  
**Application port:** `5000`

### Communication Flow

`Player 1 / Player 2 → Mininet hosts → SDN switch → Game server`

The SDN controller manages the switch's forwarding behavior by installing OpenFlow rules. The switch forwards packets between the players and the game server.

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

The JSON-based client-server implementation in `app/` is the intended application for the documented setup. The additional root-level application files use a separate implementation and should not be mixed with the files in `app/`.

## 4. Application Protocol

The application uses UDP sockets and JSON-formatted messages.

### Registration

Each client sends a registration message containing its player ID. The server records the player's address and sends a registration confirmation.

### Game-State Updates

Each update contains:

- `player_id` — identifies the player
- `seq` — sequence number of the update
- `game_state` — player coordinates (`x`, `y`) and `score`

### Server Responses

The server:

- Confirms player registration.
- Acknowledges accepted updates with their sequence numbers.
- Forwards game-state updates to other registered players.
- Returns error messages for invalid requests.

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

The commands below assume that the project is located at `/home/yashika/multiplayer_sdn`. Replace this path if your project is stored elsewhere.

### Step 1: Open the project directory

```bash
cd ~/multiplayer_sdn
```

### Step 2: Start the SDN controller

Open a terminal, activate the Python environment in which OS-Ken is installed, and navigate to the project directory.

Run:

```bash
osken-manager controller.py
```

Keep the controller running in this terminal.

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

Keep the server running.

### Step 5: Start the player clients

Open another terminal and enter the Mininet CLI if needed, then start each client on its respective host.

For Player 1, run at the `mininet>` prompt:

```text
h1 python3 /home/yashika/multiplayer_sdn/app/client.py P1 10.0.0.3
```

For Player 2, run at the `mininet>` prompt:

```text
h2 python3 /home/yashika/multiplayer_sdn/app/client.py P2 10.0.0.3
```

Enter three integers for each game-state update: `x y score`.

Example:

```text
10 20 0
```

The clients should display registration messages, acknowledgements, and game-state updates received from the other player.

### Step 6: Verify connectivity and forwarding

At the Mininet prompt, check connectivity between hosts:

```text
pingall
```

Inspect the switch's OpenFlow rules:

```text
sh ovs-ofctl -O OpenFlow13 dump-flows s1
```

Check the controller terminal for switch connection, table-miss flow installation, and forwarding-flow installation messages.

## 7. Testing and Validation

The following functionality was demonstrated during integration testing.

| Test Case | Observed Result |
|---|---|
| Player 1 registration | Registration successful |
| Player 2 registration | Registration successful |
| Host connectivity | `pingall` completed with 0% packet loss |
| Game-state update | Client sent coordinates and score |
| Sequence-number acknowledgement | ACK received for sequence number 1 |
| Multiple-player communication | Each player received the other player's update |
| SDN controller | Switch connection, table-miss flow installation, and forwarding-flow installation messages were observed |

The connectivity test, player communication tests, and controller output provide evidence of the integration. The switch flow-table command in Step 6 can also be used to inspect the installed OpenFlow rules.

Detailed results are available in [`tests/test-results.md`](tests/test-results.md).

## 8. Test Evidence

Screenshots from the integration tests are stored in the repository's `evidence/` folder.

- [Player communication: registration, updates, and acknowledgements](evidence/Player%20communication%20(P1%20and%20P2).png)
- [SDN controller: switch connection and flow installation](evidence/SDN%20controller%20(flow%20installation).png)

The folder also contains [`evidence/README.md`](evidence/README.md), which describes the screenshots.

## 9. Team Responsibilities

- **Person 1:** UDP client and server application
- **Person 2:** Mininet topology and SDN controller
- **Person 3:** Integration, testing, and documentation

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

This project demonstrates UDP socket communication between two players and a central game server in a Mininet environment controlled by an SDN controller. Integration testing demonstrated player registration, game-state updates, sequence-number acknowledgements, updates between players, host connectivity, and SDN controller flow installation.

The project establishes the initial implementation of a multiplayer application over a software-defined network and provides source code, execution instructions, test results, and supporting screenshots.

