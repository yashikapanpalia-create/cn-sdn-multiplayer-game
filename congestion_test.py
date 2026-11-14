SERVER_IP = "10.0.0.3"
TEST_DURATION = 60

def start_congestion(net):
    h1, h2, h3 = net.get('h1'), net.get('h2'), net.get('h3')

    # Separate server ports for the two simultaneous UDP streams
    h3.cmd('iperf3 -s -p 5201 -D')
    h3.cmd('iperf3 -s -p 5202 -D')

    h1.cmd('rm -f /tmp/iperf_h1.log')
    h2.cmd('rm -f /tmp/iperf_h2.log')

    h1.cmd('iperf3 -c 10.0.0.3 -p 5201 -u -b 1.5M -t 60 > /tmp/iperf_h1.log 2>&1 &')
    h2.cmd('iperf3 -c 10.0.0.3 -p 5202 -u -b 1.5M -t 60 > /tmp/iperf_h2.log 2>&1 &')

    print("Background UDP congestion traffic started.")
    print("h1 -> h3: 1.5 Mbps UDP (port 5201)")
    print("h2 -> h3: 1.5 Mbps UDP (port 5202)")
    print("Aggregate offered load: 3 Mbps; shared h3-s1 bottleneck: 2 Mbps")
    print("Game traffic remains on UDP port 5000; test duration: 60 seconds.")

def show_congestion_output(net):
    for name in ('h1', 'h2'):
        print("\n===== iperf3 output: {} =====".format(name))
        print(net.get(name).cmd('cat /tmp/iperf_{}.log'.format(name)))

def stop_congestion(net):
    # Stop iperf3 only; leave the game server and player scripts running.
    for name in ('h1', 'h2', 'h3'):
        net.get(name).cmd('pkill -x iperf3 2>/dev/null || true')
    print("iperf3 background congestion traffic stopped.")
