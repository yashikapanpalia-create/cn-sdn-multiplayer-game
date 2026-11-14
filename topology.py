from mininet.topo import Topo
from mininet.link import TCLink

class GameNetworkTopo(Topo):
    def build(self):
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        s1 = self.addSwitch('s1', protocols='OpenFlow13')

        # Player access links
        self.addLink(h1, s1, cls=TCLink, bw=10, delay='5ms')
        self.addLink(h2, s1, cls=TCLink, bw=10, delay='5ms')

        # Shared 2 Mbps bottleneck to the game server
        self.addLink(h3, s1, cls=TCLink, bw=2, delay='10ms')

topos = {'gamenet': lambda: GameNetworkTopo()}
