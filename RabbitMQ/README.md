# RabbitMQ

## Requirements

---

## Pre-requisites

---

Create a `.env` file in the root directory with the following content:

```ini
RABBITMQ_USERNAME=user
RABBITMQ_PASSWORD=password
RABBITMQ_HOST=host
```

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
