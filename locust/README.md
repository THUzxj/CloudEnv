# Data Collection

```
locust -f locustfile.py --headless -u 500 -r 10 -H http://172.24.4.150:30001
```

# Custom Load Shapes

[](https://docs.locust.io/en/stable/custom-load-shape.html)


# Run in docker

```bash
docker-compose up --scale worker=4
```
