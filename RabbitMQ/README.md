# RabbitMQ

## Requirements

---

## Usage

---

## Docker

---

Run all services

```bash
docker compose -p octo up -d --build
```

Run only one service without dependencies:

```bash
docker compose -p octo up -d --build python_producer --no-deps
```

Remove all services

```bash
docker compose -p octo down --remove-orphans
```



### Debug

Set environment variable `MODE` to `DEBUG` to enable debug mode.

```yaml
environment:
    - MODE=DEBUG
```
