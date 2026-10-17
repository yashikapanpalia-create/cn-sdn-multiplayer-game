# UDP Multiplayer Game using Mininet and SDN

## 1. Project Overview

This project implements a UDP-based multiplayer game using Python sockets, Mininet, and an SDN controller.

Two players send game-state updates to a central server. The server acknowledges updates and forwards them to the other registered player.

## 2. Network Architecture

- h1 — Player 1 (`10.0.0.1`)
- h2 — Player 2 (`10.0.0.2`)
- h3 — Game server (`10.0.0.3`)
- s1 — OpenFlow 1.3 switch
- Controller — OS-Ken

UDP port: `5000`

Communication flow:

`Player 1 / Player 2 → Mininet hosts → SDN switch → Game server`

## 3. Project Structure

- `app/client.py` — interactive UDP player client
- `app/server.py` — UDP game server
- `topology.py` — Mininet topology
- `controller.py` — SDN controller
- `player1.py`, `player2.py`, `server.py` — additional application implementation files

## 4. Application Protocol

Clients register with a player ID. Game-state updates contain a player ID, sequence number, and game state (`x`, `y`, and `score`).

The server acknowledges accepted sequence numbers and forwards updates to other registered players.

## 5. Requirements

- Ubuntu
- Python 3
- Mininet
- Open vSwitch
- OS-Ken SDN controller

## 6. Testing

D1 integration tests cover:

1. Player registration
2. Single-client updates
3. Multiple-client updates
4. Sequence-number acknowledgements
5. Game-state forwarding
6. SDN switch forwarding and flow installation

Record the actual results and attach screenshots before submission.

## 7. Team Responsibilities

- Person 1: UDP application
- Person 2: Mininet topology and SDN controller
- Person 3: Integration, testing, and D1 demonstration
