# Live Multiplayer Communication Test Report

## 1. Test Objective

To verify that two UDP clients can communicate with a central game server through the SDN-controlled Mininet network.

## 2. Test Setup

| Component | Configuration |
|---|---|
| Player 1 | h1 – 10.0.0.1 |
| Player 2 | h2 – 10.0.0.2 |
| Game server | h3 – 10.0.0.3 |
| Transport protocol | UDP |
| Application port | 5000 |
| Network switch | Open vSwitch |
| Controller | OS-Ken |

## 3. Test Procedure

1. Start the SDN controller and Mininet topology.
2. Verify connectivity between hosts using `pingall`.
3. Start the game server on h3.
4. Launch both player clients on h1 and h2.
5. Register both players with the server.
6. Send game-state updates from both clients.
7. Observe server acknowledgements and forwarded player updates.

## 4. Observations

- Both players successfully registered with the server.
- The server received game-state updates from the clients.
- Acknowledgements were returned to the respective clients.
- Updates from one player were forwarded to the other player.
- Sequence numbers were included in game-state updates.
- Network connectivity was verified with 0% packet loss using `pingall`.

## 5. Result

The live test demonstrated successful UDP communication between both players and the central game server. Player registration, game-state transmission, acknowledgement handling and update forwarding were observed.

## 6. Conclusion

The multiplayer application successfully demonstrated its core communication functionality over the SDN-controlled Mininet network.
