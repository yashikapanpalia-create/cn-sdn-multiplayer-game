# Project Evidence

This folder contains screenshots demonstrating the implementation and testing of the SDN-based UDP multiplayer game.

## 1. Player Communication

Demonstrates successful registration of both players with the game server, exchange of game-state updates, and acknowledgement messages during communication.

## 2. SDN Controller

Shows the SDN controller connecting to the OpenFlow switch and installing flow rules to manage packet forwarding.

## 3. Network Connectivity

Shows successful connectivity between all Mininet hosts using the `pingall` command.

## 4. Normal Network Communication

Demonstrates player-server communication under normal network conditions, including registration, game-state updates, acknowledgements, latency and RTT measurements.

## 5. Congestion Testing

Shows the generation of background UDP traffic to introduce congestion in the network and the effect on multiplayer communication.

## 6. Performance Measurements

Includes iperf3 results for both players, showing received bandwidth, packet loss and network jitter.

## 7. Traffic-Control Statistics

Shows the traffic-control statistics of the server-facing link, including dropped packets and overlimit events.
