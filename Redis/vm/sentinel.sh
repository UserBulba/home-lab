#! /bin/bash

# Default route
ip route add default via 192.168.55.1

# DNS
grep -qxF '192.168.55.21 redis-node-1"' || echo "192.168.55.21 redis-node-1" >> /etc/hosts
grep -qxF '192.168.55.22 redis-node-2"' || echo "192.168.55.22 redis-node-2" >> /etc/hosts
grep -qxF '192.168.55.23 redis-node-3"' || echo "192.168.55.23 redis-node-3" >> /etc/hosts

# Install Redis tools.
echo "Installing redis-tools"
apt-get install redis-tools -y > /dev/null

# Create a configuration path and move config to it.
sudo mkdir -p /opt/conf
sudo cp /tmp/sentinel.conf /opt/conf/sentinel.conf
sudo chmod -R 0777 /opt/conf

# Redis parameters.
sudo sysctl -w vm.overcommit_memory=1
sudo sysctl -w net.ipv4.tcp_syncookies=1   

# Another tuning parameters.
# vm.swappiness=0                       # turn off swapping
# net.ipv4.tcp_sack=1                   # enable selective acknowledgements
# net.ipv4.tcp_timestamps=1             # needed for selective acknowledgements
# net.ipv4.tcp_window_scaling=1         # scale the network window
# net.ipv4.tcp_congestion_control=cubic # better congestion algorithm
# net.ipv4.tcp_syncookies=1             # enable syn cookies
# net.ipv4.tcp_tw_recycle=1             # recycle sockets quickly
# net.ipv4.tcp_max_syn_backlog=NUMBER   # backlog setting
# net.core.somaxconn=NUMBER             # up the number of connections per port
# net.core.rmem_max=NUMBER              # up the receive buffer size
# net.core.wmem_max=NUMBER              # up the buffer size for all connection