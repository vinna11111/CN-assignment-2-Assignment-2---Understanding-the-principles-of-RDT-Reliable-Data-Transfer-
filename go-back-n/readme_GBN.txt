1)Launch a Mininet instance by entering the command sudo mn in the terminal.
2)Open an xterm terminal for each host by using xterm h1 for host h1 and xterm h2 for host h2.
3)On host h1, configure network settings with the command:(You need to adjust the delay later for report)
  sudo tc qdisc add dev h1-eth0 root netem delay 5ms loss 5% rate 100Mbit limit 100
4)On host h2, apply similar network settings using:(You need to adjust the delay later for report)
  sudo tc qdisc add dev h2-eth0 root netem delay 5ms loss 5% rate 100Mbit limit 100
5)From the xterm terminal on host h2, run the receiver script by executing:
  python3 es22btech11009_GBN.py
6)Finally, on host h1, execute the sender script with:
  python3 es22btech11009_GBN.py


