from mininet.topo import Topo

class GameNetworkTopo(Topo):

    def build(self):

        # Player 1
        h1 = self.addHost(
            'h1',
            ip='10.0.0.1/24'
        )

        # Player 2
        h2 = self.addHost(
            'h2',
            ip='10.0.0.2/24'
        )

        # Game Server
        h3 = self.addHost(
            'h3',
            ip='10.0.0.3/24'
        )

        # SDN Switch
        s1 = self.addSwitch(
            's1',
            protocols='OpenFlow13'
        )

        # Connect hosts to SDN switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)


topos = {
    'gamenet': lambda: GameNetworkTopo()
}
