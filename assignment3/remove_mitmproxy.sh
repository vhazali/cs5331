sudo sysctl -w net.ipv4.ip_forward=0
sudo iptables -t nat -D PREROUTING -i eth1 -p tcp --dport 80 -j REDIRECT --to-port 8080
sudo iptables -t nat -D PREROUTING -i eth1 -p tcp --dport 443 -j REDIRECT --to-port 8080