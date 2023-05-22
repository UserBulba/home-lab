#! /bin/bash

# Default route
ip route add default via 192.168.55.1

# DNS
grep -qxF '192.168.55.21 redis-node-1"' || echo "192.168.55.21 redis-node-1" >> /etc/hosts
grep -qxF '192.168.55.22 redis-node-2"' || echo "192.168.55.22 redis-node-2" >> /etc/hosts
grep -qxF '192.168.55.23 redis-node-3"' || echo "192.168.55.23 redis-node-3" >> /etc/hosts

# Create a configuration path and move config to it.
sudo mkdir -p /conf
sudo cp /tmp/haproxy.cfg /conf/haproxy.cfg
