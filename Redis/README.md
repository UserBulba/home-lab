# Redis

## Deploy

---

Create inside *shared* folder directories for each node, named with hostname of theses.

## Requirements

---

Install winget from below url.

[winget](https://aka.ms/getwinget)

Install Vagrant

```bash
winget install -e --id Hashicorp.Vagrant
```

Install VirtualBox

```bash
winget install -e --id Oracle.VirtualBox
```

### Using python lib to connect Redis

---

[redis-py - Python Client for Redis](https://redis.readthedocs.io/en/stable/connections.html)

Install redis-py

```bash
pip install redis
```

## Connect to Redis

---

```sh
redis-cli
redis-cli -h 127.0.0.1 -p 6379
```

## Sentinel

---

```bash
info
sentinel master mymaster
```

[Sentinel](https://redis.io/docs/management/sentinel/)

## Services

Redis Insight:

* [Redis Insight - 1](http://192.168.55.21:8001/)
* [Redis Insight - 2](http://192.168.55.22:8001/)
* [Redis Insight - 3](http://192.168.55.23:8001/)

[HAProxy stats](http://192.168.55.30:1936/stats)

## Compatibility

---

Soft versions:

* VBox - 6.1.32 r149290 (Qt5.6.2)
* Vagrant - 2.2.19
